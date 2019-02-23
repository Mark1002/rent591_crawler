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
    rent_list = get_rent_house_list(**params)
    return jsonify({
        'data': rent_list
    })
