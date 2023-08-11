import http.client
import mimetypes
from codecs import encode
# usare il login per avere il 'bearer' da usare poi per tutte le richieste create 
conn = http.client.HTTPSConnection("pastes.io")
dataList = []
boundary = 'wL36Yn8afVp8Ag7AmP8qZ0SA4n1v9T'
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=username;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("Mariosk0x"))#username di pastes
dataList.append(encode('--' + boundary))
dataList.append(encode('Content-Disposition: form-data; name=password;'))

dataList.append(encode('Content-Type: {}'.format('text/plain')))
dataList.append(encode(''))

dataList.append(encode("marianocyber"))#password di pastes
dataList.append(encode('--'+boundary+'--'))
dataList.append(encode(''))
body = b'\r\n'.join(dataList)
payload = body
headers = {
  'Accept': 'application/json',
  'Content-type': 'multipart/form-data; boundary={}'.format(boundary)
}
conn.request("POST", "/api/login", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
#prendi l'api token e mettilo in create
