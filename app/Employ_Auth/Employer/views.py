import json
from app import *
from Models.portal import *
from flask.views import MethodView
from flask import current_app, Blueprint

empl_auth=Blueprint('empl_auth', __name__)

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
            company=request_data["Company"]
            dev_bio = request_data["Company Biography"]

            try:
                emp=Employee.query.filter(username=username).first()
                if emp:
                    response={
                        "Message":"An account already exists with that Employer name"
                    }
                    return make_response(jsonify(response)), 202
                
                elif '~!@#$%&*():;+=-/' in username:
                    response={
                        "Message":"Employee can only have Letters and numbers at the end"
                        }
                    
                    return make_response(jsonify(response)), 401

            except:
                Employer.addEmployer(name, username, email, password, dev_bio, company, country)
                response={
                        "Message":"You have successfully Created an Employer account"
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
            emp=Employer.query.filter_by(username=request_data["Username"]).first()
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
            check_user = Employer.query.filter_by(username=username).first()
            if check_user:
                request_data=request.get_json(force=True)

                if 'Username' in request_data and 'Name' in request_data and 'Company' in request_data and 'Company Biography' in request_data and 'Password' in request_data and 'Country' in request_data and 'Email' in request_data:
                    
                    username=request_data['Username']
                    name = request_data['Name']
                    password=request_data['Password']
                    company=request_data['Company']
                    country=request_data['Country']
                    email=request_data['Email']
                    dev_biography=request_data['Company Biography']
                
                    check_user.username=username
                    check_user.name=name
                    check_user.password=password
                    check_user.company=company
                    check_user.country=country
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
empl_auth.add_url_rule('/employer/signup', view_func=registrationview, methods=['POST'])
empl_auth.add_url_rule('/employer/login', view_func=loginview, methods=['POST'])
empl_auth.add_url_rule('/employer/<string:username>/update', view_func=updateview, methods=['PUT'])
