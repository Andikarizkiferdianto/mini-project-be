import json
import falcon
import jwt  # Import PyJWT
from datetime import datetime, timedelta
from pony.orm import db_session
from models.schema import AdminUser

SECRET_KEY = "sap_pintar_rahasia_banget_123"


class AdminLoginResource:
    def on_post(self, req, resp):
        with db_session:
            try:
                raw_json = req.stream.read(req.content_length or 0)
                payload = json.loads(raw_json)

                email = payload.get('email')
                password = payload.get('password')

                admin = AdminUser.get(email=email)

                if not admin or admin.password != password:
                    resp.status = falcon.HTTP_401
                    resp.text = json.dumps({
                        "status": "error",
                        "message": "Email atau password salah, cek lagi bro!"
                    })
                    return

                admin.last_login = datetime.now()

                token_payload = {
                    "admin_id": admin.id,
                    "email": admin.email,
                    "exp": datetime.utcnow() + timedelta(hours=24)  # Token mati dalam 24 jam
                }

                encoded_jwt = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")

                resp.status = falcon.HTTP_200
                resp.text = json.dumps({
                    "status": "success",
                    "message": f"Selamat datang kembali, {admin.name}!",
                    "data": admin.to_response(),
                    "token": encoded_jwt
                })

            except Exception as e:
                resp.status = falcon.HTTP_500
                resp.text = json.dumps({
                    "status": "error",
                    "message": f"Ada masalah di server: {str(e)}"
                })