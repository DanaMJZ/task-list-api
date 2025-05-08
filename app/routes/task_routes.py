from flask import Blueprint, jsonify, request, abort, make_response
from app.models.task import Task
from app.db import db
from datetime import datetime
from app.helper import validate_model
import os
import requests 
# Wave1
task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


# @task_bp.post("")
# def create_task():
#     request_body = request.get_json()
#     try:
#         new_task = Task.from_dict(request_body)
#     except KeyError as error:
#         return make_response({"message": f"Invalid request: missing {error.args[0]}"}, 400)

#     db.session.add(new_task)
#     db.session.commit()

#     return new_task.to_dict(), 201

@task_bp.post("")
def create_task():
    request_body = request.get_json()

    if not request_body or "title" not in request_body or "description" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"task": new_task.to_dict()}), 201


@task_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    description_param = request.args.get("description")
    sort_param = request.args.get("sort")

    if title_param:
        query = query.where(Task.title == title_param)
    if description_param:
        query = query.where(Task.description == description_param)
# Wave2
    if sort_param == "asc":    
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id) 

    tasks = db.session.scalars(query).all()
    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response


@task_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}


@task_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)

    db.session.commit()
    return make_response(f'"Task #{task.id} successfully updated"', 204, {"Content-Type": "application/json"})


@task_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return make_response(f'"Task #{task.id} successfully deleted"', 204, {"Content-Type": "application/json"})


# Wave3
@task_bp.patch("/<int:task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)  
    if task.completed_at:
        return make_response("", 204)
    task.completed_at = datetime.now()
    db.session.commit()

# Wave4
    # slack_token = os.environ.get("SLACK_BOT_TOKEN")
    # slack_channel = os.environ.get("SLACK_CHANNEL")
    # slack_url = "https://slack.com/api/chat.postMessage"

    # slack_headers = {
    #     "Authorization": f"Bearer {slack_token}",
    #     "Content-Type": "application/json"
    # }

    # slack_payload = {
    #     "channel": slack_channel,
    #     "text": f"Someone just completed the task: {task.title}"
    # }

    # request.post(slack_url, headers=slack_headers, json=slack_payload)


    # return make_response("", 204)  
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_channel = os.environ.get("SLACK_CHANNEL", "task-notifications")  
    
    if slack_token:  # Only attempt if token exists
        slack_url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": f"Bearer {slack_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "channel": slack_channel,
            "text": f"Someone just completed the task: {task.title}"
        }
        
        try:
            response = requests.post(slack_url, headers=headers, json=payload)
            if not response.json().get("ok"):
                print("Slack API Error:", response.json())
        except Exception as e:
            print("Failed to send Slack notification:", str(e))

    return make_response({"task": task.to_dict()}, 200)



@task_bp.patch("/<int:task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)  
    if not task.completed_at:
        return make_response({"message": "Task is already incomplete."}, 204)

    task.completed_at = None  
    db.session.commit()

    return make_response("", 204)  

