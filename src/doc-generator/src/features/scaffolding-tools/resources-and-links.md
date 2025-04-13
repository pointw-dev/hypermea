# Getting Started with `ResourceModel` in Hypermea

In **hypermea**, a `ResourceModel` defines a resource using a familiar `pydantic` class structure, and is automatically translated into a Cerberus-compatible schema for Eve. This gives you the power of static typing, validation, and code completion — while hypermea handles the hard part of rendering and linking at runtime.

---

## 🧱 Basic Structure

To define a new resource, inherit from `ResourceModel`:

```python
from hypermea import ResourceModel

class Car(ResourceModel):
    make: str
    model: str
    year: int
```

This automatically creates a resource called `car` with the appropriate schema and default REST routes.

---

## 🔁 Customizing Resource Behavior

### 🔹 `Config.plural`

You may define the collection name explicitly:

```python
class Car(ResourceModel):
    make: str

    class Config:
        plural = "cars"
```

If omitted, the plural will default to `car` (i.e. no transformation). We recommend setting this explicitly to avoid naming collisions and clarify developer intent.

### 🔹 `Config.link_rel`

Overrides the default link relation used in hypermedia responses:

```python
class Car(ResourceModel):
    make: str

    class Config:
        link_rel = "vehicle"
```

---

## 🔍 Supported Field Features

### ✅ Standard Types

Fields of these types are supported and automatically mapped:

- `str`, `int`, `float`, `bool`
- `datetime`, `date`, `time`
- `list[...]`, `dict`, `Literal[...]`

### ✅ Validation Rules

Pydantic field constraints are translated into Cerberus rules, including:

- `min_length`, `max_length` → `minlength`, `maxlength`
- `ge`, `le` → `min`, `max`
- `const`, `enum` → `allowed`
- `multiple_of`, `pattern` → `multipleof`, `regex`

Example:

```python
from pydantic import Field
from typing import Literal

class License(ResourceModel):
    type: Literal["trial", "full"] = "trial"
    key: str = Field(..., min_length=10, max_length=64)
```

---

## 🔗 Linking Resources

Hypermea supports subresources (like Eve’s “sub-documents”) via a centralized registry:

```python
from hypermea.link import Link

LINKS = [
    Link("person", "car"),
    Link("organization", "license", rel="owns"),
]
```

You don’t declare these links inside your models. Instead, they live in a shared file like `domain/links.py`, keeping links as first-class entities.

Each `Link` object can define:

- `parent`, `child`: the resource pair
- `rel`: the name of the link in the child’s `_links` object (defaults to the parent name)
- `collection_name`: optional override of the subresource name (default: `parent_child`)

Hypermea handles:
- Creating the subresource schema and projection
- Injecting it into `config['DOMAIN']`
- Linking and HAL compliance

---

## ✅ What Hypermea Does for You

- Converts `ResourceModel` classes into Eve resources
- Enforces and enriches validation rules automatically
- Manages singular/plural naming with developer intent
- Supports embedded/nested models and lists
- Keeps link logic out of your models and into a structured registry

---

## 🧪 Next Steps

- Try defining two resources and linking them with `hy link create parent child`
- Override `plural` and `link_rel` to control URL and hypermedia affordances
- Nest models using `BaseModel` classes inside fields for structured objects

---

## 🧠 Coming Soon

Planned enhancements include:
- Support for `Annotated[...]` fields
- Class-level control over permissions and behavior (`Config.resource_methods`, etc.)
- Many-to-many links and link-as-resource patterns

Stay tuned, and keep your models clean. Hypermea will do the rest.
