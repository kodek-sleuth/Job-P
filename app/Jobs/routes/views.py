import json
from app import *
from Models.portal import *
from flask.views import MethodView
from flask import current_app, Blueprint

jobs = Blueprint('jobs', __name__)

@jobs.route('/coders/<string:stack>/', methods=['GET'])
def get_applicant_by_stack(stack):
    emp = Employee.query.filter_by(main_stack=stack).first()
    empToStr = str(emp)
    empToJson=json.loads(empToStr)

    return make_response(jsonify(empToJson))


@jobs.route('/user/<string:username>/applied', methods=['GET'])
def get_jobs_applied(username):
    try:
        emp = Employee.query.filter_by(username=username).first()
        empToStr = str(emp.job_applicants)
        toJson = json.loads(empToStr)

        return make_response(jsonify(toJson)), 200
    
    except:
        response={
            "Message": "Login or SignUp to use This service"
        }

        return make_response(jsonify(response)), 500


@jobs.route('/user/<string:username>/posted', methods=['POST'])
def get_jobs_posted(username):
    try:
        emp = Employer.query.filter_by(username=username).first()
        empToStr = str(emp.jobs_of_employer)
        toJson = json.loads(empToStr)

        return make_response(jsonify(toJson)), 200
    
    except:
        response={
            "Message": "Login or SignUp to use This service"
        }

        return make_response(jsonify(response)), 500

@jobs.route('/users/<string:username>/inbox', methods=['GET'])
def get_inbox(username):
    try:
        emp = Employee.query.filter_by(username=username).first()
        empToStr = str(emp.inbox)
        toJson = json.loads(empToStr)

        return make_response(jsonify(toJson)), 200
    
    except:
        response={
            "Message": "Login or SignUp to use This service"
        }

        return make_response(jsonify(response)), 500

@jobs.route('/users', methods=['GET'])
def get_employees():
    emp = Employee.query.all()
    empToStr = str(emp)
    toJson = json.loads(empToStr)
    return make_response(jsonify(toJson)), 200

@jobs.route('/user/<string:employee_username>/inbox', methods=['POST'])
def send_Message(employee_username):
    try:
        request_data = request.get_json(force=True)
        username = request_data['Username']
        subject = request_data['Subject']
        description = request_data['Description']

        check_employee = Employee.query.filter_by(username=employee_username).first()
        check_employer = Employer.query.filter_by(username=username).first()

        if check_employee and check_employer:
            Inbox.sendMessage(check_employer.username, subject, description, check_employee.id, check_employer.id)
            response={
                "Message": "Successfully Sent Message"
            }

            return make_response(jsonify(response)), 200





    
    except:
        response={
            "Message": "Please Enter Valid Credentials"
        }

