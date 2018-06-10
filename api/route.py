from flask import Blueprint, request, jsonify
from datetime import datetime
from api.models import CompanyProfile, FinancialSummary
from api.app import db
from werkzeug.exceptions import BadRequest

# Blueprint init
data = Blueprint('data', __name__)


# Error handler
@data.errorhandler(BadRequest)
def handle_bad_request(e):
    response = {
        "status_code": 400,
        "message": "Failed, bad query params",
    }

    return jsonify(response), 400


# endpoint for companies
@data.route('/companies', methods=['GET'])
def get_companies():
    req_data = request.args

    # check request with params
    if req_data:
        if req_data.get('company_name'):
            data = db.session.query(CompanyProfile)\
                .filter(CompanyProfile.company_name == req_data['company_name'])    
        elif req_data.get('industry'):
            data = db.session.query(CompanyProfile)\
                .filter(CompanyProfile.industry == req_data['industry'])
        elif req_data.get('revenue_gte'):
            data = db.session.query(CompanyProfile)\
                .outerjoin(FinancialSummary)\
                .filter(FinancialSummary.market_cap >= req_data['revenue_gte'])
        else:
            raise BadRequest()
    else:
        data = db.session.query(CompanyProfile)

    # jsonify result
    result = []
    for i in data:
        cp = i.__dict__
        
        # clean dict
        del cp['_sa_instance_state']

        result.append(cp)

    response = {
        "status_code": 200,
        "message": "successful",
        "data": result
    }

    return jsonify(response)