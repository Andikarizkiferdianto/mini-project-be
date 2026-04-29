import json
import falcon
from pony.orm import db_session, commit
from models.schema import TahunAjaran


def set_cors_headers(resp):
    resp.set_header("Access-Control-Allow-Origin", "*")
    resp.set_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    resp.set_header("Access-Control-Allow-Headers", "Content-Type")


class TahunAjaranResource:

    @db_session
    def on_get(self, req, resp):
        tas = TahunAjaran.select()[:]
        data = []
        for t in tas:
            data.append({
                "id": t.id,
                "nama": t.nama,
                "tahun": t.tahun,
                "is_active": t.is_active
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"data": data})
        set_cors_headers(resp)

    @db_session
    def on_post(self, req, resp):
        try:
            raw = req.stream.read(req.content_length or 0)
            payload = json.loads(raw) if raw else {}

            nama = payload.get("nama")
            tahun = payload.get("tahun")

            if not nama or not tahun:
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({"message": "nama dan tahun wajib diisi"})
                return

            ta = TahunAjaran(
                nama=str(nama),
                tahun=str(tahun),
                is_active=bool(payload.get("is_active", False))
            )

            commit()

            resp.status = falcon.HTTP_201
            resp.text = json.dumps({
                "message": "Tahun Ajaran berhasil dibuat!",
                "id": ta.id
            })

        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({
                "message": "Gagal menyimpan data",
                "error": str(e)
            })

    def on_options(self, req, resp):
        resp.status = falcon.HTTP_200
        set_cors_headers(resp)


class TahunAjaranWithIdResource:

    @db_session
    def on_delete(self, req, resp, ta_id):
        ta = TahunAjaran.get(id=ta_id)

        if not ta:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Data tidak ditemukan"})
            return

        ta.delete()
        commit()

        resp.text = json.dumps({"message": "Berhasil dihapus"})

    @db_session
    def on_put(self, req, resp, ta_id):
        ta = TahunAjaran.get(id=ta_id)

        if not ta:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Data tidak ditemukan"})
            return

        try:
            raw = req.stream.read(req.content_length or 0)
            payload = json.loads(raw) if raw else {}

            if "nama" in payload:
                ta.nama = str(payload["nama"])

            if "tahun" in payload:
                ta.tahun = str(payload["tahun"])

            if "is_active" in payload:
                ta.is_active = bool(payload["is_active"])

            commit()

            resp.text = json.dumps({
                "message": "Berhasil diupdate"
            })

        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({
                "message": "Gagal update",
                "error": str(e)
            })

    def on_options(self, req, resp, ta_id=None):
        resp.status = falcon.HTTP_200
        set_cors_headers(resp)

class TahunAjaranActiveResource:

    @db_session
    def on_get(self, req, resp):
        tas = TahunAjaran.select(lambda t: t.is_active == True)[:]

        data = []
        for t in tas:
            data.append({
                "id": t.id,
                "nama": t.nama,
                "tahun": t.tahun,
                "is_active": True
            })

        resp.text = json.dumps({"data": data})
        set_cors_headers(resp)