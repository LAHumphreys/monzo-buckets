import json

class JSONObject:
    def _load(self, json_response):
        self._raw_json = json_response
        for item in self._get_item_names():
            self.__setattr__(item, self._parse_item(item, json_response))

    def _parse_item(self, name, json_response):
        value = None
        if name in json_response:
            value = json_response[name]

        if value is not None and self._is_custom_list_field(name):
            parser = make_array(self._custom_list_fields[name])()
            parser._load(value)
            value = parser._items

        return value

    def _is_custom_list_field(self, name):
        is_cust_list = False
        if hasattr(self, "_custom_list_fields") and name in self._custom_list_fields:
            is_cust_list = True
        return  is_cust_list

    def _get_item_names(self):
        return [item for item in dir(self) if not item.startswith("_")]

    def _get_item_map(self):
        result = {}
        for item in self._get_item_names():
            value = self.__getattribute__(item)
            if self._is_custom_list_field(item):
                encoded_values = value
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
    def __init__(self, Item):
        self._Item = Item
        self._items = []

    def _load(self, json_list):
        self._items = []
        for obj in json_list:
            item = self._Item()
            item._load(obj)
            self._items.append(item)

    def _get_item_map(self):
        result = []
        for item in self._items:
            result.append(item._get_item_map())
        return result


def make_scalar(Source) -> JSONObject:
    class Derived(JSONObject, Source):
        pass
    return Derived

def make_array(Source) -> JSONObjectArray:
    class Derived(JSONObjectArray):
        def __init__(self):
            super().__init__(make_scalar(Source))
    return Derived
