# dedap-python

**dedap** implements transitive reduction for directed acyclic graphs.
DAGs are used for scheduling operations, and transitive reduction produces
equivalent DAGs sans redundant links.

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

To build the PDF documentation:

```sh
make -C doc latexpdf
```

## Future

+ Bind [C++ dedap library](https://github.com/studdansen/dedap) into this
  Python package. Call it `cdedap`.
  
  + Write benchmark tests to compare the C++-based implementation (`cdedap`) to
    the pure Python implementation.
