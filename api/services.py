"""API business logic."""
from typing import List
import pymongo

from db import settings


def get_rent_house_list(**kwargs) -> List[dict]:
    """
    Get rent house info by query.

    Parameters
    ----------
    sex_limit: int
    phone_number: str
    city: str
    renter_sex: str
    home_owner: bool
    first_name: str

    """
    client = pymongo.MongoClient(settings.MONGO_URI)
    db_name = settings.MONGO_DATABASE
    pass
