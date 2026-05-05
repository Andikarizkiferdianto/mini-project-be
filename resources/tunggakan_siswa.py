import falcon
from pony.orm import db_session
from models.schema import db


class TunggakanSiswaResource:
    @db_session
    def on_get(self, req, resp):
        try:
            kelas_id = req.get_param('kelas_id')

            # Query siswa (Pakai SQL flat/satu baris biar aman)
            sql_siswa = "SELECT id, nis, nama FROM siswa"
            params = {}
            if kelas_id and kelas_id != 'semua':
                sql_siswa += " WHERE kelas = $kelas_id"
                params['kelas_id'] = kelas_id

            siswa_list = db.select(sql_siswa, params)
            results = []

            for s in siswa_list:
                s_id, nis, nama = s

                # REVISI DISINI: Query dibuat satu baris tanpa enter/spasi aneh
                sql_tunggakan = "SELECT jp.nama_pembayaran, jp.nominal_ketetapan, COALESCE(SUM(bt.nominal), 0) FROM jenis_pembayaran jp LEFT JOIN bayar_tagihan bt ON jp.id = bt.jenis_pembayaran AND bt.siswa = $s_id GROUP BY jp.id"

                detail_tagihan = db.select(sql_tunggakan, {"s_id": s_id})

                total_tunggakan_siswa = 0
                rincian = []

                for tagihan in detail_tagihan:
                    nama_jp, ketetapan, bayar = tagihan
                    sisa = float(ketetapan) - float(bayar)

                    if sisa > 0:
                        total_tunggakan_siswa += sisa
                        rincian.append({
                            "kategori": nama_jp,
                            "kurang": sisa
                        })

                if total_tunggakan_siswa > 0:
                    results.append({
                        "nis": nis,
                        "nama": nama,
                        "total_tunggakan": total_tunggakan_siswa,
                        "rincian": rincian
                    })

            resp.status = falcon.HTTP_200
            resp.media = {"status": "success", "data": results}

        except Exception as e:
            print(f"Error Tunggakan: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class ListKelasResource:
    @db_session
    def on_get(self, req, resp):
        # Untuk mengisi dropdown "Pilih Kelas"
        try:
            data = db.select("id, nama_kelas FROM kelas")
            results = [{"id": row[0], "nama": row[1]} for row in data]
            resp.media = {"status": "success", "data": results}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}