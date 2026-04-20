import falcon
import pymysql
pymysql.install_as_MySQLdb()
from falcon_cors import CORS
from models.schema import db, AdminUser
from pony.orm import db_session
from waitress import serve

from resources.siswa import SiswaResource, SiswaWithIdResource
from resources.auth import AdminLoginResource
from resources.dashboard import DashboardStatsResource
from resources.kelas import KelasResource, KelasWithIdResource
from resources.jurusan import JurusanResource, JurusanWithIdResource
from resources.absensi import AbsensiResource
from resources.ekskul import EkskulResource, EkskulDetailResource

cors = CORS(allow_all_origins=True,
            allow_all_headers=True,
            allow_all_methods=True)

app = falcon.App(middleware=[cors.middleware])

db.bind(provider='mysql', host='localhost', user='root', passwd='', db='sap_database')

app.add_route('/api/siswa', SiswaResource())
app.add_route('/api/siswa/{siswa_id}', SiswaWithIdResource())
app.add_route('/api/admin/login', AdminLoginResource())
app.add_route('/api/dashboard/stats', DashboardStatsResource())
app.add_route('/api/kelas', KelasResource())
app.add_route('/api/kelas/{kelas_id}', KelasWithIdResource())
app.add_route('/api/jurusan', JurusanResource())
app.add_route('/api/jurusan/{jurusan_id}', JurusanWithIdResource())
app.add_route('/api/absensi', AbsensiResource())
app.add_route('/api/ekskul', EkskulResource())
app.add_route('/api/ekskul/{ekskul_id}', EkskulDetailResource())

if __name__ == '__main__':
    from models.schema import *

    db.generate_mapping(create_tables=True)

    with db_session:
        if AdminUser.select().count() == 0:
            AdminUser(name="Bos Dika", email="admin@sap.com", password="password123")
            print("Akun admin default (Email: admin@sap.com, Pass: password123)")

    print("Server Mini Project jalan di http://localhost:8000")
    serve(app, host='0.0.0.0', port=8000)
