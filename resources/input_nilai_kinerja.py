import falcon
from models.schema import db
from pony.orm import db_session


class InputNilaiKinerjaResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil data matriks nilai kinerja untuk tabel frontend"""
        tipe = req.get_param('tipe', default='GURU').upper()  # GURU atau PEGAWAI
        bulan = req.get_param('bulan', default='May')
        tahun = req.get_param('tahun', default='2026')

        try:
            sql_indikator = "SELECT id, nama_indikator FROM setting_indikator ORDER BY urutan ASC"
            indikators = db.select(sql_indikator)

            sql_pegawai = "SELECT id, nama FROM guru_pegawai WHERE tipe = $tipe ORDER BY id ASC"
            pegawais = db.select(sql_pegawai)

            sql_nilai = "SELECT id_guru_pegawai, id_indikator, nilai FROM nilai_kinerja WHERE bulan = $bulan AND tahun = $tahun"
            nilai_list = db.select(sql_nilai, {"bulan": bulan, "tahun": int(tahun)})

            map_nilai = {(n[0], n[1]): float(n[2]) for n in nilai_list}

            matriks_data = []
            for p in pegawais:
                id_guru = p[0]
                nama_guru = p[1]

                nilai_indikator_obj = {}
                for ind in indikators:
                    id_ind = ind[0]
                    nama_ind = ind[1].lower().replace(" ", "_")

                    nilai_indikator_obj[nama_ind] = {
                        "id_indikator": id_ind,
                        "nilai": map_nilai.get((id_guru, id_ind), 0.0)
                    }

                matriks_data.append({
                    "id_guru_pegawai": id_guru,
                    "nama_guru": nama_guru,
                    "nilai_kinerja": nilai_indikator_obj
                })

            list_header = [{"id": ind[0], "nama": ind[1], "key": ind[1].lower().replace(" ", "_")} for ind in
                           indikators]

            resp.media = {
                "status": "success",
                "headers": list_header,
                "data": matriks_data
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Simpan atau Update (Upsert) menggunakan ORM Object"""
        try:
            raw_data = req.get_media()
            id_guru = raw_data.get('id_guru_pegawai')
            bulan = raw_data.get('bulan', 'May')
            tahun = raw_data.get('tahun', 2026)
            scores = raw_data.get('scores')

            if not id_guru or not scores:
                resp.status = falcon.HTTP_400
                resp.media = {"status": "error", "message": "Data id_guru_pegawai dan scores wajib diisi"}
                return

            clean_id_guru = int(id_guru)
            clean_tahun = int(tahun)
            clean_bulan = str(bulan).strip()

            for id_indikator, nilai in scores.items():
                clean_id_ind = int(id_indikator)
                clean_nilai = float(nilai)

                # Cari data menggunakan model Entity Pony ORM secara murni
                item_eksis = db.NilaiKinerja.get(
                    id_guru_pegawai=clean_id_guru,
                    id_indikator=clean_id_ind,
                    bulan=clean_bulan,
                    tahun=clean_tahun
                )

                if item_eksis:
                    # Update nilai jika sudah ada
                    item_eksis.nilai = clean_nilai
                else:
                    # Insert baru jika belum ada
                    db.NilaiKinerja(
                        id_guru_pegawai=clean_id_guru,
                        id_indikator=clean_id_ind,
                        bulan=clean_bulan,
                        tahun=clean_tahun,
                        nilai=clean_nilai
                    )

            resp.media = {"status": "success", "message": "Nilai kinerja berhasil disimpan!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}