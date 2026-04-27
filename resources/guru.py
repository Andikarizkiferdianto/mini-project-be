import json
import falcon
from pony.orm import db_session, commit
from models.schema import Guru

class GuruResource:
    @db_session
    def on_get(self, req, resp):
        gurus = Guru.select()
        result = [{"id": g.id, "nama": g.nama, "nip": g.nip} for g in gurus]
        resp.text = json.dumps(result)

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            guru = Guru(nama=payload.get('nama'), nip=payload.get('nip'))
            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Guru berhasil ditambah!", "id": guru.id})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})


class GuruDetailResource:
    @db_session
    def on_put(self, req, resp, g_id):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            guru = Guru.get(id=g_id)

            if not guru:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"error": "Guru tidak ditemukan!"})
                return

            if 'nama' in payload: guru.nama = payload['nama']
            if 'nip' in payload: guru.nip = payload['nip']

            commit()
            resp.text = json.dumps({"message": "Data guru berhasil diupdate!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})

    @db_session
    def on_delete(self, req, resp, g_id):
        try:
            guru = Guru.get(id=g_id)
            if not guru:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"error": "Guru tidak ditemukan!"})
                return

            guru.delete()
            commit()
            resp.text = json.dumps({"message": "Guru berhasil dihapus!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": "Gagal menghapus! Guru mungkin masih terikat dengan jadwal mengajar."})