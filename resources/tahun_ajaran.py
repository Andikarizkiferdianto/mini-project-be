import json
import falcon
from pony.orm import db_session, commit
from models.schema import TahunAjaran

class TahunAjaranResource:
    @db_session
    def on_get(self, req, resp):
        tas = TahunAjaran.select()[:]
        data = [t.to_dict() for t in tas]
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"data": data})

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            ta = TahunAjaran(
                tahun=payload.get('tahun'),
                nama=payload.get('nama'),
                is_active=payload.get('is_active', False)
            )
            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({
                "message": "Tahun Ajaran berhasil dibuat!",
                "id": ta.id
            })
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})

class TahunAjaranWithIdResource:
    @db_session
    def on_delete(self, req, resp, ta_id):
        ta = TahunAjaran.get(id=ta_id)
        if ta:
            ta.delete()
            commit()
            resp.text = json.dumps({"message": "Berhasil dihapus"})
        else:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Data tidak ketemu"})