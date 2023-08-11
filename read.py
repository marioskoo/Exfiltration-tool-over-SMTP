import http.client
import mimetypes
from codecs import encode
import json


def readPastes(slug):
    conn = http.client.HTTPSConnection("pastes.io")
    dataList = []
    boundary = "wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T"
    dataList.append(encode("--" + boundary))
    dataList.append(encode("Content-Disposition: form-data; name=password;"))

    dataList.append(encode("Content-Type: {}".format("text/plain")))
    dataList.append(encode(""))

    dataList.append(encode("12345"))
    dataList.append(encode("--" + boundary + "--"))
    dataList.append(encode(""))
    body = b"\r\n".join(dataList)
    payload = body
    headers = {
        "Accept": "application/json",
        "Content-type": "multipart/form-data; boundary={}".format(boundary),
    }
    conn.request("POST", "/api/pastes/" + str(slug), payload, headers)
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))
