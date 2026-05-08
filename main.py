

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(50), default='Medium')
    category = db.Column(db.String(50), default='Work')
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

# Remove the inefficient before_request table creation
# db.create_all() will be called in the main block

@app.route("/", methods=["GET", "POST"])
def index():
    categories = ["Work", "Personal", "Shopping", "Others"]
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        priority = request.form.get("priority", "Medium")
        category = request.form.get("category", "Work")
        if title:
            db.session.add(Task(title=title, priority=priority, category=category))
            db.session.commit()
        return redirect(url_for("index"))

    tasks = Task.query.order_by(Task.created_at.desc()).all()
    grouped_tasks = {cat: [t for t in tasks if t.category == cat] for cat in categories}
    return render_template("index.html", grouped_tasks=grouped_tasks, categories=categories)

@app.route("/toggle/<int:task_id>", methods=["POST"])
def toggle_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)