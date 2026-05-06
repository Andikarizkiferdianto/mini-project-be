import falcon
from pony.orm import db_session, select, desc
from models.schema import db, Penerimaan
from datetime import datetime


class TransaksiPenerimaanResource:
    @db_session
    def on_get(self, req, resp):
        try:
            sql = "SELECT id, jenis_penerimaan, sumber, nominal, tanggal, menyetujui, keterangan " \
                  "FROM penerimaan ORDER BY id DESC"

            data_penerimaan = db.select(sql)

            results = []
            total_all = 0

            for p in data_penerimaan:
                total_all += float(p[3])
                results.append({
                    "id": p[0],
                    "kode_transaksi": f"TRX{p[4].strftime('%Y%m%d')}{p[0]}",
                    "jenis_penerimaan": p[1],
                    "sumber": p[2],
                    "tanggal": p[4].isoformat(),
                    "nominal": float(p[3]),
                    "menyetujui": p[5] or "-",
                    "keterangan": p[6] or "-"
                })

            resp.media = {
                "status": "success",
                "total_nominal": total_all,
                "data": results
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"SQL Error: {str(e)}"}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            tgl_str = data.get('tanggal')
            tgl_obj = datetime.strptime(tgl_str, '%Y-%m-%d').date() if tgl_str else datetime.now().date()

            Penerimaan(
                jenis_penerimaan=data['jenis_penerimaan'],
                sumber=data['sumber'],
                nominal=float(data['nominal']),
                tanggal=tgl_obj,
                menyetujui=data.get('menyetujui', ''),
                keterangan=data.get('keterangan', '')
            )

            resp.status = falcon.HTTP_201
            resp.media = {"status": "success", "message": "Transaksi berhasil disimpan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class TransaksiPenerimaanDetailResource:
    @db_session
    def on_put(self, req, resp, id):
        """Fitur EDIT Data"""
        data = req.media
        try:
            p = Penerimaan.get(id=id)
            if not p:
                resp.status = falcon.HTTP_404
                resp.media = {"status": "error", "message": "Data tidak ditemukan"}
                return

            if 'jenis_penerimaan' in data: p.jenis_penerimaan = data['jenis_penerimaan']
            if 'sumber' in data: p.sumber = data['sumber']
            if 'nominal' in data: p.nominal = float(data['nominal'])
            if 'menyetujui' in data: p.menyetujui = data['menyetujui']
            if 'keterangan' in data: p.keterangan = data['keterangan']
            if 'tanggal' in data:
                p.tanggal = datetime.strptime(data['tanggal'], '%Y-%m-%d').date()

            resp.media = {"status": "success", "message": "Data berhasil diperbarui"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        """Fitur DELETE Data"""
        try:
            p = Penerimaan.get(id=id)
            if not p:
                resp.status = falcon.HTTP_404
                resp.media = {"status": "error", "message": "Data tidak ditemukan"}
                return

            p.delete()
            resp.media = {"status": "success", "message": "Data berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}