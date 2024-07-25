from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Task

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('content')
        task_priority = request.form.get('priority')
        task_due_date = request.form.get('due_date')
        task_category = request.form.get('category')

        if task_content:
            new_task = Task(content=task_content, priority=task_priority, due_date=task_due_date, category=task_category)
            db.session.add(new_task)
            db.session.commit()
        return redirect(url_for('index'))

    search_query = request.args.get('search', '')
    tasks = Task.query.filter(Task.content.contains(search_query)).all()
    return render_template('index.html', tasks=tasks, search_query=search_query)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task_to_delete = Task.query.get(task_id)
    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = not task.completed
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)