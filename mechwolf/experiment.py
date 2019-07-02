import time

import ipywidgets as widgets
from bokeh.io import output_notebook, push_notebook, show
from bokeh.plotting import figure
from bokeh.resources import INLINE
from IPython.display import display
from loguru import logger
from xxhash import xxh32

from .components.sensor import Sensor

try:
    get_ipython  # noqa
    in_ipython = True
except NameError:
    in_ipython = False


class Experiment(object):
    """
        Experiments contain all data from execution of a protocol.
    """

    def __init__(self, protocol, verbosity):
        self.experiment_id = f'{time.strftime("%Y_%m_%d_%H_%M_%S")}_{xxh32(str(protocol.yaml())).hexdigest()}'

        self.protocol = protocol
        self.start_time = None  # the experiment hasn't started until main() is called
        self.end_time = None
        self.data = {}
        self.executed_procedures = []

        self._charts = {}
        self._graphs_shown = False
        self._sensors = [
            c for c in protocol.apparatus.components if isinstance(c, Sensor)
        ][
            ::-1
        ]  # reverse the list so the accordion is in order
        self._device_name_to_unit = {c.name: c._unit for c in self._sensors}
        self._sensor_names = [s.name for s in self._sensors]
        self._transformed_data = {
            s: {"datapoints": [], "timestamps": []} for s in self._sensor_names
        }

        # create a nice, pretty HTML string wth the metadata
        metadata = "<ul>"
        for k, v in {
            "Protocol name": self.protocol.name,
            "Start time": self.start_time,
        }.items():
            metadata += f"<li>{k}: {v}</li>"
        metadata += "</ul>"

        # create the output tab widget with its children
        self._tab = widgets.Tab()
        self._tab.children = [widgets.HTML(value=metadata), widgets.Output()]
        self._tab.set_title(0, "Metadata")
        self._tab.set_title(1, "Log")
        if self._sensors:
            self._tab.children = list(self._tab.children) + [
                widgets.Accordion(children=[widgets.Output() for s in self._sensors])
            ]
            self._tab.set_title(2, "Sensors")
            for i, sensor in enumerate(self._sensors):
                self._tab.children[2].set_title(i, sensor.name)

        self._output_widget = widgets.VBox(
            [widgets.HTML(value=f"<h3>Experiment {self.experiment_id}</h3>"), self._tab]
        )

        # route logging to go to the widget TODO: add support for saving to file as well
        logger.remove()

        def log(x):
            with self._output_widget.children[1].children[1]:  # the log
                print(x)

        logger.add(lambda x: log(x), level=verbosity)

    def _repr_html_(self):
        display(self._output_widget)

    def __str__(self):
        return f"<Experiment {self.experiment_id}>"

    def update(self, device: str, datapoint):

        # If a chart has been registered to the device, update it.
        if device not in self.data:
            self.data[device] = []
        self.data[device].append(datapoint)

        if not in_ipython:
            return

        if not self._graphs_shown:
            logger.debug("Graphs not shown. Initializing...")
            for i, sensor in enumerate(self._sensor_names):
                logger.trace(f"Initializing graph #{i+1} for {sensor}")
                with self._output_widget.children[1].children[2].children[i]:
                    p = figure(title=f"{sensor} data", plot_height=300, plot_width=600)

                    r = p.line(
                        source=self._transformed_data[sensor],
                        x="timestamps",
                        y="datapoints",
                        color="#2222aa",
                        line_width=3,
                    )
                    p.xaxis.axis_label = "Experiment elapsed time (seconds)"
                    p.yaxis.axis_label = self._device_name_to_unit[sensor]
                    output_notebook(resources=INLINE, hide_banner=True)
                    target = show(p, notebook_handle=True)
                    self._charts[sensor] = (target, r)
                logger.trace(f"Sucessfully initialized graph {i}")
            logger.trace("All graphs successfully initialized")
            self._graphs_shown = True

        logger.trace(f"Checking to see if {device} is a known sensor")
        if device in self._transformed_data:
            logger.trace(f"It is. Updating the transformed data.")
            target, r = self._charts[device]
            self._transformed_data[device]["datapoints"].append(datapoint.data)
            self._transformed_data[device]["timestamps"].append(
                datapoint.experiment_elapsed_time
            )
            r.data_source.data["datapoints"] = self._transformed_data[device][
                "datapoints"
            ]
            r.data_source.data["timestamps"] = self._transformed_data[device][
                "timestamps"
            ]
            logger.debug(f"Pushing update to the notebook.")
            push_notebook(handle=target)