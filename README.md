# dedap-python

**dedap** implements transitive reduction for acyclic directed graphs.
DAGs are used for scheduling operations, and transitive reduction produces
equivalent DAGs without redundant links.

The module is only dependent on the Python standard library for normal use.
It does need external modules for building the installable package, for
checking static type consistency, and for building the documentation.

## Installation

On Windows:

```cmd
py -m pip install --upgrade pip
py -m pip install dedap
```

On other systems (e.g., Linux, macOS):

```sh
python3 -m pip install --upgrade pip
python3 -m pip install dedap
```

## Basic Usage

A graph is a collection of nodes with unidirectional links between them. A
node can be a string, a number, or any other Python object that can be compared
by value.

The nodes comprising a collection of these inter-node links can be sorted into
a new tuple topologically. That is, if some node ``p`` is a "first" node that
comes before some "second" node ``q`` either directly or indirectly among the
links, then ``p`` will come before ``q`` in the newly created node sequence.

```python3
>>> from dedap import Link, topo_sorted_nodes
>>> links = [Link(first='B', second='D'), Link(first='A', second='B'), \
...   Link('B', 'C'), Link('C', 'D'), Link('A', 'E')]
>>> topo_sorted_nodes(links)
('A', 'E', 'B', 'C', 'D')

```

With simplified syntax (not yet supported):

```python3
>>> from dedap import topo_sorted_nodes
>>> links = [('B', 'D'), ('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'E')]
>>> topo_sorted_nodes(links)
('A', 'E', 'B', 'C', 'D')

```

If a collection of links cannot be sorted topologically, it means that the
graph composed of those links is not acyclic. At this stage of the module's
development, only directed *acyclic* graphs can be transitively reduced.

## Testing

This module has [doctest](https://docs.python.org/3/library/doctest.html)-style
unit tests within its docstrings.

To run this module's tests from the source directory:

```sh
python3 -m doctest dedap/dedap.py
```

To run this module's tests after installation:

```sh
python3 -m doctest dedap/dedap.py
```

To check the static type consistency, use `mypy` if it's available:

```sh
mypy dedap/dedap.py
```

## Documentation

To build the HTML documentation:

```sh
make -C doc html
```

To build the PDF documentation (assuming all LaTeX dependencies are installed):

```sh
make -C doc latexpdf
```

## Future

+ Bind [C++ dedap library](https://github.com/studdansen/dedap) into this
  Python package. Call it `cdedap`.
  
  + Write benchmark tests to compare the C++-based implementation (`cdedap`) to
    the pure Python implementation.
