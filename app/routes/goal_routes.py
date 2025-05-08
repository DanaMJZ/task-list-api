from flask import Blueprint, jsonify, request, make_response
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from app.helper import validate_model

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.route("", methods=["POST"])
def create_goal():
    request_body = request.get_json()
    
    if not request_body or "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    return jsonify({"goal": new_goal.to_dict()}), 201

@goal_bp.route("", methods=["GET"])
def get_goals():
    goals = Goal.query.order_by(Goal.id).all()
    goals_response = [goal.to_dict() for goal in goals]
    return jsonify(goals_response), 200

@goal_bp.route("/<goal_id>", methods=["GET"])
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return jsonify({"goal": goal.to_dict()}), 200

@goal_bp.route("/<goal_id>", methods=["PUT"])
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return make_response("", 204, {"Content-Type": "application/json"})

@goal_bp.route("/<goal_id>", methods=["DELETE"])
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return make_response("", 204, {"Content-Type": "application/json"})

# Wave 6
@goal_bp.route("/<goal_id>/tasks", methods=["POST"])
def assign_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_ids = request_body.get("task_ids")
    if not isinstance(task_ids, list):
        return jsonify({"details": "task_ids must be a list"}), 400
    for task in goal.tasks:
        task.goal_id = None

    tasks = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id
        tasks.append(task)

    db.session.commit()

    return jsonify({
        "id": goal.id,
        "task_ids": [task.id for task in tasks]
    }), 200


@goal_bp.route("/<goal_id>/tasks", methods=["GET"])
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return jsonify({
        "id": goal.id,
        "title": goal.title,
        "tasks": [
            {
                **task.to_dict(),
                "goal_id": goal.id
            } for task in goal.tasks
        ]
    }), 200