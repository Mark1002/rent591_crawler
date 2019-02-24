"""API endpoint."""
from flask import (
    Flask,
    jsonify,
    request,
)

from services import get_rent_house_list
import exceptions

app = Flask(__name__)


def check_param_format(field_type, params):
    """Check param format."""
    for key in params.keys():
        if key not in field_type.keys():
            raise exceptions.FormatError(
                f"'{key}' is not a valid param."
            )
        try:
            params[key] = field_type[key](params[key])
        except Exception:
            raise exceptions.FormatError(
                f"value of param '{key}' is not valid."
            )


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
    check_param_format(field_type, params)
    rent_list = get_rent_house_list(**params)
    return jsonify({
        'data': rent_list
    })


@app.errorhandler(exceptions.FormatError)
def handle_error_response(error):
    """Exception response."""
    response = jsonify({
        'status_code': error.status_code,
        'message': error.message
    })
    response.status_code = error.status_code
    return response
