from pydantic import BaseModel

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

    def __len__(self) -> int:
        return len(self.name)

    def isidentifier(self):
        return self.name.isidentifier()


def external(name: str) -> ResourceRef:
    """Helper to declare an external resource reference with minimal syntax."""
    return ResourceRef(name=name, external=True)


def local(name: str) -> ResourceRef:
    """Helper to declare a local resource reference with minimal syntax."""
    return ResourceRef(name=name, external=False)
