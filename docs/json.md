# JSON Support

the SDK supports converting most dataclasses and `BaseList`s of dataclasses to JSON. This is done using the `to_serializable_dict` and `to_serializable_list` methods, respectively. These methods convert the dataclass or `BaseList` to a dictionary or list of dictionaries. There is also the `dump_json` method, which is essentially the SDK's version of `json.dumps`. The reason for these methods is to provide a consistent way to convert dataclasses and `BaseList`s to JSON, as the standard `json` module often conflicts with some of the data types used in the SDK, mainly those from the `datetime` and `ipaddress` modules.

| Method | Description |
|--|--|
| `<dataclass>.to_serializable_dict` | Converts a dataclass to a JSON-serializable dictionary. |
| `<BaseList>.to_serializable_list` | Converts a `BaseList` of dataclasses to a JSON-serializable list of dictionaries. |
| `<dataclass or BaseList>.dump_json` | Converts a dataclass or `BaseList` to a JSON string. |