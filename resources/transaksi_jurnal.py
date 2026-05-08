import falcon
from models.schema import Jurnal, JenisBelanja
from pony.orm import db_session, select


class TransaksiJurnalResource:
    @db_session
    def on_get(self, req, resp):
        try:
            query = Jurnal.select()
            data = []
            for j in query:
                data.append({
                    "id": j.id,
                    "tanggal": str(j.tanggal),
                    "keterangan": j.keterangan or "",
                    "kode_akun": j.kode_akun,
                    "nama_akun": j.nama_akun,
                    "debet": float(j.debet),
                    "kredit": float(j.kredit),
                    "status": j.status
                })

            resp.media = {
                "status": "success",
                "data": data
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            Jurnal(
                tanggal=data.get('tanggal'),
                keterangan=data.get('keterangan', ''),
                kode_akun=data.get('kode_akun'),
                nama_akun=data.get('nama_akun'),
                debet=float(data.get('debet', 0)),
                kredit=float(data.get('kredit', 0)),
                status=data.get('status', 'Posting')
            )
            resp.status = falcon.HTTP_201
            resp.media = {
                "status": "success",
                "message": "Transaksi jurnal berhasil disimpan"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class AkunJurnalOptionResource:
    @db_session
    def on_get(self, req, resp):
        try:
            akun_query = JenisBelanja.select()

            options = []
            for a in akun_query:
                options.append({
                    "kode_akun": a.kode_akun,
                    "nama_akun": a.nama_akun,
                    "display": f"{a.kode_akun} - {a.nama_akun}"
                })

            resp.media = {
                "status": "success",
                "data": options
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}