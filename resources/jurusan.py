import json
import falcon
from pony.orm import db_session, select
from models.schema import Jurusan


class JurusanResource:
    @db_session
    def on_get(self, req, resp):
        semua_jurusan = Jurusan.select()[:]

        data = []
        for j in semua_jurusan:
            data.append({
                "id": j.id,
                "kode_jurusan": j.kode_jurusan,
                "nama_jurusan": j.nama_jurusan,
                "total_kelas": j.kelas.count()
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "message": "Berhasil mengambil data jurusan",
            "data": data
        })

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            kode = payload.get('kode_jurusan')
            if Jurusan.get(kode_jurusan=kode):
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({"message": f"Kode jurusan {kode} sudah ada!"})
                return

            Jurusan(
                kode_jurusan=kode,
                nama_jurusan=payload.get('nama_jurusan')
            )

            resp.status = falcon.HTTP_201
            resp.text = json.dumps({
                "message": f"Jurusan {payload.get('nama_jurusan')} berhasil ditambahkan!"
            })
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal tambah jurusan: {str(e)}"})


class JurusanWithIdResource:

    @db_session
    def on_delete(self, req, resp, jurusan_id):
        jurusan = Jurusan.get(id=jurusan_id)
        if not jurusan:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Jurusan tidak ditemukan!"})
            return

        nama = jurusan.nama_jurusan
        jurusan.delete()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": f"Jurusan {nama} berhasil dihapus!"})

    @db_session
    def on_put(self, req, resp, jurusan_id):
        jurusan = Jurusan.get(id=jurusan_id)

        if not jurusan:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Jurusan tidak ditemukan!"})
            return

        try:
            payload = json.load(req.bounded_stream)

            kode = payload.get("kode_jurusan")
            nama = payload.get("nama_jurusan")

            cek = Jurusan.get(kode_jurusan=kode)
            if cek and cek.id != jurusan.id:
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({
                    "message": f"Kode jurusan {kode} sudah digunakan!"
                })
                return

            jurusan.kode_jurusan = kode
            jurusan.nama_jurusan = nama

            resp.status = falcon.HTTP_200
            resp.text = json.dumps({
                "message": f"Jurusan {nama} berhasil diupdate!"
            })

        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({
                "message": f"Gagal update: {str(e)}"
            })