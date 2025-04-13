from pydantic import BaseModel, field_validator, model_validator
from typing import Literal

class Relation(BaseModel):
    parent: str
    child: str
    rel: str | None = None
    reverse: str | None = None
    collection_name: str | None = None
    parent_is_external: bool = False
    child_is_external: bool = False

    def model_post_init(self, __context):
        if self.rel is None:
            self.rel = self.parent
        if self.collection_name is None:
            self.collection_name = f"{self.parent}_{self.child}"

    @property
    def has_external_relation(self) -> bool:
        return self.parent_is_external or self.child_is_external

    @classmethod
    def from_link_command(cls, parent: str, child: str):
        parent_is_external = parent.startswith("external:")
        child_is_external = child.startswith("external:")

        clean_parent = parent.replace("external:", "")
        clean_child = child.replace("external:", "")

        return cls(
            parent=clean_parent,
            child=clean_child,
            parent_is_external=parent_is_external,
            child_is_external=child_is_external
        )

    @model_validator(mode="after")
    def check_only_one_external(cls, values):
        if values.parent_is_external and values.child_is_external:
            raise ValueError("Only one of parent or child may be external, not both.")
        return values
