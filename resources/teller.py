import falcon
from pony.orm import db_session, select, desc, count, sum as pony_sum
from models.schema import db, Tabungan, Siswa
from datetime import datetime


class TellerResource:
    @db_session
    def on_get(self, req, resp):
        q_setoran = select(t.nominal for t in Tabungan if t.jenis_transaksi == 'Setoran').sum() or 0
        q_penarikan = select(t.nominal for t in Tabungan if t.jenis_transaksi == 'Penarikan').sum() or 0

        total_saldo = float(q_setoran - q_penarikan)
        total_penabung = int(count(select(t.siswa for t in Tabungan)))

        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day, 0, 0, 0)
        end_of_day = datetime(now.year, now.month, now.day, 23, 59, 59)

        riwayat_today = select(t for t in Tabungan if t.tanggal >= start_of_day and t.tanggal <= end_of_day).order_by(
            desc(Tabungan.id))

        results = []
        for i, t in enumerate(riwayat_today, 1):
            results.append({
                "no": i,
                "nama": t.siswa.nama,
                "jenis": t.jenis_transaksi,
                "jumlah": float(t.nominal)
            })

        resp.media = {
            "summary": {
                "total_saldo": total_saldo,
                "total_penabung": total_penabung
            },
            "riwayat_hari_ini": results
        }

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            siswa = Siswa.get(nis=data['nis'])
            if not siswa:
                resp.status = falcon.HTTP_404
                resp.media = {"status": "error", "message": "NIS tidak ditemukan"}
                return

            Tabungan(
                siswa=siswa,
                jenis_transaksi=data['jenis_transaksi'],
                nominal=float(data['nominal']),
                keterangan=data.get('keterangan', '')
            )
            resp.status = falcon.HTTP_201
            resp.media = {"status": "success", "message": "Transaksi berhasil disimpan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class RiwayatTabunganResource:
    @db_session
    def on_get(self, req, resp):
        try:
            nis = req.get_param('nis')
            print(f"DEBUG: Mencari NIS {nis}")

            if not nis:
                resp.status = falcon.HTTP_400
                resp.media = {"status": "error", "message": "NIS harus diisi"}
                return

            siswa = Siswa.get(nis=nis)
            if not siswa:
                print("DEBUG: Siswa tidak ditemukan")
                resp.media = {"status": "success", "total_data": 0, "data": []}
                return

            riwayat = Tabungan.select_by_sql("SELECT * FROM tabungan WHERE siswa = $siswa.id ORDER BY tanggal DESC")
            print(f"DEBUG: Berhasil mengambil {len(riwayat)} data")

            results = []
            for t in riwayat:
                results.append({
                    "id": getattr(t, 'id', 0),
                    "tanggal": t.tanggal.isoformat() if t.tanggal else "-",
                    "jenis": str(t.jenis_transaksi),
                    "nominal": float(t.nominal or 0),
                    "keterangan": str(t.keterangan or "-")
                })

            resp.media = {
                "status": "success",
                "total_data": len(results),
                "data": results
            }
        except Exception as e:
            import traceback
            print("ERROR TRACEBACK:")
            traceback.print_exc()
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class RiwayatTransaksiGlobalResource:
    @db_session
    def on_get(self, req, resp):
        try:
            raw_start = req.get_param('start') or datetime.now().strftime('%Y-%m-%d')
            raw_end = req.get_param('end') or datetime.now().strftime('%Y-%m-%d')

            start_date = "".join(c for c in raw_start if c in "0123456789-")
            end_date = "".join(c for c in raw_end if c in "0123456789-")

            sql = "SELECT t.id, t.tanggal, t.jenis_transaksi, s.nis, s.nama, t.nominal, t.keterangan " \
                  "FROM tabungan t " \
                  "JOIN siswa s ON t.siswa = s.id " \
                  "WHERE t.tanggal BETWEEN $awal AND $akhir " \
                  "ORDER BY t.tanggal DESC"

            params = {
                "awal": f"{start_date} 00:00:00",
                "akhir": f"{end_date} 23:59:59"
            }

            riwayat = db.select(sql, params)

            results = []
            total_saldo = 0

            for row in riwayat:
                if row[2] == 'Setoran':
                    total_saldo += float(row[5])
                else:
                    total_saldo -= float(row[5])

                results.append({
                    "tanggal": row[1].isoformat() if row[1] else "-",
                    "kode_transaksi": f"TRX-{row[0]}",
                    "jenis": row[2],
                    "nis": row[3],
                    "nama": row[4],
                    "jumlah": float(row[5]),
                    "keterangan": row[6] or "-"
                })

            resp.media = {
                "status": "success",
                "filter": {"start": start_date, "end": end_date},
                "total_saldo": total_saldo,
                "data": results
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"Database Error: {str(e)}"}