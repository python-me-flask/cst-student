import csv

from flask import Flask
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    branch = db.Column(db.String(80), unique=False, nullable=False)
    college = db.Column(db.String(80), unique=False, nullable=False)
    batch = db.Column(db.String(80), unique=False, nullable=False)
    program = db.Column(db.String(80), unique=False, nullable=False)
    course = db.Column(db.String(80), unique=False, nullable=False)
    f_lang = db.Column(db.String(80), unique=False, nullable=False)

    def __init__(self, id, name, branch, college, batch, program, course, f_lang):
        self.id = id
        self.name = name
        self.branch = branch
        self.college = college
        self.batch = batch
        self.program = program
        self.course = course
        self.f_lang = f_lang

    def json(self):
        return {'ID': self.id, 'Name': self.name, 'Branch': self.branch, 'College': self.college, 'Batch': self.batch,
                'Program': self.program, 'Course': self.course, 'First Language': self.f_lang}

    @classmethod
    def find_all(cls, title):
        return cls.query.all()

    def save_to(self):
        db.session.add(self)
        db.session.commit()

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True


db.init_app(app)
app.app_context().push()
db.reflect()
db.drop_all()
db.create_all()




with open('data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        std = Student(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        std.save_to()


class main(Resource):
    def get(self):
        return list(map(lambda x: x.json(), Student.query.all()))


api.add_resource(main, '/')
if __name__ == '__main__':
    app.run()
