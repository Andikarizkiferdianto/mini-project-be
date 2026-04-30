import falcon
from pony.orm import db_session, count, select
from models.schema import Buku, Peminjaman


class DashboardResource:
    @db_session
    def on_get(self, req, resp):
        # Inisialisasi data default biar kalau ada yang kosong gak crash
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
            # Ambil angka statistik dasar
            res["total_buku"] = count(Buku.select())
            res["total_kategori"] = count(select(b.kategori for b in Buku))
            res["stok_minim"] = count(Buku.select(lambda b: b.stok <= 3))
            res["total_peminjaman"] = count(Peminjaman.select())
            res["sedang_dipinjam"] = count(Peminjaman.select(lambda p: p.status.lower() == "dipinjam"))
            res["sudah_dikembalikan"] = count(Peminjaman.select(lambda p: p.status.lower() == "dikembalikan"))

            # Logika Buku Terpopuler yang anti-index error
            pjm_list = list(Peminjaman.select())
            if pjm_list:
                counts = {}
                for p in pjm_list:
                    # Ambil judul buku, abaikan kalau datanya corrupt/None
                    judul = getattr(p.buku, 'judul_buku', None)
                    if judul:
                        counts[judul] = counts.get(judul, 0) + 1

                if counts:
                    top_judul = max(counts, key=counts.get)
                    res["buku_terpopuler"] = {"judul": top_judul, "jumlah": counts[top_judul]}

        except Exception as e:
            # Kalau ada error database, kirim info error aslinya ke Postman
            # Biar kita tau errornya APA, bukan cuma "ga bisa"
            res["error_detail"] = str(e)
            res["catatan"] = "Coba cek terminal PyCharm atau hapus folder __pycache__"

        resp.status = falcon.HTTP_200
        resp.media = res