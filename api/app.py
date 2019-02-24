"""API endpoint."""
from flask import (
    Flask,
    jsonify,
    request,
)
from services import get_rent_house_list

app = Flask(__name__)


@app.route("/rent")
def rent():
    """Rent API endpoint."""
    params = request.args.to_dict()
    # check params field
    field_type = {
        'sex_limit': int,
        'phone_number': str,
        'city': str,
        'renter_sex': int,
        'home_owner': int,
        'first_name': str
    }
    for key in params.keys():
        if key not in field_type.keys():
            raise KeyError
        try:
            params[key] = field_type[key](params[key])
        except Exception:
            raise ValueError

    rent_list = get_rent_house_list(**params)
    return jsonify({
        'data': rent_list
    })
