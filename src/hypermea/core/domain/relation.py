from pydantic import BaseModel, model_validator
from typing import Union
from .resource_ref import ResourceRef, external, local


class Relation(BaseModel):
    parent: Union[str, ResourceRef]
    child: Union[str, ResourceRef]
    rel: str | None = None
    reverse: str | None = None

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

    @model_validator(mode="after")
    def check_external_exclusivity(self):
        if self.parent.external and self.child.external:
            raise ValueError("A relation cannot have both parent and child marked as external.")
        return self

    @property
    def is_cross_service(self) -> bool:
        return self.parent.external or self.child.external
