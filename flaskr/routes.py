from flask import (
    Blueprint,request, Response, json
)
from . import functions
from  werkzeug.utils import secure_filename



bp = Blueprint('routes', __name__)

@bp.route('/', methods=['GET'])
def general():
    return "Testing"

@bp.route('/text',methods=['GET','POST'])
def default():
    data ={
        "msg" : "Please use the post method to submit an audio file"
    }
    if request.method == 'POST':
        data = functions.check_post(request)

    response =Response(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response

@bp.route('/text/<language>',methods=['GET','POST'])
def custom_language(language):
    data ={
        "msg" : "Please use the post method to submit an audio file"
    }
    if request.method == 'POST':
        accepted_languages = ["en-US","en-UK","fr-FR","nl-NL"]
        if(language not in accepted_languages ):
            data["msg"] = "Failed"
            data["error"] = "This language is not accepted"
        else:
            data = functions.check_post(request,language)

    response =Response(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return response
