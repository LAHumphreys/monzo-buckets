import json
from typing import List
from abc import ABC, abstractmethod


class JSONInterface(ABC):
    _custom_list_fields = []
    _items: List["JSONInterface"] = []

    def _get_item_names(self):
        return [item for item in dir(self) if not item.startswith("_") and item != "parse_json_string_into_object"]

    def parse_json_string_into_object(self, json_string: str):
        return self._load(json_string)

    @abstractmethod
    def _load(self, json_response: str):
        raise NotImplemented

    @abstractmethod
    def _get_item_map(self):
        raise NotImplemented

    def _is_custom_list_field(self, name):
        is_custom_list: bool = False
        if name in self._custom_list_fields:
            is_custom_list = True
        return is_custom_list


class JSONObject(JSONInterface):

    def _load(self, json_response):
        self._raw_json = json_response
        for item in self._get_item_names():
            self.__setattr__(item, self._parse_item(item, json_response))

    def _parse_item(self, name, json_response):
        value = None
        if name in json_response:
            value = json_response[name]

        if value is not None and self._is_custom_list_field(name):
            parser = make_array(self._custom_list_fields[name])
            parser._load(value)
            value = parser._items

        return value

    def _get_item_map(self):
        result = {}
        for item in self._get_item_names():
            value = self.__getattribute__(item)
            if self._is_custom_list_field(item):
                encoded_values: List[JSONInterface] = value
                value = []
                for encoded_item in encoded_values:
                    value.append(encoded_item._get_item_map())
            elif isinstance(value, JSONObject):
                value = value._get_item_map()
            result[item] = value
        return result

    def __str__(self):
        return json.dumps(self._get_item_map())

    def __repr__(self):
        return "<JSONObject>\n" + self.__str__() + "\n</JSONObject>"


class JSONObjectArray(JSONObject):
    def __init__(self, item):
        self._item_class = item

    def _load(self, json_list):
        self._items = []
        for obj in json_list:
            item: JSONInterface = self._item_class()
            item._load(obj)
            self._items.append(item)

    def _get_item_map(self):
        result = []
        for item in self._items:
            result.append(item._get_item_map())
        return result


def make_scalar(source) -> JSONInterface:
    class Derived(JSONObject, source):
        pass
    return Derived()


def make_array(source) -> JSONInterface:
    class Derived(JSONObjectArray):
        def __init__(self):
            super().__init__(make_scalar(source))
    return Derived()
