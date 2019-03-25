import json
from app import *
from Models.portal import *
from flask.views import MethodView
from flask import current_app, Blueprint

jobs_auth=Blueprint('jobs_auth', __name__)

class Post_Job(MethodView):
    def post(self, username):
        try:
            request_data = request.get_json(force=True)
            title=request_data["Job Title"]
            description=request_data["Job Description"]
            main_stack=request_data["Main Skill"]
            other_stacks=request_data["Other Skills"]
            job_type=request_data["Job Type"]

            check_username = Employer.query.filter_by(username=username).first()
            emp = JobsEmployer.addJob(title, description, main_stack, other_stacks, job_type, check_username.id)
            response={
                        "Message":"You have successfully Posted Job"
                }
            return make_response(jsonify(response)), 201

        except:
            response={
                        "Message":"Invalid Credentials, Please enter Title, Description, Main Skill, Other Skills and Job Type"
                }
            return make_response(jsonify(response)), 401

class Apply_Job(MethodView):
    def post(self, username):
        try:
            request_data = request.get_json(force=True)
            title=request_data["Job Title"]
            main_stack=request_data["Main Skill"]

            check_username = Employee.query.filter_by(username=username).first()
            JobsEmployees.addJobEmp(title, main_stack, check_username.id)
            response={
                        "Message":"You Have Successfully Applied For This Job"
                }
            return make_response(jsonify(response)), 201

        
        except:
            response={
                        "Message":"Invalid Credentials, Please enter Job Title and Main Skill"
                }
            return make_response(jsonify(response)), 401

#
post_job=Post_Job.as_view('Post_Job')
apply_job=Apply_Job.as_view('Apply_Job')

#adding routes to the Views we just created
jobs_auth.add_url_rule('/user/<string:username>/post', view_func=post_job, methods=['POST'])
jobs_auth.add_url_rule('/user/<string:username>/apply', view_func=apply_job, methods=['POST'])


