from app import create_app, db
from Models.portal import *

app = create_app('development')

if __name__=='__main__':
    app.run(debug=True, port=3000)