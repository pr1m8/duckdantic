# Duckdantic Examples

## Understanding Duck Typing in Duckdantic

Duckdantic performs structural type checking, which means it compares the **shape** of objects, not whether they are valid instances.

### Basic Usage

```python
from pydantic import BaseModel
from duckdantic import satisfies, TraitSpec, FieldSpec

# Define a Pydantic model
class User(BaseModel):
    id: int
    email: str
    name: str | None = None

# Define a trait that describes the same structure
user_trait = TraitSpec(
    name="User",
    fields=[
        FieldSpec(name="id", typ=int, required=True),
        FieldSpec(name="email", typ=str, required=True),
        FieldSpec(name="name", typ=str, required=False),
    ]
)

# Check if a CLASS has the same structure
assert satisfies(User, user_trait)  # True - User class has these fields

# Check if another model matches
class Customer(BaseModel):
    id: int
    email: str
    company: str

assert satisfies(Customer, user_trait)  # True - has required fields

# Check a plain class
class Person:
    id: int
    email: str
    phone: str = "555-1234"

assert satisfies(Person, user_trait)  # True - has required fields
```

### Duck Typing with Instances

When checking instances, the library looks at the actual types of the fields:

```python
# Create instances
user = User(id=1, email="user@example.com")
customer = Customer(id=2, email="c@example.com", company="ACME")

# Both satisfy the trait because they have the required structure
assert satisfies(user, user_trait)
assert satisfies(customer, user_trait)
```

### Working with Dictionaries

For dictionaries, duckdantic treats the VALUES as the types:

```python
# This dict describes a STRUCTURE, not an instance
user_structure = {
    "id": int,
    "email": str,
    "name": str | None
}

# This works - comparing structure to structure
assert satisfies(user_structure, user_trait)

# For validating dict data, use Pydantic directly
user_data = {"id": 1, "email": "user@example.com"}
user_instance = User.model_validate(user_data)  # Use Pydantic validation
```

### The Duck API

The Duck API provides a more ergonomic interface:

```python
from duckdantic import Duck, DuckModel

# Create a duck type from a model
UserDuck = Duck(User)

# Check if a CLASS satisfies the duck type
assert UserDuck.validate(Customer)  # True - Customer has User's fields

# For runtime validation of data, combine with Pydantic
if UserDuck.validate(Customer):
    # We know Customer has the right shape
    # Now validate actual data
    data = {"id": 1, "email": "test@example.com", "company": "ACME"}
    customer = Customer.model_validate(data)
    # Extract just the User fields
    user = User.model_validate(customer.model_dump())
```

### DuckModel Base Class

```python
class Product(DuckModel):
    id: int
    name: str
    price: float

# Check if another class has the same structure
class InventoryItem:
    id: int
    name: str
    price: float
    quantity: int

assert Product.is_duck(InventoryItem)  # True - has all Product fields

# Convert from compatible instance
item = InventoryItem()
item.id = 1
item.name = "Widget"
item.price = 9.99
item.quantity = 100

product = Product.from_duck(item)  # Extracts just Product fields
```

### Method Signature Checking

```python
from duckdantic import MethodSpec, methods_satisfy

# Define required methods
storage_methods = [
    MethodSpec(name="save", params=[str], returns=bool),
    MethodSpec(name="load", params=[str], returns=dict),
]

class FileStorage:
    def save(self, path: str) -> bool:
        return True

    def load(self, path: str) -> dict:
        return {}

class DatabaseStorage:
    def save(self, key: str) -> bool:
        return True

    def load(self, key: str) -> dict:
        return {}

    def delete(self, key: str) -> bool:
        return True

# Both satisfy the interface
assert methods_satisfy(FileStorage, storage_methods)
assert methods_satisfy(DatabaseStorage, storage_methods)
```

### ABC Integration

```python
from duckdantic import abc_for

# Create an ABC from a trait
UserABC = abc_for(user_trait)

# Now use with isinstance for STRUCTURAL checking
assert issubclass(Customer, UserABC)  # True - has User structure
assert issubclass(Person, UserABC)    # True - has User structure

# Works with instances too
customer_instance = Customer(id=1, email="c@example.com", company="ACME")
assert isinstance(customer_instance, UserABC)  # True
```

## Key Concepts

1. **Structural Typing**: Duckdantic checks if objects have the required fields/methods, not if they inherit from specific classes.

2. **Type vs Instance**: When checking classes, it verifies field definitions. When checking instances, it looks at actual values.

3. **Dictionaries**: Plain dicts are treated as type mappings (field_name -> type), not as data instances.

4. **Validation vs Structure**: Duckdantic checks structure. For data validation, use Pydantic's built-in validation.

## Common Patterns

### Pattern 1: Interface Checking

```python
# Define an interface as a trait
interface = TraitSpec(
    name="Serializable",
    fields=[
        FieldSpec(name="to_dict", typ=callable, required=True),
        FieldSpec(name="from_dict", typ=callable, required=True),
    ]
)

# Check if classes implement the interface
assert satisfies(MyModel, interface)
```

### Pattern 2: Plugin Systems

```python
# Define required plugin structure
plugin_trait = TraitSpec(
    name="Plugin",
    fields=[
        FieldSpec(name="name", typ=str, required=True),
        FieldSpec(name="version", typ=str, required=True),
        FieldSpec(name="execute", typ=callable, required=True),
    ]
)

# Validate plugins
def load_plugin(plugin_class):
    if not satisfies(plugin_class, plugin_trait):
        raise TypeError("Invalid plugin structure")
    return plugin_class()
```

### Pattern 3: API Response Validation

```python
# Define expected API response structure
response_trait = TraitSpec(
    name="APIResponse",
    fields=[
        FieldSpec(name="status", typ=str, required=True),
        FieldSpec(name="data", typ=dict, required=True),
        FieldSpec(name="error", typ=str, required=False),
    ]
)

# Check if response matches expected structure
def handle_response(response_class):
    if satisfies(response_class, response_trait):
        # We know the response has the right structure
        return response_class.model_validate(api_data)
```

## Advanced Usage

### Custom Type Checking

```python
from duckdantic import TypeCompatPolicy

# Strict policy - exact type matches only
strict = TypeCompatPolicy(
    allow_subclass=False,
    numeric_widening=False,
)

# Check with strict policy
assert not satisfies(Customer, user_trait, strict)  # False - has extra fields

# Relaxed policy - allow numeric widening
relaxed = TypeCompatPolicy(
    numeric_widening=True,  # int -> float OK
)
```

### Trait Algebra

```python
from duckdantic import union, intersect, minus

# Combine traits
base_trait = TraitSpec(name="Base", fields=[
    FieldSpec(name="id", typ=int, required=True),
])

extended_trait = TraitSpec(name="Extended", fields=[
    FieldSpec(name="id", typ=int, required=True),
    FieldSpec(name="name", typ=str, required=True),
])

# Union - accepts either
flexible = union(base_trait, extended_trait)

# Intersection - requires both
strict = intersect(base_trait, extended_trait)

# Subtraction - remove fields
minimal = minus(extended_trait, ["name"])
```

### Registry Pattern

```python
from duckdantic import TraitRegistry

registry = TraitRegistry()

# Register traits
registry.add("User", user_trait)
registry.add("Admin", admin_trait)

# Find compatible traits
class Employee:
    id: int
    email: str
    department: str

compatible = registry.compatible_traits(Employee)
print(f"Employee satisfies: {compatible}")  # ['User']
```
