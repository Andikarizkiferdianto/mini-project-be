import falcon
import json


class DashboardStatsResource:
    def on_get(self, req, resp):
        data = {
            "akademik": {
                "total_siswa_aktif": 1250,
                "total_guru": 45,
                "total_staf": 15,
                "total_kelas": 32,
                "total_jurusan": 6,
                "total_alumni": 4520,
                "total_ekstrakurikuler": 12
            },
            "keuangan": {
                "total_pendapatan_bulan_ini": 25500000,
                "total_tagihan_tertunggak": 8500000,
                "total_kas_keluar": 12000000
            },
            "grafik_kehadiran_hari_ini": {
                "hadir": 1200,
                "izin": 30,
                "sakit": 15,
                "alpha": 5
            }
        }

        resp.text = json.dumps({
            "status": "success",
            "message": "Data dashboard lengkap berhasil diambil",
            "data": data
        })
        resp.status = falcon.HTTP_200
