"""
JobResultSummary data class
"""

from dataclasses import dataclass
from typing import Union
from datetime import datetime

from .PMAsset import PMAssetJobView
from ...base.base_list import BaseList
from ...base.base_class import BaseClass


@dataclass
class JobResultSummary(BaseClass):
    """
    Represents a job result summary in Patch Management.
    """

    id: str = None
    name: str = None
    assetCount: int = None
    patchCount: int = None
    createdBy: str = None
    createdOn: Union[int, datetime] = None
    assets: BaseList[PMAssetJobView] = None

    def __post_init__(self):
        if self.createdOn:
            setattr(self, "createdOn", datetime.fromtimestamp(self.createdOn / 1000))

        if self.assets:
            bl = BaseList()
            for asset in self.assets:
                asset_dict = dict()
                for key, value in asset.items():
                    if key == "asset":
                        asset_dict.update(value)
                    else:
                        asset_dict[key] = value

                asset_dict["jobId"] = self.id
                bl.append(PMAssetJobView.from_dict(asset_dict))
            setattr(self, "assets", bl)

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)
