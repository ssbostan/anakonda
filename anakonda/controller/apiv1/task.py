from flask import request

from anakonda.anakonda import db
from anakonda.config import Config
from anakonda.decorator import json_required
from anakonda.model import Task
from anakonda.schema.apiv1 import TaskSchema
from anakonda.util import jsonify, now


class TaskController:
    @json_required
    def get_tasks():
        try:
            tasks_schema = TaskSchema(many=True)
        except:
            return jsonify(status=500, code=103)
        try:
            tasks = Task.query.all()
        except:
            return jsonify(status=500, code=106)
        return jsonify(tasks_schema.dump(tasks))

    @json_required
    def get_task(task_id):
        try:
            task_schema = TaskSchema()
        except:
            return jsonify(status=500, code=103)
        try:
            task = db.session.get(Task, task_id)
        except:
            return jsonify(status=500, code=106)
        if task is None:
            return jsonify(status=404, code=107)
        return jsonify(task_schema.dump(task))

    @json_required
    def create_task():
        try:
            task_schema = TaskSchema()
        except:
            return jsonify(status=500, code=103)
        try:
            request_data = task_schema.load(request.get_json())
        except:
            return jsonify(status=400, code=102)
        if len(request_data["name"]) > 32 or not request_data["name"].islower():
            return jsonify(status=400, code=104)
        if (
            len(request_data["namespace"]) > 32
            or not request_data["namespace"].islower()
        ):
            return jsonify(status=400, code=104)
        if request_data["runtime"] not in Config.AVAILABLE_RUNTIMES:
            return jsonify(status=400, code=108)
        task = Task(
            name=request_data["name"],
            namespace=request_data["namespace"],
            runtime=request_data["runtime"],
            image=request_data["image"],
            script=request_data["script"],
            status="new",
        )
        db.session.add(task)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(status=500, code=106)
        return jsonify(task_schema.dump(task), status=201)

    @json_required
    def update_task(task_id):
        try:
            task_schema = TaskSchema(partial=True)
        except:
            return jsonify(status=500, code=103)
        try:
            request_data = task_schema.load(request.get_json())
        except:
            return jsonify(status=400, code=102)
        if "name" in request_data:
            if len(request_data["name"]) > 32 or not request_data["name"].islower():
                return jsonify(status=400, code=104)
        if "namespace" in request_data:
            if (
                len(request_data["namespace"]) > 32
                or not request_data["namespace"].islower()
            ):
                return jsonify(status=400, code=104)
        if "runtime" in request_data:
            if request_data["runtime"] not in Config.AVAILABLE_RUNTIMES:
                return jsonify(status=400, code=108)
        try:
            task = db.session.get(Task, task_id)
        except:
            return jsonify(status=500, code=106)
        if task is None:
            return jsonify(status=404, code=107)
        if task.status != "new":
            return jsonify(status=400, code=109)
        task.name = request_data["name"] if "name" in request_data else task.name
        task.namespace = (
            request_data["namespace"] if "namespace" in request_data else task.namespace
        )
        task.runtime = (
            request_data["runtime"] if "runtime" in request_data else task.runtime
        )
        task.image = request_data["image"] if "image" in request_data else task.image
        task.script = (
            request_data["script"] if "script" in request_data else task.script
        )
        task.last_update_at = now()
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(status=500, code=106)
        return jsonify(task_schema.dump(task))

    @json_required
    def delete_task(task_id):
        try:
            task = db.session.get(Task, task_id)
        except:
            return jsonify(status=500, code=106)
        if task is None:
            return jsonify(status=404, code=107)
        db.session.delete(task)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify(status=500, code=106)
        return jsonify()
