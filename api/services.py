"""API business logic."""
from typing import List
import pymongo
from db import settings


def get_rent_house_list(**kwargs) -> List[dict]:
    """
    Get rent house info by query.

    Parameters
    ----------
    sex_limit: int (0/male, 1/female, 2/both)
    phone_number: str
    city: str
    renter_sex: int (0/male, 1/female)
    home_owner: int (0/not home owner, 1/home owner)
    first_name: str

    """
    client = pymongo.MongoClient(settings.MONGO_URI)
    db_name = settings.MONGO_DATABASE

    if 'home_owner' in kwargs.keys():
        is_home_owner = bool(kwargs.pop('home_owner'))
        if is_home_owner:
            kwargs['renter_type'] = '屋主'
        else:
            kwargs['renter_type'] = {'$ne': '屋主'}

    if 'first_name' in kwargs.keys():
        first_name = kwargs.pop('first_name')
        kwargs['renter'] = {'$regex': first_name}

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
