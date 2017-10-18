from requests import get, post
import json, uuid

# TODO: write docstrings
class FtsRequest:
    baseUrl = "https://proverkacheka.nalog.ru:9999"

    def __init__(self):
        self.headers = {'Device-Id':     uuid.uuid4().hex,
                        'Device-OS':     "Adnroid 4.4.4",
                        'Version':       "2",
                        'ClientVersion': "1.4.1.3",
                        'user-agent':    "okhttp/3.0.1"}
    
    def signUp(self, name, email, phone):
        url = "{}/v1/mobile/users/signup".format(self.baseUrl)
        
        data = {"name": name, "email" : email, "phone": phone}

        response = post(url, headers = self.headers, json = data)

        if response.ok:
            return json.loads(json.dumps({"ftsRequestSuccess": True}))
        else:
            JSON = {"ftsRequestSuccess": False, "responseCode": response.status_code, "error": response.text}
            return json.loads(json.dumps(JSON))

    def restorePassword(self, phone):
        url = "{}/v1/mobile/users/restore".format(self.baseUrl)
        
        data = {"phone": phone}

        response = post(url, headers = self.headers, json = data)

        if response.ok:
            return json.loads(json.dumps({"ftsRequestSuccess": True}))
        else:
            JSON = {"ftsRequestSuccess": False, "responseCode": response.status_code, "error": response.text}
            return json.loads(json.dumps(JSON))

    def checkAuthData(self, loginPhone, smsPass):
        url = "{}/v1/mobile/users/login".format(self.baseUrl)
        auth = (loginPhone, smsPass)

        response = get(url, headers = self.headers, auth = auth)
        return response.ok

    def getReceipt(self, fn, fd, fp, loginPhone, smsPass):
        url = "{}/v1/inns/*/kkts/*/fss/{}/tickets/{}?fiscalSign={}&sendToEmail=no".format(self.baseUrl, fn, fd, fp)
        auth = (loginPhone, smsPass)

        response = get(url, headers = self.headers, auth = auth)

        if response.ok:
            JSON = json.loads(response.text)['document']['receipt']
            JSON["ftsRequestSuccess"] = True
            return JSON
        else:
            JSON = {"ftsRequestSuccess": False, "responseCode": response.status_code, "error": response.text}
            return json.loads(json.dumps(JSON))