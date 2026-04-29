import falcon
import json
from models.schema import db_session, Siswa, Kelas, Jurusan, Absensi, Ekstrakurikuler
from datetime import datetime


class DashboardStatsResource:
    def on_get(self, req, resp):
        with db_session:
            total_siswa = Siswa.select().count()
            total_kelas = Kelas.select().count()
            total_jurusan = Jurusan.select().count()
            total_alumni = Siswa.select(lambda s: s.status_aktif == "Alumni").count()
            total_eskul = Ekstrakurikuler.select().count()

            hari_ini = datetime.now().strftime("%Y-%m-%d")
            hadir_count = 0
            sakit_izin_count = 0

            list_absensi = Absensi.select()[:]

            for a in list_absensi:
                if a.tanggal.strftime("%Y-%m-%d") == hari_ini:
                    if a.status_hadir == "Hadir":
                        hadir_count += 1
                    elif a.status_hadir in ["Sakit", "Izin"]:
                        sakit_izin_count += 1

            alpha_count = total_siswa - hadir_count - sakit_izin_count

            data = {
                "akademik": {
                    "total_siswa_aktif": total_siswa,
                    "total_guru": 45,
                    "total_staf": 15,
                    "total_kelas": total_kelas,
                    "total_jurusan": total_jurusan,
                    "total_alumni": total_alumni,
                    "total_ekstrakurikuler": total_eskul
                },
                "grafik_kehadiran_hari_ini": {
                    "hadir": hadir_count,
                    "izin": sakit_izin_count,
                    "sakit": 0,
                    "alpha": max(0, alpha_count)
                }
            }

        resp.text = json.dumps({
            "status": "success",
            "message": "Data dashboard asli berhasil diambil",
            "data": data
        })
        resp.status = falcon.HTTP_200
