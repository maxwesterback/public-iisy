
import json
import sys
from .integration_utilities import create


data = json.load(open(sys.argv[1]))
username = data["username"]
password = data["password"]
baseurl = data["baseurl"]
enterprize_id = data["enterprize_id"]

# this is demo, we would upload ids from database
qr_ids = ['uuid1']

for uuid in qr_ids:
    deviceId = create(enterprize_id, uuid)
