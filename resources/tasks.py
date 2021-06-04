from flask import request
from flask import jsonify
from datetime import datetime
from flask import Blueprint

from database import tasks

tasks_bp = Blueprint('routes-tasks', __name__)


@tasks_bp.route('/')
def welcome():
    return "Api creada para gestionar tareas por realizar futuramente le crearemos la interfaz de usuario"

@tasks_bp.route('/tasks', methods=['POST'])
def add_task():
    title = request.json['title']
    created_date = datetime.now().strftime("%x") #Nos da el formato de fecha

    data = (title, created_date)
    task_id = tasks.insert_task(data)

    if task_id:
        task = tasks.select_task_by_id(task_id)
        return jsonify({'task': task})
    return jsonify({'message':'Internal error'})

@tasks_bp.route('/tasks', methods=['GET'])
def get_tasks():
    data = tasks.select_all_task()

    if data:
        return jsonify({"tasks" : data})
    elif data == False:
        return jsonify({'message' : 'Internal error'})    
    else:
        return jsonify({'tasks' : {}})


@tasks_bp.route('/tasks', methods=['PUT'])
def update_task():
    title = request.json['title'] 
    id_arg = request.args.get('id')   

    if tasks.update_task(id_arg, (title,)):
        task = tasks.select_task_by_id(id_arg)
        return jsonify(task)
    return jsonify({'message':'Internal error'})    

@tasks_bp.route('/tasks', methods=['DELETE'])
def delete_task():
    id_arg = request.args.get('id')

    if tasks.delete_task(id_arg):
        return jsonify({'message' : 'Task deleted'})
    return jsonify({'message' : 'Internal Error'})   

@tasks_bp.route('/tasks/completed', methods=['PUT'])
def completed_task():
    id_args = request.args.get('id')
    completed = request.args.get('completed')
    if tasks.complete_task(id_args, completed):
        return jsonify({'message' : 'Task completed'})
    return jsonify({'message' : 'Internal error'}) 