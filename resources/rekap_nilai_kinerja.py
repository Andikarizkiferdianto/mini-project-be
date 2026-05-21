import falcon
from models.schema import db
from pony.orm import db_session


class RekapNilaiKinerjaResource:
    @db_session
    def on_get(self, req, resp):
        tipe = req.get_param('tipe', default='GURU').upper()
        bulan = req.get_param('bulan', default='Mei')
        tahun = int(req.get_param('tahun', default='2026'))

        try:
            # 1. Ambil indikator tanpa ORDER BY urutan (agar tidak error)
            # Pastikan nama kolom di bawah ini SAMA PERSIS dengan di database kamu
            indikators = db.select("SELECT id, nama_indikator FROM setting_indikator")

            # 2. Ambil pegawai
            pegawais = db.select("SELECT id, nama FROM guru_pegawai WHERE UPPER(tipe) = $tipe")

            # 3. Ambil nilai
            nilai_list = db.select(
                "SELECT id_guru_pegawai, id_indikator, nilai FROM nilai_kinerja WHERE bulan = $bulan AND tahun = $tahun",
                {"bulan": bulan, "tahun": tahun})

            # Mapping nilai
            map_nilai = {(n[0], n[1]): n[2] for n in nilai_list}

            rekap_data = []
            for p in pegawais:
                row = {"no": len(rekap_data) + 1, "nama_guru": p[1]}
                total = 0
                count = 0
                for ind in indikators:
                    val = map_nilai.get((p[0], ind[0]), 0)
                    row[f"ind_{ind[0]}"] = val
                    total += int(val)
                    count += 1
                row["rata_rata"] = round(total / count, 1) if count > 0 else 0
                rekap_data.append(row)

            resp.media = {
                "status": "success",
                "headers": [{"id": i[0], "title": i[1]} for i in indikators],
                "data": rekap_data
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}