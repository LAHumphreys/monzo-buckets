# pylint: disable=no-self-use, protected-access
import json
from typing import List
from abc import ABC, abstractmethod


class JSONTypeError(Exception):
    pass


class JSONInterface(ABC):
    _raw_json: dict = None
    _custom_list_fields = []
    _items: List["JSONInterface"] = []
    _public_methods = ["parse_json_string_into_object", "parse_json_string_into_array"]

    def _get_item_names(self) -> List[str]:
        item_names = []
        for item in dir(self):
            if not item.startswith("_") and item not in self._public_methods:
                item_names.append(item)
        return item_names

    @abstractmethod
    def _get_item_map(self):
        raise NotImplementedError

    def _is_custom_list_field(self, name):
        is_custom_list: bool = False
        if name in self._custom_list_fields:
            is_custom_list = True
        return is_custom_list


class JSONObject(JSONInterface):

    def parse_json_string_into_object(self, json_response: dict):
        self._raw_json = json_response
        for item in self._get_item_names():
            self.__setattr__(item, self._parse_item(item, json_response))

    def _parse_item(self, name, json_response):
        value = None
        if name in json_response:
            value = json_response[name]

        if value is not None and self._is_custom_list_field(name):
            parser = make_array(self._custom_list_fields[name])
            parser.parse_json_string_into_array(value)
            value = parser.get_items()

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
        self._public_methods.append("get_items")

    def parse_json_string_into_array(self, json_list: list):
        self._items = []
        for obj in json_list:
            item: JSONObject = self._item_class()
            item.parse_json_string_into_object(obj)
            self._items.append(item)

    def _get_item_map(self):
        result = []
        for item in self._items:
            result.append(item._get_item_map())
        return result

    def get_items(self):
        return self._items


def make_scalar(source) -> JSONObject:
    class Derived(JSONObject, source):
        pass

    return Derived()


def make_array(source) -> JSONObjectArray:
    class Derived(JSONObjectArray):
        def __init__(self):
            super().__init__(make_scalar(source).__class__)

    return Derived()
