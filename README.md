# dedap-python

**dedap** implements transitive reduction for directed acyclic graphs.
DAGs are used for scheduling operations, and transitive reduction produces
equivalent DAGs sans redundant links.

## Installation

On Windows:

```cmd
py -m pip install dedap
```

On other systems (e.g., Linux, macOS):

```sh
python3 -m pip install dedap
```

## Testing

To run this module's tests after installation:

```sh
python3 -m doctest dedap
```

To check the static type consistency, use `mypy` if it's available:

```sh
mypy dedap
```

## Future

+ Bind [C++ dedap library](https://github.com/studdansen/dedap) into this
  Python package.
