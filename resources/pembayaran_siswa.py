import falcon
import json
from pony.orm import db_session, select
from models.schema import db, Siswa, JenisPembayaran, BayarTagihan


class CariSiswaResource:
    @db_session
    def on_get(self, req, resp):
        try:
            query = req.get_param('q') or ""

            # 1. Cari Siswa Berdasarkan Nama/NIS (Tanpa filter dummy)
            # Menggunakan raw SQL agar aman dari bug bytecode Python 3.13
            sql_siswa = """
                SELECT id, nis, nama, kelas, jurusan 
                FROM siswa 
                WHERE (LOWER(nama) LIKE $nama OR nis LIKE $nis)
            """
            params = {"nama": f"%{query.lower()}%", "nis": f"%{query}%"}
            res_siswa = db.select(sql_siswa, params)

            data_final = []
            for row in res_siswa:
                s_id, nis, nama, kelas_id, jurusan_id = row

                # Ambil Nama Kelas & Jurusan
                nama_kelas = db.select("nama_kelas FROM kelas WHERE id = $id", {"id": kelas_id}).get() or "-"
                nama_jurusan = db.select("nama_jurusan FROM jurusan WHERE id = $id", {"id": jurusan_id}).get() or "-"

                # 2. Ambil Rincian Tagihan Siswa Tersebut
                # Kita hitung berapa yang sudah dibayar per jenis pembayaran
                tagihan_list = []
                semua_jenis = db.select("id, nama_pembayaran, nominal_ketetapan FROM jenis_pembayaran")

                for jp in semua_jenis:
                    jp_id, jp_nama, nominal_target = jp

                    # Hitung total yang sudah dibayar siswa ini untuk jenis ini
                    total_dibayar = db.select("""
                        SELECT SUM(nominal) FROM bayar_tagihan 
                        WHERE siswa = $s_id AND jenis_pembayaran = $jp_id
                    """, {"s_id": s_id, "jp_id": jp_id}).get() or 0

                    tagihan_list.append({
                        "jenis_pembayaran": jp_nama,
                        "target": float(nominal_target),
                        "terbayar": float(total_dibayar),
                        "sisa": float(nominal_target - total_dibayar),
                        "status": "Lunas" if total_dibayar >= nominal_target else "Belum Lunas"
                    })

                data_final.append({
                    "id": s_id,
                    "nis": nis,
                    "nama": nama,
                    "kelas": nama_kelas,
                    "jurusan": nama_jurusan,
                    "rincian_tagihan": tagihan_list
                })

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": "success",
                "data": data_final
            }
        except Exception as e:
            print(f"Error Cari Siswa: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class ListTahunAjaranResource:
    @db_session
    def on_get(self, req, resp):
        try:
            # Menggunakan raw SQL agar aman dari bug Python 3.13
            sql = "SELECT id, nama FROM tahun_ajaran"
            tahun_data = db.select(sql)

            results = [{"id": row[0], "nama": row[1]} for row in tahun_data]

            resp.status = falcon.HTTP_200
            resp.media = {
                "status": "success",
                "data": results
            }
        except Exception as e:
            print(f"Error List Tahun: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class SimpanPembayaranResource:
    @db_session
    def on_post(self, req, resp):
        try:
            # Ambil data JSON dari frontend
            raw_data = req.stream.read().decode('utf-8')
            data = json.loads(raw_data)

            siswa_id = data.get('siswa_id')
            jp_id = data.get('jenis_pembayaran_id')
            nominal = data.get('nominal')
            tanggal = data.get('tanggal_bayar')  # Format: YYYY-MM-DD

            if not all([siswa_id, jp_id, nominal]):
                resp.status = falcon.HTTP_400
                resp.media = {"status": "error", "message": "Data tidak lengkap"}
                return

            # Simpan menggunakan raw SQL agar aman di Python 3.13
            sql = """
                INSERT INTO bayar_tagihan (siswa, jenis_pembayaran, nominal, tanggal_bayar) 
                VALUES ($siswa, $jp, $nom, $tgl)
            """
            db.execute(sql, {
                "siswa": siswa_id,
                "jp": jp_id,
                "nom": nominal,
                "tgl": tanggal
            })

            resp.status = falcon.HTTP_201
            resp.media = {
                "status": "success",
                "message": "Pembayaran berhasil disimpan"
            }
        except Exception as e:
            print(f"Error Simpan: {e}")
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}