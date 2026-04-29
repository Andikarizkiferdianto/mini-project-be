import json
import falcon
from pony.orm import db_session, commit
from models.schema import AspekPenilaian


class AspekResource:
    @db_session
    def on_get(self, req, resp):
        aspek_list = AspekPenilaian.select()[:]
        data = []
        for a in aspek_list:
            data.append({
                "id": a.id,
                "nama_aspek": a.nama_aspek,
                "keterangan": a.keterangan or "-",
                "can_edit": a.can_edit
            })
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"data": data})

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            AspekPenilaian(
                nama_aspek=payload.get('nama_aspek'),
                keterangan=payload.get('keterangan'),
                can_edit=payload.get('can_edit', True)
            )
            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Aspek Penilaian berhasil ditambah!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": str(e)})


class AspekDetailResource:

    @db_session
    def on_put(self, req, resp, aspek_id):
        try:
            aspek = AspekPenilaian.get(id=aspek_id)

            if not aspek:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"message": "Data tidak ditemukan"})
                return

            if not aspek.can_edit:
                resp.status = falcon.HTTP_403
                resp.text = json.dumps({"message": "Data ini dikunci (tidak bisa diedit)!"})
                return

            payload = json.loads(req.stream.read(req.content_length or 0))

            aspek.nama_aspek = payload.get("nama_aspek", aspek.nama_aspek)
            aspek.keterangan = payload.get("keterangan", aspek.keterangan)

            commit()

            resp.status = falcon.HTTP_200
            resp.text = json.dumps({"message": "Aspek berhasil diupdate!"})

        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": str(e)})


    @db_session
    def on_delete(self, req, resp, aspek_id):
        aspek = AspekPenilaian.get(id=aspek_id)
        if not aspek:
            resp.status = falcon.HTTP_404
            return

        if not aspek.can_edit:
            resp.status = falcon.HTTP_403
            resp.text = json.dumps({"message": "Data ini dikunci (tidak bisa dihapus)!"})
            return

        aspek.delete()
        commit()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Aspek berhasil dihapus!"})