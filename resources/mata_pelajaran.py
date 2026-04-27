import json
import falcon
from pony.orm import db_session, commit
from models.schema import MataPelajaran

class MataPelajaranResource:
    @db_session
    def on_get(self, req, resp):
        mapels = MataPelajaran.select()
        result = [{"id": m.id, "nama_mapel": m.nama_mapel} for m in mapels]
        resp.text = json.dumps(result)

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            mapel = MataPelajaran(nama_mapel=payload.get('nama_mapel'))
            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Berhasil!", "id": mapel.id})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})

class MataPelajaranDetailResource:
    @db_session
    def on_put(self, req, resp, mp_id):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            mapel = MataPelajaran.get(id=mp_id)
            if not mapel:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"error": "Data tidak ditemukan!"})
                return

            mapel.nama_mapel = payload.get('nama_mapel')
            commit()
            resp.text = json.dumps({"message": "Data berhasil diupdate!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})

    @db_session
    def on_delete(self, req, resp, mp_id):
        try:
            mapel = MataPelajaran.get(id=mp_id)
            if not mapel:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"error": "Data tidak ditemukan!"})
                return

            mapel.delete()
            commit()
            resp.text = json.dumps({"message": "Data berhasil dihapus!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})