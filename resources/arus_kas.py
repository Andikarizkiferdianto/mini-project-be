import falcon
from models.schema import db
from pony.orm import db_session
import traceback


class ArusKasResource:
    @db_session
    def on_get(self, req, resp):
        tgl_awal = req.get_param('start')
        tgl_akhir = req.get_param('end')

        if not tgl_awal or not tgl_akhir:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": "Parameter 'start' dan 'end' wajib diisi"}
            return

        try:
            sql = """SELECT 
j.tanggal, 
j.keterangan, 
j.kode_akun, 
j.nama_akun,
j.debet, 
j.kredit
FROM jurnal j
WHERE j.tanggal >= $tgl_awal AND j.tanggal <= $tgl_akhir
ORDER BY j.tanggal ASC"""

            result = db.select(sql)

            arus_operasi = []
            arus_investasi = []
            arus_pendanaan = []

            total_operasi = 0
            total_investasi = 0
            total_pendanaan = 0

            for row in result:
                kode = row[2]
                nama = row[3]
                debet = float(row[4] or 0)
                kredit = float(row[5] or 0)
                nilai = debet - kredit

                if nilai == 0: continue

                if kode.startswith('4') or kode.startswith('5'):
                    total_operasi += nilai
                    arus_operasi.append({"keterangan": row[1], "jumlah": nilai})
                elif kode.startswith('12'):
                    total_investasi += nilai
                    arus_investasi.append({"keterangan": row[1], "jumlah": nilai})
                elif kode.startswith('2') or kode.startswith('3'):
                    total_pendanaan += nilai
                    arus_pendanaan.append({"keterangan": row[1], "jumlah": nilai})

            resp.media = {
                "status": "success",
                "periode": f"{tgl_awal} s/d {tgl_akhir}",
                "data": {
                    "operasi": {
                        "items": arus_operasi,
                        "total": total_operasi
                    },
                    "investasi": {
                        "items": arus_investasi,
                        "total": total_investasi
                    },
                    "pendanaan": {
                        "items": arus_pendanaan,
                        "total": total_pendanaan
                    },
                    "kenaikan_penurunan_kas": total_operasi + total_investasi + total_pendanaan
                }
            }
        except Exception as e:
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}