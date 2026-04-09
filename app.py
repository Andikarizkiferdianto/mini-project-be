import falcon
from falcon_cors import CORS
from models.schema import db, AdminUser
from pony.orm import db_session

from resources.siswa import SiswaResource, SiswaWithIdResource
from resources.auth import AdminLoginResource

cors = CORS(allow_all_origins=True,
            allow_all_headers=True,
            allow_all_methods=True)

app = falcon.App(middleware=[cors.middleware])

db.bind(provider='sqlite', filename='sap_database.sqlite', create_db=True)

app.add_route('/api/siswa', SiswaResource())
app.add_route('/api/siswa/{siswa_id}', SiswaWithIdResource())
app.add_route('/api/admin/login', AdminLoginResource())

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    from models.schema import *

    db.generate_mapping(create_tables=True)

    with db_session:
        if AdminUser.select().count() == 0:
            AdminUser(name="Bos Dika", email="admin@sap.com", password="password123")
            print("Akun admin default (Email: admin@sap.com, Pass: password123)")

    print("Server Backend SAP berjalan di http://localhost:8000")
    with make_server('', 8000, app) as httpd:
        httpd.serve_forever()