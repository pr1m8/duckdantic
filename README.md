# Duckdantic 🦆

[![PyPI - Version](https://img.shields.io/pypi/v/duckdantic.svg)](https://pypi.org/project/duckdantic)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/duckdantic.svg)](https://pypi.org/project/duckdantic)

**Fluent duck typing for Pydantic and beyond.**

Duckdantic provides structural typing and runtime validation for Python, enabling seamless duck typing with Pydantic models and other data structures.

## Why Duckdantic?

In Python, if it walks like a duck and quacks like a duck, it's probably a duck. But what if you want to make _sure_ it's a duck at runtime? What if you want to check if that dictionary has the right "duck-like" fields, regardless of its actual type?

Duckdantic bridges this gap by providing:

- 🦆 **True duck typing** - Check object structure, not inheritance
- 🔍 **Runtime validation** - Ensure objects match expected traits
- 🎯 **Zero dependencies** - Works with Pydantic, dataclasses, TypedDict, and more
- ⚡ **Blazing fast** - Caches normalization for optimal performance
- 🐍 **Pythonic** - Integrates with `isinstance()` and `issubclass()`

## Installation

```bash
pip install duckdantic
```

## Quick Start

### Basic Duck Typing

```python
from duckdantic import TraitSpec, FieldSpec, satisfies

# Define what a "duck" looks like
duck_trait = TraitSpec(
    name="Duck",
    fields=[
        FieldSpec(name="name", type=str, required=True),
        FieldSpec(name="age", type=int, required=True),
        FieldSpec(name="quack", type=str, required=False),
    ]
)

# Any object can be a duck if it has the right fields
class Bird:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# This dictionary is also a duck!
duck_dict = {"name": "Donald", "age": 5}

# Check if they satisfy the duck trait
assert satisfies(Bird("Daffy", 3), duck_trait)
assert satisfies(duck_dict, duck_trait)
```

### Working with Pydantic

```python
from pydantic import BaseModel
from duckdantic import satisfies, TraitSpec, FieldSpec

# Your existing Pydantic model
class User(BaseModel):
    id: int
    email: str
    name: str | None = None

# Define trait independently
user_trait = TraitSpec(
    name="UserLike",
    fields=[
        FieldSpec(name="id", type=int, required=True),
        FieldSpec(name="email", type=str, required=True),
    ]
)

# Works with Pydantic models
user = User(id=1, email="duck@example.com")
assert satisfies(user, user_trait)

# But also with plain dictionaries
user_dict = {"id": 2, "email": "goose@example.com"}
assert satisfies(user_dict, user_trait)

# And even other objects
class Customer:
    def __init__(self, id: int, email: str, company: str):
        self.id = id
        self.email = email
        self.company = company

customer = Customer(3, "swan@example.com", "Duck Corp")
assert satisfies(customer, user_trait)  # It's user-like!
```

### Python Integration with ABCs

```python
from duckdantic import TraitSpec, FieldSpec, abc_for

# Define a trait
person_trait = TraitSpec(
    name="Person",
    fields=[
        FieldSpec(name="name", type=str, required=True),
        FieldSpec(name="age", type=int, required=True),
    ]
)

# Create an ABC that uses structural typing
PersonABC = abc_for(person_trait)

# Now use with isinstance
class Employee:
    def __init__(self, name: str, age: int, dept: str):
        self.name = name
        self.age = age
        self.dept = dept

emp = Employee("Alice", 30, "Engineering")
assert isinstance(emp, PersonABC)  # True! It has the required fields
```

### Method Signature Checking

```python
from duckdantic import MethodSpec, methods_satisfy

# Define required methods
db_trait_methods = [
    MethodSpec(name="save", params=[str], returns=bool),
    MethodSpec(name="load", params=[int], returns=str),
]

class Database:
    def save(self, data: str) -> bool:
        return True

    def load(self, id: int) -> str:
        return f"Data {id}"

assert methods_satisfy(Database(), db_trait_methods)
```

## Advanced Features

### Type Policies

Control how types are compared:

```python
from duckdantic import satisfies, POLICY_PRAGMATIC, TypeCompatPolicy

# Strict policy - exact type matches only
strict_policy = TypeCompatPolicy(
    allow_subclass=False,
    numeric_widening=False,
    literal_compatibility=False
)

# Pragmatic policy (default) - sensible defaults
# Allows int -> float, subclasses, etc.
result = satisfies(obj, trait, policy=POLICY_PRAGMATIC)
```

### Detailed Explanations

Get detailed information about why validation failed:

```python
from duckdantic import explain

result = explain(obj, trait)
if not result["ok"]:
    print("Missing fields:", result["missing"])
    print("Type mismatches:", result["type_mismatches"])
    print("Failed requirements:", result["failed_requirements"])
```

### Set Operations

Combine traits using set operations:

```python
from duckdantic import union, intersect, minus

# Create a trait that requires fields from both
combined = intersect(user_trait, profile_trait)

# Create a trait that accepts either
flexible = union(user_trait, guest_trait)

# Remove fields from a trait
simplified = minus(user_trait, ["email", "phone"])
```

### Registry Pattern

Manage collections of traits:

```python
from duckdantic import TraitRegistry

registry = TraitRegistry()
registry.add("User", user_trait)
registry.add("Admin", admin_trait)

# Find all traits an object satisfies
compatible = registry.compatible_traits(some_object)
print(f"Object satisfies: {compatible}")
```

## Supported Types

Duckdantic works with:

- ✅ Pydantic models (v2)
- ✅ Standard dataclasses
- ✅ TypedDict classes
- ✅ attrs classes
- ✅ Plain classes with annotations
- ✅ Dictionaries and mappings
- ✅ Any combination of the above!

## Performance

Duckdantic uses intelligent caching to ensure optimal performance:

```python
from duckdantic import get_cache_stats, clear_cache

# Check cache performance
stats = get_cache_stats()
print(f"Cache hits: {stats['hits']}, misses: {stats['misses']}")

# Clear cache if needed
clear_cache()
```

## Use Cases

- **API Validation** - Ensure responses match expected structure
- **Plugin Systems** - Verify plugins implement required interfaces
- **Configuration** - Validate settings from multiple sources
- **Testing** - Assert objects have expected shape
- **Integration** - Bridge between different frameworks

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## License

Duckdantic is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

---

_If it walks like a duck and quacks like a duck, Duckdantic can check that for you!_ 🦆
