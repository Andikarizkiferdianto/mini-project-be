import json
import falcon
from datetime import datetime
from pony.orm import db_session
from models.schema import AdminUser


class AdminLoginResource:
    @db_session
    def on_post(self, req, resp):
        payload = json.loads(req.stream.read(req.content_length or 0))
        email = payload.get('email')
        password = payload.get('password')
        admin = AdminUser.get(email=email)

        if not admin or admin.password != password:
            resp.status = falcon.HTTP_401
            resp.text = json.dumps({
                "message": "Email atau password salah bos!"
            })
            return

        admin.last_login = datetime.now()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "message": "Login berhasil!",
            "data": admin.to_response(),
            "token": "dummy-token-sap-12345"
        })
