import json
import falcon
from pony.orm import db_session, commit
from models.schema import JenisSemester

class JenisSemesterResource:
    @db_session
    def on_get(self, req, resp):
        # Query sudah benar pakai [:]
        js = JenisSemester.select()[:]
        data = [{"id": j.id, "nama": j.nama} for j in js]
        resp.status = falcon.HTTP_200
        resp.media = {"data": data} # Pakai resp.media lebih simple

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            JenisSemester(nama=payload.get('nama'))
            commit()
            resp.status = falcon.HTTP_201
            resp.media = {"message": "Jenis Semester berhasil ditambah!"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}

class JenisSemesterDetailResource:
    @db_session
    def on_put(self, req, resp, js_id):
        try:
            js = JenisSemester.get(id=js_id)
            if not js:
                resp.status = falcon.HTTP_404
                resp.media = {"message": "Data tidak ditemukan"}
                return

            payload = json.loads(req.stream.read(req.content_length or 0))
            js.nama = payload.get("nama", js.nama)
            commit()

            resp.status = falcon.HTTP_200
            resp.media = {"message": "Jenis Semester berhasil diupdate!"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"message": str(e)}

    @db_session
    def on_delete(self, req, resp, js_id):
        try:
            js = JenisSemester.get(id=js_id)
            if js:
                js.delete()
                commit()
                resp.media = {"message": "Berhasil dihapus"}
            else:
                resp.status = falcon.HTTP_404
                resp.media = {"message": "Data tidak ditemukan"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}