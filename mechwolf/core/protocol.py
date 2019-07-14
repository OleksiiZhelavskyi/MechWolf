import asyncio
import json
import tempfile
import webbrowser
from copy import deepcopy
from datetime import timedelta
from math import isclose
from typing import Iterable, Optional, Union
from warnings import warn

import yaml
from IPython.display import HTML, Code, display
from jinja2 import Environment, PackageLoader, select_autoescape
from loguru import logger

from .. import ureg
from ..components import ActiveComponent, TempControl, Valve
from .apparatus import Apparatus
from .execute import main
from .experiment import Experiment


class Protocol(object):
    """
    A set of procedures for an apparatus.

    A protocol is defined as a list of procedures, atomic steps for the individual active components of an apparatus.

    ::: tip
    The same `Apparatus` object can create multiple distinct `Protocol` objects.
    :::

    Attributes:
    - `apparatus`: The apparatus for which the protocol is being defined.
    - `name`: The name of the protocol. Defaults to "Protocol_X" where *X* is protocol count.
    """

    _id_counter = 0

    def __init__(
        self,
        apparatus: Apparatus,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        # type checking
        if not isinstance(apparatus, Apparatus):
            raise TypeError(
                f"Must pass an Apparatus object. Got {type(apparatus)}, "
                "which is not an instance of mechwolf.Apparatus."
            )

        # ensure apparatus is valid
        if not apparatus.validate():
            raise ValueError("Apparaus is not valid.")

        # store the passed args
        self.apparatus = apparatus
        self.description = description

        # generate the name
        if name is not None:
            self.name = name
        else:
            self.name = "Protocol_" + str(Protocol._id_counter)
            Protocol._id_counter += 1

        # default values
        self.procedures = []
        self.is_executing = False
        self.was_executed = False

    def __repr__(self):
        return f"<{self.__str__()}>"

    def __str__(self):
        return f"Protocol {self.name} defined over {repr(self.apparatus)}"

    def _add_single(
        self,
        component: ActiveComponent,
        start="0 seconds",
        stop=None,
        duration=None,
        **kwargs,
    ):
        """Adds a single procedure to the protocol.

        See add() for full documentation.
        """

        # make sure that the component being added to the protocol is part of the apparatus
        if component not in self.apparatus.components:
            raise ValueError(
                f"{component} is not a component of {self.apparatus.name}."
            )

        # perform the mapping for valves
        if isinstance(component, Valve) and kwargs.get("setting") is not None:
            try:
                kwargs["setting"] = component.mapping[kwargs["setting"]]
            except KeyError:
                # allow direct specification of valve settings
                if isinstance(kwargs["setting"], int):
                    pass

        # don't let users give empty procedures
        if not kwargs:
            raise RuntimeError(
                "No kwargs supplied. This will not manipulate the state of your sythesizer. Ensure your call to add() is valid."
            )

        # make sure the component and keywords are valid
        for kwarg, value in kwargs.items():

            if not hasattr(component, kwarg):
                raise ValueError(
                    f"Invalid attribute {kwarg} for {component}."
                    f" Valid attributes are {[x for x in vars(component).keys() if x != 'name' and not x.startswith('_')]}."
                )

            if (
                isinstance(component.__dict__[kwarg], ureg.Quantity)
                and ureg.parse_expression(value).dimensionality
                != component.__dict__[kwarg].dimensionality
            ):
                raise ValueError(
                    f"Bad dimensionality of {kwarg} for {component}. "
                    f"Expected dimensionality of {component.__dict__[kwarg].dimensionality} "
                    f"but got {ureg.parse_expression(value).dimensionality}."
                )

            elif not isinstance(
                component.__dict__[kwarg], type(value)
            ) and not isinstance(component.__dict__[kwarg], ureg.Quantity):
                raise ValueError(
                    f"Bad type matching. Expected {kwarg} to be {type(component.__dict__[kwarg])} "
                    f"but got {value}, which is of type {type(value)}"
                )

        if stop is not None and duration is not None:
            raise RuntimeError("Must provide one of stop and duration, not both.")

        # parse the start time if given
        if isinstance(start, timedelta):
            start = str(start.total_seconds()) + " seconds"
        start = ureg.parse_expression(start)

        # parse duration if given
        if duration is not None:
            if isinstance(duration, timedelta):
                duration = str(duration.total_seconds()) + " seconds"
            stop = start + ureg.parse_expression(duration)
        elif stop is not None:
            if isinstance(stop, timedelta):
                stop = str(stop.total_seconds()) + " seconds"
            if isinstance(stop, str):
                stop = ureg.parse_expression(stop)

        if start is not None and stop is not None and start > stop:
            raise ValueError("Procedure beginning is after procedure end.")

        # a little magic for temperature controllers
        if issubclass(component.__class__, TempControl):
            if kwargs.get("temp") is not None and kwargs.get("active") is None:
                kwargs["active"] = True
            elif not kwargs.get("active") and kwargs.get("temp") is None:
                kwargs["temp"] = "0 degC"
            elif kwargs["active"] and kwargs.get("temp") is None:
                raise RuntimeError(
                    f"TempControl {component} is activated but temperature "
                    "setting is not given. Specify 'temp' in your call to add()."
                )

        # add the procedure to the procedure list
        self.procedures.append(
            dict(
                start=float(start.to_base_units().magnitude)
                if start is not None
                else start,
                stop=float(stop.to_base_units().magnitude)
                if stop is not None
                else stop,
                component=component,
                params=kwargs,
            )
        )

    def add(
        self,
        component: Union[ActiveComponent, Iterable],
        start="0 seconds",
        stop=None,
        duration=None,
        **kwargs,
    ):
        """
        Adds a procedure to the protocol.

        ::: warning
        If stop and duration are both `None`, the procedure's stop time will be inferred as the end of the protocol.
        :::

        # Arguments
        - `component_added`: The component(s) for which the procedure being added. If an interable, all components will have the same parameters.
        - `start`: The start time of the procedure relative to the start of the protocol, such as `"5 seconds"`. May also be a `datetime.timedelta`. Defaults to `"0 seconds"`, *i.e.* the beginning of the protocol.
        - `stop`: The stop time of the procedure relative to the start of the protocol, such as `"30 seconds"`. May also be a `datetime.timedelta`. May not be given if `duration` is used.
        duration: The duration of the procedure, such as "1 hour". May not be used if `stop` is used.
        - `**kwargs`: The state of the component for the procedure.

        # Raises
        - `TypeError`: A component is not of the correct type (*i.e.* a Component object)
        - `ValueError`: An error occurred when attempting to parse the kwargs.
        - `RuntimeError`: Stop time of procedure is unable to be determined or invalid component.
        """

        try:
            iter(component)
        except TypeError:
            component = [component]

        for _component in component:
            self._add_single(
                _component, start=start, stop=stop, duration=duration, **kwargs
            )

    @property
    def _inferred_duration(self):
        # infer the duration of the protocol
        computed_durations = sorted(
            [x["stop"] for x in self.procedures],
            key=lambda z: z if z is not None else 0,
        )
        if all([x is None for x in computed_durations]):
            raise RuntimeError(
                "Unable to automatically infer duration of protocol. "
                'Must define stop or duration for at least one procedure to use duration="auto".'
            )
        return computed_durations[-1]

    def compile(self, dry_run: bool = True, _visualization: bool = False) -> dict:
        """
        Compile the protocol into a dict of devices and their procedures.

        # Returns
        A dict with components as the values and lists of their procedures as the value. The elements of the list of procedures are dicts with two keys: "time" in seconds, and "params", whose value is a dict of parameters for the procedure.

        # Raises
        - `RuntimeError`: When compilation fails.
        """
        output = {}

        if len({c.name for c in self.apparatus._active_components}) != len(
            self.apparatus._active_components
        ):
            raise RuntimeError("Found ActiveComponents with duplicate names.")

        # deal only with compiling active components
        for component in self.apparatus._active_components:
            # determine the procedures for each component
            component_procedures = sorted(
                [x for x in self.procedures if x["component"] == component],
                key=lambda x: x["start"],
            )

            # skip compiling components without procedures
            if not len(component_procedures):
                warn(
                    f"{component} is an active component but was not used in this procedure."
                    " If this is intentional, ignore this warning."
                )
                continue

            # validate each component
            if not component.validate(dry_run=dry_run):
                raise RuntimeError("Component is not valid.")

            # check for conflicting continuous procedures
            if (
                len(
                    [
                        x
                        for x in component_procedures
                        if x["start"] is None and x["stop"] is None
                    ]
                )
                > 1
            ):
                raise RuntimeError(
                    f"{component} cannot have two procedures for the entire duration of the protocol. "
                    "If each procedure defines a different attribute to be set for the entire duration, "
                    "combine them into one call to add(). Otherwise, reduce ambiguity by defining start "
                    "and stop times for each procedure. "
                    ""
                )

            for i, procedure in enumerate(component_procedures):

                # automatically infer start and stop times
                try:
                    if component_procedures[i + 1]["start"] == 0:
                        raise RuntimeError(
                            f"Ambiguous start time for {procedure['component']}. " ""
                        )
                    elif (
                        component_procedures[i + 1]["start"] is not None
                        and procedure["stop"] is None
                    ):
                        warn(
                            f"Automatically inferring stop time for {procedure['component']} "
                            f"as beginning of {procedure['component']}'s next procedure."
                        )
                        procedure["stop"] = component_procedures[i + 1]["start"]
                except IndexError:
                    if procedure["stop"] is None:
                        warn(
                            f"Automatically inferring stop for {procedure['component']} as "
                            f"the end of the protocol. To override, provide stop in your call to add()."
                        )
                        procedure["stop"] = self._inferred_duration

            # give the component instructions at all times
            compiled = []
            for i, procedure in enumerate(component_procedures):
                if _visualization:
                    compiled.append(
                        dict(
                            start=procedure["start"],
                            stop=procedure["stop"],
                            params=procedure["params"],
                        )
                    )
                else:
                    compiled.append(
                        dict(time=procedure["start"], params=procedure["params"])
                    )

                    # if the procedure is over at the same time as the next
                    # procedure begins, don't go back to the base state
                    try:
                        if isclose(
                            component_procedures[i + 1]["start"], procedure["stop"]
                        ):
                            continue
                    except IndexError:
                        pass

                    # otherwise, go back to base state
                    compiled.append(
                        dict(time=procedure["stop"], params=component.base_state())
                    )

            output[component] = compiled

            # raise warning if duration is explicitly given but not used?
        return output

    def to_dict(self):
        compiled = deepcopy(self.compile(dry_run=True))
        compiled = {k.name: v for (k, v) in compiled.items()}
        return compiled

    def to_list(self):
        output = []
        for procedure in deepcopy(self.procedures):
            procedure["component"] = procedure["component"].name
            output.append(procedure)
        return output

    def yaml(self) -> Union[str, Code]:
        """
        Outputs the uncompiled procedures to YAML.

        Internally, this is a conversion of the output of `Protocol.json` for the purpose of enhanced human readability.

        # Returns:
        YAML of the procedure list. When in Jupyter, this string is wrapped in an `IPython.display.Code` object for nice syntax highlighting.

        """
        compiled_yaml = yaml.safe_dump(self.to_list(), default_flow_style=False)

        try:
            get_ipython
            return Code(compiled_yaml, language="yaml")
        except NameError:
            pass
        return compiled_yaml

    def json(self) -> Union[str, Code]:
        """
        Outputs the uncompiled procedures to JSON.

        # Returns
        JSON of the protocol. When in Jupyter, this string is wrapped in a `IPython.display.Code` object for nice syntax highlighting.
        """
        compiled_json = json.dumps(self.to_list(), sort_keys=True, indent=4)

        try:
            get_ipython
            return Code(compiled_json, language="json")
        except NameError:
            pass
        return compiled_json

    def visualize(self, browser: bool = True) -> Union[str, HTML]:
        """
        Generates a Gantt plot visualization of the protocol.

        # Arguments
        - `browser`: Whether to open in the browser.

        # Returns
        The html of the visualization. When in Jupyter, this string is wrapped in a `IPython.display.HTML` object for interactive display.
        """

        # render the html
        env = Environment(
            autoescape=select_autoescape(["html", "xml"]),
            loader=PackageLoader("mechwolf", "templates"),
        )
        visualization = env.get_template("viz_div.html").render(
            procedures=self.procedures
        )

        # show it in Jupyter, if possible
        try:
            get_ipython()
            return HTML(visualization)
        except NameError:
            pass

        template = env.get_template("visualizer.html")
        visualization = template.render(title=self.name, visualization=visualization)

        if browser:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp:
                tmp.write(visualization.encode("utf-8"))
                webbrowser.open("file://" + tmp.name)

        return visualization

    def execute(self, dry_run: bool = False, verbosity: str = "info") -> Experiment:
        """
        Executes the procedure.

        # Arguments
        - `dry_run`: Whether to simulate the experiment or actually perform it. Defaults to `False`, which means executing the protocol on real hardware.
        - `verbosity`: The level of logging verbosity. One of "critical", "error", "warning", "success", "info", "debug", or "trace" in descending order of severity. "debug" and (especially) "trace" are not meant to be used regularly, as they generate significant amounts of usually useless information. However, these verbosity levels are useful for tracing where exactly a bug was generated, especially if no error message was thrown.

        # Returns
        An `Experiment` object. In a Jupyter notebook, the object yields an interactive visualization.

        # Raises
        `RuntimeError`: When attempting to execute a protocol on invalid components.
        """

        # If protocol is executing, return an error
        if self.is_executing:
            logger.error("Protocol is currently running.")
            return

        logger.info(f"Compiling protocol with dry_run = {dry_run}")
        try:
            compiled_protocol = self.compile(dry_run=dry_run)
        except RuntimeError as e:
            # add an execution-specific message
            raise (RuntimeError(str(e).rstrip() + " Aborting execution..."))

        # the Experiment object is going to hold all the info
        E = Experiment(
            self, compiled_protocol=compiled_protocol, verbosity=verbosity.upper()
        )
        display(E._output_widget)

        self.is_executing = True

        try:
            get_ipython()
            asyncio.ensure_future(main(experiment=E, dry_run=dry_run))
        except NameError:
            asyncio.run(main(experiment=E, dry_run=dry_run))

        return E

    def clear_procedures(self) -> None:
        """
        Reset the protocol's procedures.
        """
        if not self.was_executed or self.is_executing:
            self.procedures = []
        else:
            raise RuntimeError(
                "Unable to clear the procedures of a protocol that has been executed."
            )