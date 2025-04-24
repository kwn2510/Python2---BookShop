from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:25102004@localhost:5432/Book Shop'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

def main():
    Invoice_Details.__table__.create(db.engine)
    #db.create_all()
    
if __name__ == '__main__':
    with app.app_context():
        main()