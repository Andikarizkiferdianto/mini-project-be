import json
import falcon
from pony.orm import db_session, commit, rollback
from models.schema import Siswa, Kelas, TahunAjaran


def set_cors_headers(resp):
    resp.set_header("Access-Control-Allow-Origin", "*")
    resp.set_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    resp.set_header("Access-Control-Allow-Headers", "Content-Type")


class KenaikanKelasResource:

    @db_session
    def on_post(self, req, resp):
        try:
            raw = req.stream.read(req.content_length or 0)
            payload = json.loads(raw) if raw else {}

            tahun_id = payload.get("tahun_ajaran")
            kelas_tujuan = payload.get("kelas_tujuan")
            siswa_list = payload.get("siswa", [])

            # VALIDASI
            if not tahun_id or not kelas_tujuan or len(siswa_list) == 0:
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({
                    "message": "Data tidak lengkap!"
                })
                return

            # ambil objek
            kelas_tujuan_obj = Kelas.get(id=kelas_tujuan)
            tahun_obj = TahunAjaran.get(id=tahun_id)

            if not kelas_tujuan_obj or not tahun_obj:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({
                    "message": "Data kelas/tahun tidak ditemukan!"
                })
                return

            updated = []

            for s in siswa_list:
                siswa = Siswa.get(id=s.get("id"))

                if siswa:
                    siswa.kelas = kelas_tujuan_obj
                    siswa.tahun_ajaran = tahun_obj.nama   # ✅ FIX DISINI
                    updated.append(siswa.nama)

            commit()

            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "message": "Kenaikan kelas berhasil!",
                "total": len(updated),
                "siswa": updated
            })

        except Exception as e:
            rollback()
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({
                "message": "Gagal proses kenaikan",
                "error": str(e)
            })

        set_cors_headers(resp)
    def on_options(self, req, resp):
        resp.status = falcon.HTTP_200
        set_cors_headers(resp)