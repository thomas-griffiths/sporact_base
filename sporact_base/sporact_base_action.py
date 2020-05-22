import logging
import os

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

