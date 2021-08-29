# lib
import json
import sys
from iotticket.models import device
from iotticket.models import criteria
from iotticket.models import deviceattribute
from iotticket.models import datanodesvalue
from iotticket.client import Client

data = json.load(open(sys.argv[1]))
username = data["username"]
password = data["password"]
# deviceId = data["deviceId"] #device id is generated after device is registered
baseurl = data["baseurl"]


def create(enterprize_id, uuid):

    c = Client(baseurl, username, password)

    d = device()
    d.set_name(f"{uuid}")  # needed for register
    d.set_manufacturer("IISY")  # needed for register
    d.set_type("QR-entity")
    d.set_description("IISY_enterprize")
    # if enterprise id is not given, iotticket use default enterprise id.
    d.set_enterpriseId(f"{enterprize_id}")
    d.set_attributes(deviceattribute("key", f"{uuid}"))

    # register device demo
    print("REGISTER DEVICE FUNTION.")
    dev = c.registerdevice(d)
    print(dev)
    print(dev.deviceId)
    print("END REGISTER DEVICE FUNCTION")
    print("-------------------------------------------------------\n")

    # get all device function demo
    print("GET ALL DEVICES FUNTION.")
    print("Get list of devices:\n", c.getdevices(5, 0))
    print("END GET ALL DEVICES FUNCTION")
    print("-------------------------------------------------------\n")

    return dev.deviceId


def upload(tag, deviceId, baseurl, username, password, value):

    c = Client(baseurl, username, password)

    print("WRITE DEVICE DATANODES FUNTION.")
    listofvalues = []
    nv = datanodesvalue()
    nv.set_name("Trashbin issue")  # needed for writing datanode
    nv.set_path(f"{tag}")
    nv.set_dataType("boolean")
    nv.set_value(value)  # needed for writing datanode
    listofvalues.append(nv)

    # another way to make this would be c.writedata(deviceId, nv, nv1)
    print(c.writedata(deviceId, *listofvalues))
    print("END WRITE DEVICE DATANODES FUNCTION")
    print("-------------------------------------------------------\n")


if __name__ == "__main__":
    # just for testing example usage
    deviceId = create('E9382', 'test_location')
    upload(tag="trashbin_reported", deviceId=deviceId, baseurl=baseurl,
           username=username, password=password, value=True)
