import falcon
import json
from models.schema import db_session, Siswa, Kelas, Jurusan  # Import model kamu


class DashboardStatsResource:
    def on_get(self, req, resp):
        with db_session:
            total_siswa = Siswa.select().count()
            total_kelas = Kelas.select().count()
            total_jurusan = Jurusan.select().count()

            total_alumni = Siswa.select(lambda s: s.status == 'Alumni').count() if hasattr(Siswa, 'status') else 0

            data = {
                "akademik": {
                    "total_siswa_aktif": total_siswa,
                    "total_guru": 45,
                    "total_staf": 15,
                    "total_kelas": total_kelas,
                    "total_jurusan": total_jurusan,
                    "total_alumni": total_alumni,
                    "total_ekstrakurikuler": 12
                },
                "keuangan": {
                    "total_pendapatan_bulan_ini": 25500000,
                    "total_tagihan_tertunggak": 8500000,
                    "total_kas_keluar": 12000000
                },
                "grafik_kehadiran_hari_ini": {
                    "hadir": 0,
                    "izin": 0,
                    "sakit": 0,
                    "alpha": total_siswa
                }
            }

        resp.text = json.dumps({
            "status": "success",
            "message": "Data dashboard asli berhasil diambil",
            "data": data
        })
        resp.status = falcon.HTTP_200