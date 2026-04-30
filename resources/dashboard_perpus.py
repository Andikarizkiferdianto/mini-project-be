import falcon
from pony.orm import db_session
from models.schema import db


class DashboardResource:
    @db_session
    def on_get(self, req, resp):
        res = {
            "total_buku": 0,
            "total_kategori": 0,
            "stok_minim": 0,
            "total_peminjaman": 0,
            "sedang_dipinjam": 0,
            "sudah_dikembalikan": 0,
            "buku_terpopuler": {"judul": "-", "jumlah": 0}
        }

        try:
            # Statistik Dasar (Query simpel satu baris)
            res["total_buku"] = db.select("SELECT COUNT(*) FROM buku")[0]
            res["total_kategori"] = db.select("SELECT COUNT(DISTINCT kategori) FROM buku")[0]
            res["stok_minim"] = db.select("SELECT COUNT(*) FROM buku WHERE stok <= 3")[0]
            res["total_peminjaman"] = db.select("SELECT COUNT(*) FROM peminjaman")[0]
            res["sedang_dipinjam"] = db.select("SELECT COUNT(*) FROM peminjaman WHERE status LIKE 'Dipinjam%'")[0]
            res["sudah_dikembalikan"] = db.select("SELECT COUNT(*) FROM peminjaman WHERE status LIKE 'Kembali%'")[0]

            # Query Terpopuler (Dibuat satu baris lurus biar MariaDB gak rewel)
            sql = "SELECT b.judul_buku, COUNT(p.siswa) FROM buku b JOIN peminjaman p ON b.id = p.buku GROUP BY b.judul_buku ORDER BY COUNT(p.siswa) DESC LIMIT 1"
            populer = db.select(sql)

            if populer:
                res["buku_terpopuler"] = {"judul": populer[0][0], "jumlah": populer[0][1]}

        except Exception as e:
            res["error_debug"] = str(e)

        resp.status = falcon.HTTP_200
        resp.media = res