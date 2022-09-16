import logging
import os
import traceback
import uuid
import json
from redis import Redis

rj = Redis(host='redis', port=6379)

logger = logging.getLogger("base_action")

try:
    log_dir = os.path.join(os.environ.get("INTEGRATIONS"), "logs")
except Exception:
    # logger not found
    log_dir = os.path.join(os.getcwd(), "logs")

logger.setLevel(logging.INFO)
os.makedirs(log_dir, exist_ok=True)
fh = logging.FileHandler(os.path.join(log_dir, "action.log"))
fh.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)


class SporactBaseAction:

    def __init__(self, extracontent):
        self.conf = extracontent.get("conf", None)
        self.sporact = extracontent.get("sporact", None)
        self.LOG = logger
        self.case = extracontent.get("case", None)
        self.SPORACT_URL = "http://api:8000/"
        self.SPORACT_API_URL = "http://api:8000/api/"
        self.SPORACT_MEDIA_URL = "http://api:8000/media/"

    def add_task(self, task: dict):
        try:
            task_id = "firewall-task-" + str(uuid.uuid4())
            obj = {task_id: json.dumps({"task": task})}
            rj.mset(obj)
            return {"status": "success", "task_id": task_id}
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def add_result(self, task: dict):
        try:
            task_id = task["task_id"]
            del task["task_id"]
            response = rj.mget(task_id)
            if None not in response:
                response = json.loads(response[0])
                response.update({"result": task})
                obj = {task_id: json.dumps(response)}
                rj.mset(obj)
            else:
                pass
            return {"status": "success", "task_id": task_id}
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def get_result(self, task_id: str):
        try:
            response = rj.mget(task_id)
            if None not in response:
                response = json.loads(response[0])
            else:
                response = {}
            return response
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def get_task(self):
        try:
            result = rj.scan_iter()
            key_list = []
            for key in result:
                if str(key.decode("utf-8")).startswith("firewall-task-"):
                    key_list.append(key.decode("utf-8"))
                # rj.delete(key)
            final_json = {}
            for each_key in key_list:
                response = get_result(each_key)
                final_json[each_key] = response
            return final_json
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}
