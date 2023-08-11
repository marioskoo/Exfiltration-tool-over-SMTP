import http.client
import mimetypes
from codecs import encode
import json
def createPaste(content):
    conn = http.client.HTTPSConnection("pastes.io")
    dataList = []
    boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=content;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(content))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=status;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("1"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=expire;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("N"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=title;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("My Paste"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=syntax;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode("none"))
    dataList.append(encode('--' + boundary))
    dataList.append(encode('Content-Disposition: form-data; name=password;'))

    dataList.append(encode('Content-Type: {}'.format('text/plain')))
    dataList.append(encode(''))

    dataList.append(encode(""))
    dataList.append(encode('--'+boundary+'--'))
    dataList.append(encode(''))
    body = b'\r\n'.join(dataList)
    payload = body
    headers = {
    'Accept': 'application/json',
    'Authorization': 'Bearer 16dfeb6eb1b2e559bcd7679aaa9e84a5d7aba02aae7e5f63fbccca6f76224ab7', # api token qui
    'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
    }
    conn.request("POST", "/api/paste/create", payload, headers)
    res = conn.getresponse()
    data = res.read()

    if res.status == 200:
        response_data = json.loads(data)
        if(response_data['success']):
            slug = response_data['success']['slug']
            return str(slug)
        else:
            return None
    else:
        print('Request failed with status code:', res.status)
        print(data.decode())
        return None
