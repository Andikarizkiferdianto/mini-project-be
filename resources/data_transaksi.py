import falcon
from pony.orm import db_session
from models.schema import db


class DataTransaksiResource:
    @db_session
    def on_get(self, req, resp):
        try:
            # Ambil filter dari query params
            ta_id = req.get_param('ta_id')
            bulan = req.get_param('bulan')

            # Query SQL Native tanpa kolom admin/petugas
            sql = sql = "SELECT bt.id, bt.tanggal_bayar, s.nis, s.nama as nama_siswa, k.nama_kelas, jp.nama_pembayaran, bt.nominal, bt.keterangan FROM bayar_tagihan bt JOIN siswa s ON bt.siswa = s.id JOIN kelas k ON s.kelas = k.id JOIN jenis_pembayaran jp ON bt.jenis_pembayaran = jp.id"

            conditions = []
            params = {}

            if ta_id:
                conditions.append("jp.tahun_ajaran = $ta_id")
                params['ta_id'] = ta_id

            if bulan:
                conditions.append("MONTH(bt.tanggal_bayar) = $bulan")
                params['bulan'] = bulan

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " ORDER BY bt.tanggal_bayar DESC"

            data_raw = db.select(sql, params)
            results = []

            for i, row in enumerate(data_raw, 1):
                results.append({
                    "no": i,
                    "tanggal": row[1].strftime('%d/%m/%Y') if row[1] else "-",
                    "status": "Sukses",
                    "nis": row[2],
                    "nama_lengkap": row[3],
                    "kelas": row[4],
                    "kwitansi": f"INV-{row[0]:05d}",
                    "jenis": row[5],
                    "nominal": float(row[6]),
                    "keterangan": row[7] or "-",
                    "petugas": "Administrator",  # Kita hardcode aja biar UI-nya gak kosong
                    "metode": "Tunai"
                })

            resp.status = falcon.HTTP_200
            resp.media = {"status": "success", "data": results}

        except Exception as e:
            print(f"Error Data Transaksi: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}