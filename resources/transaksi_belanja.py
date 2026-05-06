import falcon
from pony.orm import db_session
from models.schema import db, TransaksiBelanja
from datetime import datetime


class TransaksiBelanjaResource:
    @db_session
    def on_get(self, req, resp):
        try:
            sql = "SELECT id, jenis_belanja, bidang, penerima, sumber, tanggal, menyetujui, nominal, keterangan " \
                  "FROM transaksi_belanja ORDER BY id DESC"
            data_belanja = db.select(sql)

            results = []
            total_nominal = 0
            for b in data_belanja:
                total_nominal += float(b[7])
                results.append({
                    "id": b[0],
                    "kode_transaksi": f"BLJ{b[5].strftime('%Y%m%d')}{b[0]}",
                    "jenis_belanja": b[1],
                    "bidang": b[2],
                    "penerima": b[3],
                    "sumber": b[4],
                    "tanggal": b[5].isoformat(),
                    "menyetujui": b[6],
                    "nominal": float(b[7]),
                    "keterangan": b[8] or "-"
                })

            resp.media = {
                "status": "success",
                "total_nominal": total_nominal,
                "data": results
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            tgl_obj = datetime.strptime(data['tanggal'], '%Y-%m-%d')
            TransaksiBelanja(
                jenis_belanja=data['jenis_belanja'],
                bidang=data['bidang'],
                penerima=data['penerima'],
                sumber=data['sumber'],
                tanggal=tgl_obj,
                menyetujui=data['menyetujui'],
                nominal=float(data['nominal']),
                keterangan=data.get('keterangan', '')
            )
            resp.status = falcon.HTTP_201
            resp.media = {"status": "success", "message": "Transaksi belanja berhasil disimpan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class TransaksiBelanjaDetailResource:
    @db_session
    def on_put(self, req, resp, id):
        """Fitur EDIT menggunakan TransaksiBelanja"""
        data = req.media
        try:
            b = TransaksiBelanja.get(id=id)
            if not b:
                resp.status = falcon.HTTP_404
                resp.media = {"status": "error", "message": "Data tidak ditemukan"}
                return

            if 'jenis_belanja' in data: b.jenis_belanja = data['jenis_belanja']
            if 'bidang' in data: b.bidang = data['bidang']
            if 'penerima' in data: b.penerima = data['penerima']
            if 'sumber' in data: b.sumber = data['sumber']
            if 'menyetujui' in data: b.menyetujui = data['menyetujui']
            if 'nominal' in data: b.nominal = float(data['nominal'])
            if 'keterangan' in data: b.keterangan = data['keterangan']
            if 'tanggal' in data:
                b.tanggal = datetime.strptime(data['tanggal'], '%Y-%m-%d')

            resp.media = {"status": "success", "message": "Data belanja berhasil diperbarui"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        """Fitur DELETE menggunakan TransaksiBelanja"""
        try:
            b = TransaksiBelanja.get(id=id)
            if not b:
                resp.status = falcon.HTTP_404
                resp.media = {"status": "error", "message": "Data tidak ditemukan"}
                return

            b.delete()
            resp.media = {"status": "success", "message": "Data belanja berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}