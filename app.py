from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    is_completed = db.Column(db.Boolean, default=False)


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.content for task in tasks])


@app.route('/tasks', methods=['POST'])
def create_or_update_task():
    data = request.get_json()
    task_id = data.get('id')

    if task_id:
        task = Task.query.get(task_id)
        if task:
            task.title = data.get('title', task.title)
            task.description = data.get('description', task.description)
            task.is_completed = data.get('is_completed', task.is_completed)
        else:
            return jsonify({'message': 'Task not found'}), 404
    else:
        task = Task(title=data['title'], description=data.get('description'))
        db.session.add(task)

    db.session.commit()

    return jsonify(
        {'id': task.id, 'title': task.title, 'description': task.description, 'is_completed': task.is_completed})


@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    with app.app_context():
        task = Task.query.get(task_id)
        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'result': 'Task deleted'}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
