# Flow Chemistry

The purpose of this module is to allow light weight flow chemistry experiment design in Python. Features include extensive error checking, flexibility, and user extensibility. 

## API Reference

### Apparatus
#### Methods

##### __init__
`__init__(self, name=None)`

Initialization of an `Apparatus` object. 

###### Arguments
* **name**: The name of the apparatus. If not given, defaults to "Apparatus_[number]".

##### add
`add(self, from_component, to_component, tube)`

Adds a connection between components to the apparatus.

###### Arguments
* **from_component**: Component object.
* **to_component**: Component object.
* **tube**: Tube object describing the connection between the two components.

##### visualize
`visualize(self, label=True, node_attr={}, edge_attr={}, graph_attr={}, format="pdf", filename=None)`

Creates a graphical visualization of the apparatus. For full list of acceptable attributes, see [here](https://www.graphviz.org/doc/info/attrs.html) and [here](http://graphviz.readthedocs.io/en/stable/manual.html#attributes)

###### Arguments
* **label**: Boolean. If true, displays the name of the apparatus as the title for the graph. 
* **node_attr**: Dictionary. Attributes to modify the display of nodes.
* **edge_attr**: Dictionary. Attributes to modify the display of edges.
* **graph_attr**: Dictionary. Attributes to modify the display of the graph.
* **format**: String. The output format for rendering.
* **filename**: String. The filename of the output file. If `None`, defaults to the name of the apparatus.

##### summarize
`summarize(self)`

Prints a tabular summary of the apparatus.

##### compile
`compile(self)`

Ensures that the apparatus is valid. While you can call it yourself, creating a protocol automatically checks that the apparatus can be compiled.



### Protocol
#### Methods

##### __init__
`__init__(self, apparatus, duration=None, name=None)`

Initialize the `Protocol` object.

###### Attributes
* **apparatus**: Apparatus object that the protocol is for.
* **duration**: String. The duration of the protocol. Required if using `continuous`. Inferred from the last time given by `add` if not explicitly defined.
* **name**: String. Name of the protocol.

##### add
`add(self, start_time, stop_time, component, **kwargs)`

Add a procedure to the protocol. 

###### Attributes
* **start_time**: String. The start time of the procedure relative to time 0 (the start time of the experiment).
* **stop_time**: String. The stop time of the procedure relative to time 0 (the start time of the experiment).
* **component**: Component. The component which the procedure being added to the protocol if for.
* **\*\*kwargs**: The parameters of the component that are being modified.

##### continuous
`continuous(self, component, **kwargs)`

Add a procedure to be run for the entire duration of the protocol. Useful for activating sensors to collect data. If used, the duration of the experiment must be explicitly defined when the Protocol object is instantiated.

###### Attributes
* **component**:  Component.
* **\*\*kwargs**: The parameters of the component that are being modified for the entire protocol.

##### compile
`compile(self)`

Ensures that the protocol is valid. While you can call it yourself, this is done automatically before any protocol is executed.
