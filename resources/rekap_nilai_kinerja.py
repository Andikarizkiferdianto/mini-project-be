import falcon
from models.schema import db
from pony.orm import db_session


class RekapNilaiKinerjaResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil data rekapitulasi nilai kinerja berbentuk flat array untuk Datatables"""
        tipe = req.get_param('tipe', default='GURU').strip().upper()
        bulan = req.get_param('bulan', default='May').strip()
        tahun = req.get_param('tahun', default='2026').strip()

        try:
            sql_indikator = "SELECT id, nama_indikator FROM setting_indikator ORDER BY urutan ASC"
            indikators = db.select(sql_indikator)

            sql_pegawai = "SELECT id, nama FROM guru_pegawai WHERE UPPER(tipe) = $tipe ORDER BY id ASC"
            pegawais = db.select(sql_pegawai)

            sql_nilai = "SELECT id_guru_pegawai, id_indikator, nilai FROM nilai_kinerja WHERE bulan = $bulan AND tahun = $tahun"
            nilai_list = db.select(sql_nilai, {"bulan": bulan, "tahun": int(tahun)})

            map_nilai = {(n[0], n[1]): float(n[2]) for n in nilai_list}

            rekap_data = []
            for idx, p in enumerate(pegawais, start=1):
                id_guru = p[0]
                nama_guru = p[1]

                row = {
                    "no": idx,
                    "nama_guru": nama_guru
                }

                for ind in indikators:
                    id_ind = ind[0]
                    nama_ind_key = ind[1].lower().replace(" ", "_").replace("&", "dan")

                    nilai_v = map_nilai.get((id_guru, id_ind), "-")
                    row[nama_ind_key] = nilai_v

                rekap_data.append(row)

            list_header = [{"title": ind[1], "data": ind[1].lower().replace(" ", "_").replace("&", "dan")} for ind in
                           indikators]

            resp.media = {
                "status": "success",
                "headers": list_header,
                "data": rekap_data
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}