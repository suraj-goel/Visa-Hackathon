import requests
url = "https://sandbox.api.visa.com/vdp/helloworld"
r = requests.get(url, timeout=10,
                 #put your certificate and key or just use mine
                  cert = ('./cert.pem','./key_374cc983-558b-49dd-a55b-99d3cb3afac5.pem'),
                  headers = {},
                  auth = ("STT3WACAH2W19FH6H48A2117b1JIIYevI8qRcIQn2Zwhtdp4M", "81SYH42zc2CwJgtOzInj50e8zT6vr"),
                  data = {})
print(r.text)