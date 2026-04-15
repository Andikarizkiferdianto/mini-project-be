import json
import falcon
from pony.orm import db_session, select
from models.schema import Absensi, Siswa
from datetime import datetime


class AbsensiResource:
    @db_session
    def on_get(self, req, resp):
        absensi_list = select(a for a in Absensi).order_by(desc(Absensi.tanggal))[:]

        data = [a.to_response() for a in absensi_list]

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "message": "Berhasil mengambil data absensi",
            "data": data
        })

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            siswa_obj = Siswa.get(nis=payload.get('nis'))

            if not siswa_obj:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"message": "Siswa tidak ditemukan!"})
                return

            Absensi(
                siswa=siswa_obj,
                tanggal=datetime.now(),
                status_hadir=payload.get('status'),
                jam_masuk=datetime.now().strftime("%H:%M"),
                keterangan=payload.get('keterangan', '')
            )

            resp.status = falcon.HTTP_201
            resp.text = json.dumps({
                "message": f"Absensi untuk {siswa_obj.nama} berhasil dicatat!"
            })
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal catat absensi: {str(e)}"})