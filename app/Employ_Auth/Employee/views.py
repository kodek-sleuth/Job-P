import json
from app import *
from Models.portal import *
from flask.views import MethodView
from flask import current_app, Blueprint

emp_auth=Blueprint('emp_auth', __name__)

#Creating Class based views for Registration, Login and Logout as well as The Token
class RegistrationView(MethodView):
    def post(self):
        try:
            request_data = request.get_json(force=True)
            name=request_data["Name"]
            username=request_data["Username"]
            email=request_data["Email"]
            password=request_data["Password"]
            country=request_data["Country"]
            main_stack=request_data["Main Expertise"]
            other_stacks=request_data["Other Skills"]
            work_status = request_data["Work Status"]
            dev_bio = request_data["Developer Biography"]

            try:
                emp=Employee.query.filter(username=username).first()
                if emp:
                    response={
                        "Message":"An account already exists with that Employee name"
                    }
                    return make_response(jsonify(response)), 409
                
                elif '~!@#$%&*():;+=-/' in username:
                    response={
                        "Message":"Employee can only have Letters and numbers at the end"
                        }
                    
                    return make_response(jsonify(response)), 401

            except:
                Employee.addEmployee(name, username, email, password, work_status, country, main_stack, other_stacks, dev_bio)
                response={
                        "Message":"You have successfully Created an Employee account"
                    }
                return make_response(jsonify(response)), 201
    
        except:
            response={
                "Message":"Please Enter valid Credentials"
            }
            return make_response(jsonify(response)), 409

class LoginView(MethodView):
    def post(self):
        try:
            request_data = request.get_json(force=True)
            emp=Employee.query.filter_by(username=request_data["Username"]).first()
            if emp.username==request_data["Username"] and emp.password==request_data["Password"]:
                response={
                    "Message":"You have successfully Logged In"
                }
                
                return make_response(jsonify(response)), 201
            
            elif emp.password!=request_data["Password"]:
                response={
                    "Message":"Invalid Password"
                }
                return make_response(jsonify(response)), 401
            
            elif emp.username!=request_data["Username"]:
                response={
                    "Message":"Invalid username"
                }
                return make_response(jsonify(response)), 401
                
        
        except:
            response={
                "Message":"Try checking Your Credentials and Try again"
            }
            return make_response(jsonify(response)), 401


class UpdateView(MethodView):
    def put(self, username):
        try:
            check_user = Employee.query.filter_by(username=username).first()
            if check_user:
                request_data=request.get_json(force=True)

                if 'Username' in request_data and 'Name' in request_data and 'Main Expertise' in request_data and 'Developer Biography' in request_data and 'Other Skills' in request_data and 'Password' in request_data and 'Country' in request_data and 'Email' in request_data and 'Work Status' in request_data:
                    
                    username=request_data['Username']
                    name = request_data['Name']
                    password=request_data['Password']
                    main_stack=request_data['Main Expertise']
                    country=request_data['Country']
                    work_status=request_data['Work Status']
                    other_stacks=request_data['Other Skills']
                    email=request_data['Email']
                    dev_biography=request_data['Developer Biography']
                
                    check_user.username=username
                    check_user.name=name
                    check_user.password=password
                    check_user.main_stack=main_stack
                    check_user.country=country
                    check_user.work_status=work_status
                    check_user.other_stacks=other_stacks
                    check_user.email=email
                    check_user.dev_biography=dev_biography
                    
                    
                    db.session.commit()
                    
                    response={
                        "Message": "Successfully Updated Profile"
                    }
                    return make_response(jsonify(response)), 200

                
        except:
            response={
                "Message":"Failed To Update Information"
            }





#Creating View Function/Resources
registrationview=RegistrationView.as_view('registrationview')
loginview=LoginView.as_view('loginview')
updateview=UpdateView.as_view('updateview')

#adding routes to the Views we just created
emp_auth.add_url_rule('/employee/signup', view_func=registrationview, methods=['POST'])
emp_auth.add_url_rule('/employee/login', view_func=loginview, methods=['POST'])
emp_auth.add_url_rule('/employee/<string:username>/update', view_func=updateview, methods=['PUT'])
