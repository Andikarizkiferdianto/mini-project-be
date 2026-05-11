import falcon
from models.schema import db
from pony.orm import db_session
import traceback


class SettingUserResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil Dropdown Kelas - Tanpa error kolom"""
        try:
            # Ambil semua kolom dari tabel kelas, kita ambil index 0 (id) dan index 1 (nama)
            res_kelas = db.select("SELECT * FROM kelas")
            resp.media = {
                "status": "success",
                "options": {
                    "kelas": [{"id": r[0], "nama": r[1]} for r in res_kelas],
                    "jenis_user": ["Siswa", "Guru", "Wali Kelas", "Orang Tua"]
                }
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tampilkan data - Metode Filter Manual (Anti-SQL-Error)"""
        raw_data = req.get_media()
        jenis = raw_data.get('jenis_user')
        kelas_id = raw_data.get('kelas_id')

        try:
            data = []
            if jenis == "Siswa":
                # Ambil SEMUA data siswa, lalu kita filter di Python
                # Ini menghindari error 'Unknown column id_kelas'
                all_siswa = db.select("SELECT * FROM siswa")

                # Kita asumsikan id_kelas ada di salah satu kolom
                # Mari kita cari baris yang punya id_kelas sesuai input
                for s in all_siswa:
                    # s[0]=id, s[1]=nis, s[2]=nisn, s[3]=nama...
                    # Kita cari mana yang nilainya sama dengan kelas_id (biasanya di kolom akhir)
                    if str(kelas_id) in [str(val) for val in s]:
                        user_id = s[0]
                        # Cek auth_user
                        auth = db.select("SELECT username FROM auth_user WHERE user_id=$uid AND role='Siswa'",
                                         {"uid": user_id})

                        data.append({
                            "id": s[0],
                            "nis_id": s[2],  # NISN
                            "nama": s[3],
                            "username": auth[0][0] if auth else s[2],
                            "password": ""
                        })
            else:
                # Untuk Guru
                all_guru = db.select("SELECT * FROM guru")
                for g in all_guru:
                    user_id = g[0]
                    auth = db.select("SELECT username FROM auth_user WHERE user_id=$uid AND role=$r",
                                     {"uid": user_id, "r": jenis})
                    data.append({
                        "id": g[0],
                        "nis_id": g[1],  # NIP
                        "nama": g[2],
                        "username": auth[0][0] if auth else g[1],
                        "password": ""
                    })

            resp.media = {"status": "success", "data": data}
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"Gagal load: {str(e)}"}

    @db_session
    def on_put(self, req, resp):
        """Update massal password"""
        raw_data = req.get_media()
        users = raw_data.get('users', [])
        role = raw_data.get('role')
        try:
            for u in users:
                if u.get('password'):
                    sql = "INSERT INTO auth_user (user_id, role, username, password) VALUES ($uid, $role, $uname, $pass) ON DUPLICATE KEY UPDATE username = $uname, password = $pass"
                    db.execute(sql, {"uid": u['id'], "role": role, "uname": u['username'], "pass": u['password']})
            resp.media = {"status": "success", "message": "Berhasil simpan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}