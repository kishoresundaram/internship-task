from typing import Any

from celery.result import AsyncResult


class JobStatusService:

    @staticmethod
    def get_status(
        task_id: str,
        celery_app,
    ) -> dict[str, Any]:

        task = AsyncResult(
            task_id,
            app=celery_app,
        )

        response: dict[str, Any] = {
            "task_id": task_id,
            "status": task.status,
        }

        if task.info:
            if isinstance(task.info, dict):
                response["details"] = task.info
            else:
                response["details"] = str(task.info)

        if task.successful():
            response["result"] = task.result

        return response