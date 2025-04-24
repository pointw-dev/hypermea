from pydantic import BaseModel


class ResourceModel(BaseModel):

    @classmethod
    def singplu(cls):
        singular = cls.__name__.lower()
        plural = getattr(getattr(cls, 'Config', object), 'plural', singular)
        return singular, plural

    @classmethod
    def from_hal(cls, data: dict) -> 'ResourceModel':
        """
        Construct an instance of this model from a HAL response.
        Filters out HAL metadata (_id, _etag, _created, _updated, _links).
        """
        filtered = {
            k: v for k, v in data.items()
            if not k.startswith('_') or k in cls.model_fields  # allow _id if explicitly defined
        }
        return cls.model_validate(filtered)
