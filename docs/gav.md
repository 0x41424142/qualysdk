# Global AssetView APIs
Global AssetView APIs return data on hosts within your Qualys subscription. 
>**Pro Tip**: To see all available GAV QQL filters, look [here!](https://docs.qualys.com/en/gav/2.18.0.0/search/how_to_search.htm)

After running:
```py
from qualyspy.gav import *
```
You can any of the 4 GAV endpoints:

## GAV Endpoints
|API Call| Description |
|--|--|
| ```count_assets``` | Count assets based on the ```filter``` kwarg, which is written in Qualys QQL.|
```get_asset```|Get a specific host based on the ```assetId``` kwarg.|
```get_all_assets```| Pull the entire host inventory (or a few pages of it with ```page_count```), in file sizes of ```pageSize```. Does **NOT** support ```filter```.|
|```query_assets```| Scaled down version of```get_all_assets``` - pulls entire host inventory that matches the given ```filter``` kwarg.

Or use the uber class:
```py
from qualyspy import TokenAuth, GAVUber

#Hey look! context managers!
with TokenAuth(<username>, <password>, platform='qg1') as auth:
    with GAVUber(auth) as uber:
        full_inventory_count = uber.get("count_assets")
        ...
```

## The GAV Host Dataclass
>**Heads Up!**: The ```Host``` class does not apply to ```count_assets()```

When results are received from a GAV API, each host record is stored in a ```Host``` object, with its data points as attributes. The ```Host``` class is decorated with ```@dataclass(frozen=True)``` to maintain consistency with the Qualys platform.	

Chances are, there will be a good chunk of attributes returned from Qualys that will be null. To deal with this, almost all attributes are defined as ```typing.Optional[]```, with the main exception being ```assetId```. It is also somewhat likely that I have mistyped certain attributes, as both the Qualys documentation and the data I am working with to build this package return a decent amount of null values. Should you come across something, submit a PR.