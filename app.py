from flask import Flask, render_template, request, redirect, url_for, send_file, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
import datetime
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///tracker.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
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
    if User.query.first() is None:
        admin = User(username='admin', password='password', role='admin')
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def index():
    return redirect(url_for('calendar_view'))

@app.route('/calendar')
def calendar_view():
    if 'user' not in session:
        return redirect(url_for('login'))
    tasks = Task.query.all()
    events = []
    color_map = {"Planned": "#FFA500", "In Progress": "#007BFF", "Completed": "#28A745"}
    for row in tasks:
        events.append({
            "id": row.project_name,
            "name": row.project_name,
            "date": row.date,
            "description": f"Team: {row.team}, Status: {row.status}",
            "type": "event",
            "color": color_map.get(row.status, "#6C757D")
        })
    return render_template('calendar.html', events=events)

@app.route('/clock')
def clock():
    now = datetime.datetime.now()
    return jsonify({"time": now.strftime("%Y-%m-%d %H:%M:%S")})

@app.route('/recurring')
def recurring():
    if 'user' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))
    today = datetime.datetime.now().date().isoformat()
    tasks = Task.query.all()
    for task in tasks:
        if task.recurring == "daily" and task.date != today:
            db.session.add(Task(**{**task.__dict__, 'date': today, 'id': None}))
        elif task.recurring == "weekly":
            last_dt = datetime.datetime.strptime(task.date, '%Y-%m-%d')
            if (datetime.datetime.now().date() - last_dt.date()).days >= 7:
                db.session.add(Task(**{**task.__dict__, 'date': today, 'id': None}))
    db.session.commit()
    return redirect(url_for('calendar_view'))

@app.route('/download-weekly-report')
def download_weekly_report():
    if 'user' not in session:
        return redirect(url_for('login'))
    one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
    recent_tasks = Task.query.filter(Task.date >= one_week_ago.strftime('%Y-%m-%d')).all()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Weekly Project Report", ln=True, align='C')
    pdf.ln(10)

    for task in recent_tasks:
        pdf.multi_cell(0, 10, txt=f"Date: {task.date}\nProject: {task.project_name}\nTeam: {task.team}\nAssigned: {task.assigned_members}\nStatus: {task.status}\nProgress: {task.achieved_output}/{task.target_output}\nMilestone: {task.milestone}\nReview: {task.review_status}\nNotes: {task.notes}\n{'-'*80}")

    file_path = "weekly_report.pdf"
    pdf.output(file_path)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
