from flask_restful import Resource

from anakonda.controller.apiv1 import TaskController


class TaskResource(Resource):
    def get(self, task_id=None):
        """
        GET /api/v1/tasks --> List of tasks.
        GET /api/v1/tasks/<task_id> --> Get task info.
        """
        if task_id is None:
            return TaskController.get_tasks()
        else:
            return TaskController.get_task(task_id)

    def post(self):
        """
        POST /api/v1/tasks --> Create a new task.
        POST /api/v1/tasks/<task_id> --> Not allowed.
        """
        return TaskController.create_task()

    def patch(self, task_id):
        """
        PATCH /api/v1/tasks --> Not allowed.
        PATCH /api/v1/tasks/<task_id> --> Update task.
        """
        return TaskController.update_task(task_id)

    def delete(self, task_id):
        """
        DELETE /api/v1/tasks --> Not allowed.
        DELETE /api/v1/tasks/<task_id> --> Delete task.
        """
        return TaskController.delete_task(task_id)
