import datetime
import jwt, requests
from flask_cors import CORS
from flasgger import Swagger, swag_from
from flask_sqlalchemy import SQLAlchemy
from Settings.config import app_config
from flask import Flask, request, jsonify, make_response, redirect

db = SQLAlchemy()

def create_app(config_name):
    app=Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config['SWAGGER'] = {
        'swagger': '2.0',
        'title': 'FoodHub Delivery-API',
        'description': "The innovative Job-Portal API is an application that allows\
        Programming Job Seekers to find jobs worlwide from a variety of Jobs and for Employers to get Employees\
        \nThis is a RESTful API built in python using the Flask Framework.\
        \nGitHub Repository: 'https://github.com/kodek-sleuth/Job-Portal-API'",
        'basePath': '/',
        'version': '0.1.0',
        'contact': {
            'Developer': 'Mugerwa Joseph Lumu',
            'email': 'mugerwalumu@gmail.com',
            'Company': 'None'
        },

        'schemes': [
            'http',
            'https'
        ],

        'license': {
            'name': 'MIT'
        },

        'tags': [
            {
                'name': 'Job Seeker',
                'description': 'Showcasing different routes taken by the Job Seeker'
            },
            {
                'name': 'Employer',
                'description': 'Showcasing different routes taken by the Employer'
            },
            {
                'name': 'Jobs',
                'description': 'A User can choose from here all types of food'
            },
        
        ],

        'specs_route': '/apidocs/'
    }

    from app.Routes.Employee.views import emp_auth
    app.register_blueprint(emp_auth)
    
    db.init_app(app) 
    CORS(app)
    swagger=Swagger(app)

    @app.route('/')
    def index():
        return redirect('/apidocs/')

    return app
