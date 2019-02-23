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

    cursor = client[db_name]['rents'].find(kwargs)
    rent_list = [{
        'house_id': rent['house_id'],
        'house_type': rent['house_type'],
        'house_recent': rent['house_recent'],
        'city': rent['city'],
        'renter': rent['renter'],
        'renter_type': rent['renter_type'],
        'renter_sex': rent['renter_sex'],
        'phone_number': rent['phone_number'],
        'sex_limit': rent['sex_limit']
    } for rent in cursor]
    # close db connection
    client.close()
    return rent_list
