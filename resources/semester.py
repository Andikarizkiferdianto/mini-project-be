import json
import falcon
from pony.orm import db_session, commit
from models.schema import Semester, TahunAjaran


def set_cors_headers(resp):
    resp.set_header("Access-Control-Allow-Origin", "*")
    resp.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    resp.set_header("Access-Control-Allow-Headers", "Content-Type")


class SemesterResource:
    @db_session
    def on_get(self, req, resp):
        semua_semester = Semester.select()[:]
        data = []

        for s in semua_semester:
            data.append({
                "id": s.id,
                "id_tahun_ajaran": s.tahun_ajaran.id,
                # --- UBAH BARIS INI ---
                "tahun_ajaran": s.tahun_ajaran.nama,
                # ----------------------
                "jenis_semester": s.jenis_semester,
                "nama_semester": s.nama_semester
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"data": data})
        set_cors_headers(resp)

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            ta = TahunAjaran.get(id=payload.get('id_tahun_ajaran'))
            if not ta:
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({"message": "Tahun Ajaran tidak ditemukan!"})
                set_cors_headers(resp)
                return

            Semester(
                tahun_ajaran=ta,
                jenis_semester=payload.get('jenis_semester'),
                nama_semester=payload.get('nama_semester')
            )

            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Data Semester berhasil ditambah!"})
            set_cors_headers(resp)

        except Exception as ex:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal simpan: {str(ex)}"})
            set_cors_headers(resp)

    def on_options(self, req, resp):
        resp.status = falcon.HTTP_200
        set_cors_headers(resp)


class SemesterDetailResource:

    @db_session
    def on_put(self, req, resp, semester_id):
        sem = Semester.get(id=semester_id)

        if not sem:
            resp.status = falcon.HTTP_404
            set_cors_headers(resp)
            return

        payload = json.loads(req.stream.read(req.content_length or 0))

        ta = TahunAjaran.get(id=payload.get('id_tahun_ajaran'))

        sem.tahun_ajaran = ta
        sem.jenis_semester = payload.get('jenis_semester')
        sem.nama_semester = payload.get('nama_semester')

        commit()

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Semester berhasil diupdate!"})
        set_cors_headers(resp)

    @db_session
    def on_delete(self, req, resp, semester_id):
        sem = Semester.get(id=semester_id)
        if not sem:
            resp.status = falcon.HTTP_404
            set_cors_headers(resp)
            return

        sem.delete()
        commit()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Semester berhasil dihapus!"})
        set_cors_headers(resp)

    def on_options(self, req, resp, semester_id=None):
        resp.status = falcon.HTTP_200
        set_cors_headers(resp)
