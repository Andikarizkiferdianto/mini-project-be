import falcon
from models.schema import db
from pony.orm import db_session

class InputNilaiKinerjaResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil data matriks nilai kinerja untuk tabel frontend"""
        # Menangkap parameter filter tipe (GURU / PEGAWAI)
        tipe = req.get_param('tipe', default='GURU').upper()
        bulan = req.get_param('bulan', default='May')
        tahun = req.get_param('tahun', default='2026')

        try:
            # 1. Ambil indikator dari setting_indikator
            sql_indikator = "SELECT id, nama_indikator FROM setting_indikator ORDER BY id ASC"
            indikators = db.select(sql_indikator)

            # 2. FIX: Diubah ke tabel 'guru_pegawai' sesuai database asli lo
            sql_pegawai = "SELECT id, nama FROM guru_pegawai WHERE UPPER(tipe) = $tipe ORDER BY id ASC"
            pegawais = db.select(sql_pegawai, {"tipe": tipe})

            # 3. Ambil nilai kinerja yang sudah terinput
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

            list_header = [{"id": ind[0], "nama": ind[1], "key": ind[1].lower().replace(" ", "_")} for ind in indikators]

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
        """Simpan atau Update (Upsert) nilai kinerja menggunakan SQL murni agar aman tanpa dependensi ORM"""
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
                clean_nilai = float(nilai) if nilai != '' else 0.0

                # Menggunakan INSERT ON DUPLICATE KEY UPDATE agar otomatis insert baru / update data lama
                sql_upsert = """
                    INSERT INTO nilai_kinerja (id_guru_pegawai, id_indikator, bulan, tahun, nilai)
                    VALUES ($id_guru, $id_ind, $bulan, $tahun, $nilai)
                    ON DUPLICATE KEY UPDATE nilai = $nilai
                """
                db.execute(sql_upsert, {
                    "id_guru": clean_id_guru,
                    "id_ind": clean_id_ind,
                    "bulan": clean_bulan,
                    "tahun": clean_tahun,
                    "nilai": clean_nilai
                })

            resp.media = {"status": "success", "message": "Nilai kinerja berhasil disimpan!"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}