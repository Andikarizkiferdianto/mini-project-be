import falcon
import json
from models.schema import Jurnal
from pony.orm import db_session, commit, rollback
from datetime import datetime
import traceback


class LaporanJurnalResource:

    @db_session
    def on_get(self, req, resp):

        tgl_awal = req.get_param('start')
        tgl_akhir = req.get_param('end')

        if not tgl_awal or not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {
                "status": "error",
                "message": "Parameter tanggal wajib diisi"
            }
            return

        try:

            data_jurnal = Jurnal.select(
                lambda j:
                str(j.tanggal) >= tgl_awal and
                str(j.tanggal) <= tgl_akhir
            ).order_by(Jurnal.tanggal)

            data = []

            for j in data_jurnal:
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
                "total_data": len(data),
                "data": data
            }

        except Exception as e:

            print(traceback.format_exc())

            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": str(e)
            }


class LaporanJurnalDetailResource:

    @db_session
    def on_put(self, req, resp, jurnal_id):

        try:

            payload = json.loads(
                req.stream.read(req.content_length or 0)
            )

            jurnal = Jurnal.get(id=jurnal_id)

            if not jurnal:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": "error",
                    "message": "Data jurnal tidak ditemukan"
                }
                return

            # UPDATE
            if payload.get("tanggal"):
                jurnal.tanggal = datetime.strptime(
                    payload.get("tanggal"),
                    "%Y-%m-%d"
                ).date()

            jurnal.keterangan = payload.get("keterangan", "")
            jurnal.kode_akun = payload.get("kode_akun", "")
            jurnal.nama_akun = payload.get("nama_akun", "")
            jurnal.debet = float(payload.get("debet", 0))
            jurnal.kredit = float(payload.get("kredit", 0))
            jurnal.status = payload.get("status", "Posting")

            commit()

            resp.media = {
                "status": "success",
                "message": "Jurnal berhasil diupdate"
            }

        except Exception as e:

            rollback()

            print(traceback.format_exc())

            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_delete(self, req, resp, jurnal_id):

        try:

            jurnal = Jurnal.get(id=jurnal_id)

            if not jurnal:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "status": "error",
                    "message": "Data jurnal tidak ditemukan"
                }
                return

            jurnal.delete()

            commit()

            resp.media = {
                "status": "success",
                "message": "Jurnal berhasil dihapus"
            }

        except Exception as e:

            rollback()

            print(traceback.format_exc())

            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": str(e)
            }
