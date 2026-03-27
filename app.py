
import os
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
    "DATABASE_URL",
    "sqlite:///employee_tracker.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship("Task", backref="employee", cascade="all, delete-orphan", lazy=True)
    leaves = db.relationship("LeaveRequest", backref="employee", cascade="all, delete-orphan", lazy=True)


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="Pending")
    priority = db.Column(db.String(30), default="Medium")
    due_date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class LeaveRequest(db.Model):
    __tablename__ = "leave_requests"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(30), default="Pending")
    employee_id = db.Column(db.Integer, db.ForeignKey("employees.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@app.route("/")
def dashboard():
    employee_count = Employee.query.count()
    task_count = Task.query.count()
    pending_task_count = Task.query.filter_by(status="Pending").count()
    leave_count = LeaveRequest.query.count()

    tasks_by_status = db.session.query(Task.status, func.count(Task.id)).group_by(Task.status).all()
    leave_by_status = db.session.query(LeaveRequest.status, func.count(LeaveRequest.id)).group_by(LeaveRequest.status).all()

    recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
    recent_leaves = LeaveRequest.query.order_by(LeaveRequest.created_at.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        employee_count=employee_count,
        task_count=task_count,
        pending_task_count=pending_task_count,
        leave_count=leave_count,
        tasks_by_status=tasks_by_status,
        leave_by_status=leave_by_status,
        recent_tasks=recent_tasks,
        recent_leaves=recent_leaves,
    )


@app.route("/employees")
def employees():
    all_employees = Employee.query.order_by(Employee.created_at.desc()).all()
    return render_template("employees.html", employees=all_employees)


@app.route("/employees/add", methods=["POST"])
def add_employee():
    name = request.form["name"].strip()
    email = request.form["email"].strip().lower()
    department = request.form["department"].strip()

    if not name or not email or not department:
        flash("All employee fields are required.", "error")
        return redirect(url_for("employees"))

    existing = Employee.query.filter_by(email=email).first()
    if existing:
        flash("Employee email already exists.", "error")
        return redirect(url_for("employees"))

    employee = Employee(name=name, email=email, department=department)
    db.session.add(employee)
    db.session.commit()
    flash("Employee added successfully.", "success")
    return redirect(url_for("employees"))


@app.route("/employees/delete/<int:employee_id>", methods=["POST"])
def delete_employee(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    db.session.delete(employee)
    db.session.commit()
    flash("Employee deleted successfully.", "success")
    return redirect(url_for("employees"))


@app.route("/tasks")
def tasks():
    all_tasks = Task.query.order_by(Task.due_date.asc()).all()
    employees = Employee.query.order_by(Employee.name.asc()).all()
    return render_template("tasks.html", tasks=all_tasks, employees=employees)


@app.route("/tasks/add", methods=["POST"])
def add_task():
    title = request.form["title"].strip()
    description = request.form["description"].strip()
    status = request.form["status"].strip()
    priority = request.form["priority"].strip()
    due_date = request.form["due_date"].strip()
    employee_id = request.form["employee_id"].strip()

    if not all([title, description, status, priority, due_date, employee_id]):
        flash("All task fields are required.", "error")
        return redirect(url_for("tasks"))

    task = Task(
        title=title,
        description=description,
        status=status,
        priority=priority,
        due_date=datetime.strptime(due_date, "%Y-%m-%d").date(),
        employee_id=int(employee_id),
    )
    db.session.add(task)
    db.session.commit()
    flash("Task added successfully.", "success")
    return redirect(url_for("tasks"))


@app.route("/tasks/update/<int:task_id>", methods=["POST"])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = request.form["status"]
    db.session.commit()
    flash("Task status updated.", "success")
    return redirect(url_for("tasks"))


@app.route("/tasks/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully.", "success")
    return redirect(url_for("tasks"))


@app.route("/leaves")
def leaves():
    all_leaves = LeaveRequest.query.order_by(LeaveRequest.start_date.desc()).all()
    employees = Employee.query.order_by(Employee.name.asc()).all()
    return render_template("leaves.html", leaves=all_leaves, employees=employees)


@app.route("/leaves/add", methods=["POST"])
def add_leave():
    start_date = request.form["start_date"].strip()
    end_date = request.form["end_date"].strip()
    reason = request.form["reason"].strip()
    status = request.form["status"].strip()
    employee_id = request.form["employee_id"].strip()

    if not all([start_date, end_date, reason, status, employee_id]):
        flash("All leave request fields are required.", "error")
        return redirect(url_for("leaves"))

    leave = LeaveRequest(
        start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
        end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
        reason=reason,
        status=status,
        employee_id=int(employee_id),
    )
    db.session.add(leave)
    db.session.commit()
    flash("Leave request submitted successfully.", "success")
    return redirect(url_for("leaves"))


@app.route("/leaves/update/<int:leave_id>", methods=["POST"])
def update_leave_status(leave_id):
    leave = LeaveRequest.query.get_or_404(leave_id)
    leave.status = request.form["status"]
    db.session.commit()
    flash("Leave status updated.", "success")
    return redirect(url_for("leaves"))


@app.route("/leaves/delete/<int:leave_id>", methods=["POST"])
def delete_leave(leave_id):
    leave = LeaveRequest.query.get_or_404(leave_id)
    db.session.delete(leave)
    db.session.commit()
    flash("Leave request deleted successfully.", "success")
    return redirect(url_for("leaves"))


@app.route("/health")
def health():
    return {"status": "ok"}, 200


def seed_data():
    if Employee.query.count() == 0:
        e1 = Employee(name="Aarav Sharma", email="aarav@example.com", department="Engineering")
        e2 = Employee(name="Priya Mehta", email="priya@example.com", department="HR")
        e3 = Employee(name="Neha Kulkarni", email="neha@example.com", department="Operations")
        db.session.add_all([e1, e2, e3])
        db.session.commit()

        db.session.add_all([
            Task(
                title="Prepare deployment checklist",
                description="Create release checklist for production deployment.",
                status="In Progress",
                priority="High",
                due_date=datetime.strptime("2026-03-25", "%Y-%m-%d").date(),
                employee_id=e1.id,
            ),
            Task(
                title="Update onboarding document",
                description="Refresh internal joining documentation for new hires.",
                status="Pending",
                priority="Medium",
                due_date=datetime.strptime("2026-03-28", "%Y-%m-%d").date(),
                employee_id=e2.id,
            ),
            LeaveRequest(
                start_date=datetime.strptime("2026-03-29", "%Y-%m-%d").date(),
                end_date=datetime.strptime("2026-03-31", "%Y-%m-%d").date(),
                reason="Family function",
                status="Pending",
                employee_id=e3.id,
            ),
        ])
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_data()
