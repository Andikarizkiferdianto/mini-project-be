import json
import falcon

def response_api(resp, status=falcon.HTTP_200, message="Success", data=None):
    resp.status = status
    payload = {
        "message": message,
        "data": data
    }
    resp.text = json.dumps(payload)