from pydantic import BaseModel, model_validator
from typing import Union

class ResourceRef(BaseModel):
    name: str
    external: bool = False  # True means this resource is defined in another service

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, ResourceRef):
            return self.name == other.name and self.external == other.external
        return False

    def __contains__(self, item: str) -> bool:
        return item in self.name

    def __iter__(self):
        return iter(self.name)

def external(name: str) -> ResourceRef:
    """Helper to declare an external resource reference with minimal syntax."""
    return ResourceRef(name=name, external=True)

def local(name: str) -> ResourceRef:
    """Helper to declare a local resource reference with minimal syntax."""
    return ResourceRef(name=name, external=False)

class Relation(BaseModel):
    parent: Union[str, ResourceRef]
    child: Union[str, ResourceRef]
    rel: str | None = None
    reverse: str | None = None
    collection_name: str | None = None

    def model_post_init(self, __context):
        # Allow "external:" prefix in str-based shorthand
        if isinstance(self.parent, str):
            if self.parent.startswith("external:"):
                self.parent = external(self.parent.replace("external:", ""))
            else:
                self.parent = local(self.parent)

        if isinstance(self.child, str):
            if self.child.startswith("external:"):
                self.child = external(self.child.replace("external:", ""))
            else:
                self.child = local(self.child)

        if self.rel is None:
            self.rel = self.parent.name

        if self.collection_name is None:
            self.collection_name = f"{self.parent.name}_{self.child.name}"

    @model_validator(mode="after")
    def check_external_exclusivity(self):
        if self.parent.external and self.child.external:
            raise ValueError("A relation cannot have both parent and child marked as external.")
        return self

    @property
    def is_cross_service(self) -> bool:
        return self.parent.external or self.child.external
