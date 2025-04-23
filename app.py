
from flask import Flask, render_template, request, redirect, url_for, send_file, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os, datetime
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///tracker.db")
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    owner = db.Column(db.String(50))
    tasks = db.relationship('Task', backref='project', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=True)
    date = db.Column(db.String(20))
    team = db.Column(db.String(100))
    project_name = db.Column(db.String(200))
    assigned_members = db.Column(db.String(200))
    target_output = db.Column(db.Integer)
    achieved_output = db.Column(db.Integer)
    status = db.Column(db.String(50))
    milestone = db.Column(db.String(200))
    feedback = db.Column(db.String(300))
    asset_links = db.Column(db.String(300))
    review_status = db.Column(db.String(100))
    notes = db.Column(db.String(300))
    checklist = db.Column(db.String(300))
    subcomponent_type = db.Column(db.String(50))
    recurring = db.Column(db.String(20))
    created_by = db.Column(db.String(50))

with app.app_context():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        db.session.add(User(username='admin', password=generate_password_hash('password'), role='admin'))
        db.session.commit()

# All routes (login, logout, calendar, projects, dashboard, kanban included as per earlier provided)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
