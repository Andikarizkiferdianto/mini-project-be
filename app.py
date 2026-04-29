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
from resources.aspek import AspekResource, AspekDetailResource
from resources.semester import SemesterResource, SemesterDetailResource
from resources.tahun_ajaran import TahunAjaranResource, TahunAjaranWithIdResource, TahunAjaranActiveResource
from resources.jenis_semester import JenisSemesterResource, JenisSemesterDetailResource
from resources.jadwal import JadwalResource, JadwalDetailResource
from resources.mata_pelajaran import MataPelajaranResource, MataPelajaranDetailResource
from resources.guru import GuruResource, GuruDetailResource
from resources.jenis_pembayaran import JenisPembayaranResource, JenisPembayaranDetailResource

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
app.add_route('/api/aspek-penilaian', AspekResource())
app.add_route('/api/aspek-penilaian/{aspek_id}', AspekDetailResource())
app.add_route('/api/semester', SemesterResource())
app.add_route('/api/semester/{semester_id}', SemesterDetailResource())
app.add_route('/api/tahun-ajaran', TahunAjaranResource())
app.add_route('/api/tahun-ajaran/{ta_id}', TahunAjaranWithIdResource())
app.add_route('/api/tahun-ajaran/active', TahunAjaranActiveResource())
app.add_route('/api/jenis-semester', JenisSemesterResource())
app.add_route('/api/jenis-semester/{js_id}', JenisSemesterDetailResource())
app.add_route('/api/jadwal', JadwalResource())
app.add_route('/api/jadwal/{j_id}', JadwalDetailResource())
app.add_route('/api/mata-pelajaran', MataPelajaranResource())
app.add_route('/api/mata-pelajaran/{mp_id}', MataPelajaranDetailResource())
app.add_route('/api/guru', GuruResource())
app.add_route('/api/guru/{g_id}', GuruDetailResource())
app.add_route('/api/jenis-pembayaran', JenisPembayaranResource())
app.add_route('/api/jenis-pembayaran/{jp_id}', JenisPembayaranDetailResource())

if __name__ == '__main__':
    from models.schema import *

    db.generate_mapping(create_tables=True)

    with db_session:
        if AdminUser.select().count() == 0:
            AdminUser(name="Bos Dika", email="admin@sap.com", password="password123")
            print("Akun admin default (Email: admin@sap.com, Pass: password123)")

    print("Server Mini Project jalan di http://localhost:8000")
    serve(app, host='0.0.0.0', port=8000)
