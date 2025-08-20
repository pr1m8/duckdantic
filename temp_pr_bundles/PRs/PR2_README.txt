PR 2: Methods API + ABC sugar
=============================

Add the following files into your repo:

  structdantic/build/methods.py
  structdantic/adapters/abc.py
  tests/test_methods_satisfy.py
  tests/test_abc_adapter.py

Then update `structdantic/__init__.py` to export:

    from .build.methods import MethodSpec, methods_satisfy, methods_explain
    from .adapters.abc import abc_for, duckisinstance, duckissubclass
    __all__ += ["MethodSpec", "methods_satisfy", "methods_explain", "abc_for", "duckisinstance", "duckissubclass"]

Run tests:

    pytest -q

Both tests are framework-agnostic and do not require Pydantic.
