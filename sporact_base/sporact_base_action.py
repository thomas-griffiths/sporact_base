import logging
import os
import time
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

    def add_task(self, task: dict, tag=""):
        try:
            if tag != "":
                tag = str(tag).lower() + "-"
            task_id = "task-" + tag + str(uuid.uuid4())
            obj = {task_id: json.dumps({"inputs": task, "status": "pending"})}
            rj.mset(obj)
            return {"status": "success", "task_id": task_id}
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def add_result(self, result: dict):
        try:
            task_id = result["task_id"]
            del result["task_id"]
            response = rj.mget(task_id)
            if None not in response:
                response = json.loads(response[0])
                response.update({"outputs": result["outputs"], "status": "completed"})
                obj = {task_id: json.dumps(response)}
                rj.mset(obj)
            else:
                pass
            return {"status": "success", "task_id": task_id}
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def get_task_info(self, task_id: str):
        try:
            response = rj.mget(task_id)
            if None not in response:
                response = json.loads(response[0])
                if "outputs" in response and response["status"] == "completed":
                    self.remove_task(task_id)
                else:
                    response.update({"status": "in-progress"})
                    obj = {task_id: json.dumps(response)}
                    rj.mset(obj)
            else:
                response = {}
            return response
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def get_task(self, tag=""):
        try:
            if tag != "":
                tag = str(tag).lower() + "-"
            result = rj.scan_iter()
            key_list = []
            for key in result:
                if str(key.decode("utf-8")).startswith("task-" + tag):
                    key_list.append(key.decode("utf-8"))
            final_list = []
            for each_key in key_list:
                response = self.get_task_info(each_key)
                if response != {}:
                    outputs = {}
                    if "outputs" in response:
                        outputs = response["outputs"]
                    final_json = {"task_id": each_key, "status": response["status"],
                                  "inputs": response["inputs"], "outputs": outputs}
                    final_list.append(final_json)
            return final_list
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def remove_task(self, task_id: str):
        try:
            rj.delete(task_id)
            return {"status": "success"}
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def get_result(self, task: dict, timeout=300):
        try:
            response = {}
            while True:
                if timeout == 0:
                    break
                if "task_id" in task:
                    response = self.get_task_info(task["task_id"])
                    if "outputs" in response:
                        if response["outputs"] != {}:
                            break
                else:
                    break
                timeout = timeout - 1
                time.sleep(1)
            final_json = {}
            if response != {}:
                final_json = {"task_id": task["task_id"], "status": response["status"],
                              "outputs": response["outputs"]}
            return final_json
        except Exception as e:
            traceback.print_exc()
            return {"status": "failed"}

    def get_integration(self, cur_dir: str):
        try:
            file_name = "integration.json"
            while True:
                file_list = os.listdir(cur_dir)
                parent_dir = os.path.dirname(cur_dir)
                if file_name in file_list:
                    with open(os.path.join(cur_dir, file_name), "r") as file:
                        integration_data = json.loads(file.read())
                        integration_name = integration_data["name"]
                        return integration_name
                else:
                    if cur_dir == parent_dir:
                        return ""
                    else:
                        cur_dir = parent_dir
        except Exception as e:
            traceback.print_exc()
            return ""
