from anakonda.model import Task
from anakonda.util import jsonify


class TaskController:
    def get_tasks():
        return jsonify(status=501, code=101)

    def get_task(task_id):
        return jsonify(status=501, code=101)

    def create_task():
        return jsonify(status=501, code=101)

    def update_task(task_id):
        return jsonify(status=501, code=101)

    def delete_task(task_id):
        return jsonify(status=501, code=101)
