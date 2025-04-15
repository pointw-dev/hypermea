from pydantic import BaseModel


class ResourceModel(BaseModel):

    @classmethod
    def singplu(cls):
        singular = cls.__name__.lower()
        plural = getattr(getattr(cls, "Config", object), "plural", singular)
        return singular, plural
