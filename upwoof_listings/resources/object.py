import json
from datetime import datetime
from dateutil import parser
from typing import Any, Dict, List, Optional, Union

class Serializer:
    @staticmethod
    def serialize(value: Any) -> Any:
        return str(value)

    @staticmethod
    def deserialize(value: Any) -> Any:
        if isinstance(value, list):
            return [Serializer.deserialize(v) if isinstance(v, (list, dict)) else v for v in value]
        elif isinstance(value, dict):
            return {k.lower(): (Serializer.deserialize(v) if isinstance(v, (list, dict)) else v) for k, v in value.items()}
        return value

class TimeSerializer:
    @staticmethod
    def serialize(value: datetime) -> str:
        return value.isoformat()

    @staticmethod
    def deserialize(value: str) -> datetime:
        return parser.parse(value)

class ResourceObject:
    _attributes = {
        'date_created_utc': TimeSerializer,
        'date_updated_utc': TimeSerializer
    }

    def __init__(self, data: Dict[str, Any]):
        self._data = {k.upper(): v for k, v in data.items()}

    def __getattr__(self, name: str) -> Any:
        upper_name = name.upper()
        if upper_name in self._data:
            value = self._data[upper_name]
            serializer = self._get_serializer(name)
            return serializer.deserialize(value)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def _get_serializer(self, name: str):
        # In Ruby, it's quite dynamic. We'll simplify a bit but keep it extensible.
        return self._attributes.get(name, Serializer)

    @classmethod
    def parse(cls, response: Any) -> Union['ResourceObject', List['ResourceObject'], None]:
        if not response:
            raise ValueError("Response cannot be blank")
        
        data = response.json()
        if isinstance(data, list):
            return [cls(item) for item in data]
        elif isinstance(data, dict):
            return cls(data)
        return None

    def serialize(self) -> Dict[str, Any]:
        result = {}
        for name, serializer in self._attributes.items():
            upper_name = name.upper()
            if upper_name in self._data:
                result[upper_name] = serializer.serialize(getattr(self, name))
        return result

    def __repr__(self) -> str:
        attrs = " ".join([f"{k}={getattr(self, k)!r}" for k in self._attributes if hasattr(self, k)])
        return f"<{self.__class__.__name__} {attrs}>"
