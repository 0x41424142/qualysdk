# JSON Support

the SDK supports converting most dataclasses and `BaseList`s of dataclasses to JSON. This is done using the `to_serializable_dict` and `to_serializable_list` methods, respectively. These methods convert the dataclass or `BaseList` to a dictionary or list of dictionaries. There is also the `dump_json` method, which is essentially the SDK's version of `json.dumps`. The reason for these methods is to provide a consistent way to convert dataclasses and `BaseList`s to JSON, as the standard `json` module often conflicts with some of the data types used in the SDK, mainly those from the `datetime` and `ipaddress` modules.

| Method | Description |
|--|--|
| `<dataclass>.to_serializable_dict` | Converts a dataclass to a JSON-serializable dictionary. |
| `<BaseList>.to_serializable_list` | Converts a `BaseList` of dataclasses to a JSON-serializable list of dictionaries. |
| `<dataclass or BaseList>.dump_json` | Converts a dataclass or `BaseList` to a JSON string. |

## Dataclass Mutations

You can also control how dataclasses are parsed using the `qualysdk.DONT_EXPAND` singleton object. This is useful for controlling how the SDK parses certain dataclass attributes. Normally, the SDK will try to either create dataclass objects for any objects an API endpoint returns under a key or expand certain sub-keys to new attributes on the dataclass. For example, in the `WAS` module, ownership data for a `WebApp` is received from the API like:

```json
...
"owner": {
    "id": 123456,
    "username": "admin",
    "firstName": "Jane",
    "lastName": "Doe"
},
...
```

Normally, the SDK would create new attributes, prefixing them with `owner_`, and set them to the values of the keys in the `owner` object. So, the above example would be parsed as:

```python
WebApp(
    owner_id=123456,
    owner_username="admin",
    owner_firstName="Jane",
    owner_lastName="Doe"
)
```

However, by using:

```python
from qualysdk import DONT_EXPAND
DONT_EXPAND.flag = True
```

The SDK will not flatten the `owner` object, instead leaving it as it was received from the API. So, the above example would be parsed as:

```python
WebApp(
    owner={
        "id": 123456,
        "username": "admin",
        "firstName": "Jane",
        "lastName": "Doe"
    }
)
```

In SQL Server, this would look like:

```sql
SELECT 
    JSON_VALUE(owner, '$.id') AS id,
    JSON_VALUE(owner, '$.firstName') AS firstName
FROM 
    MY_WAS_JSON_TABLE
```

| id | firstName |
|--|--|
| 123456 | Jane |

This is mainly used for JSON exports, either to a file with `json.dump` or to a SQL database with `qualysdk.sql.upload_json`. By default, `DONT_EXPAND` is set to `False`, so the SDK will always try to expand dataclass attributes. This is done to make it easier to work with the SDK, as it is often easier to work with flat dataclasses than nested ones. However, if you want to keep the structure as close to the API response as possible, you can set `DONT_EXPAND` to `True`.