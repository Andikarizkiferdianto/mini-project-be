import json
import falcon
from pony.orm import db_session, commit
from models.schema import Ekstrakurikuler
from datetime import datetime


class EkskulResource:
    @db_session
    def on_get(self, req, resp):
        # Ambil semua data ekskul
        semua_ekskul = Ekstrakurikuler.select()[:]
        data = []

        for e in semua_ekskul:
            data.append({
                "id": e.id,
                "nama_ekskul": e.nama_ekskul,
                "pembina": e.pembina,
                "jadwal": e.jadwal or "-",
                "tanggal": e.tanggal.strftime("%d-%m-%Y") if e.tanggal else "-",
                "keterangan": e.keterangan or "-"
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"data": data})

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            # Konversi tanggal dari format frontend (biasanya YYYY-MM-DD)
            tgl_obj = None
            if payload.get('tanggal'):
                tgl_obj = datetime.strptime(payload.get('tanggal'), '%Y-%m-%d')

            Ekstrakurikuler(
                nama_ekskul=payload.get('nama_ekskul'),
                pembina=payload.get('pembina'),
                jadwal=payload.get('jadwal'),
                tanggal=tgl_obj,
                keterangan=payload.get('keterangan')
            )

            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Data Ekskul berhasil ditambah!"})

        except Exception as ex:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal simpan ekskul: {str(ex)}"})


class EkskulDetailResource:
    @db_session
    def on_delete(self, req, resp, ekskul_id):
        ekskul = Ekstrakurikuler.get(id=ekskul_id)
        if not ekskul:
            resp.status = falcon.HTTP_404
            return

        ekskul.delete()
        commit()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Ekskul berhasil dihapus!"})