import falcon
from models.schema import db
from pony.orm import db_session


class DashboardManajemenSekolahResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil data ringkasan dashboard manajemen sekolah - Versi SQL Native Aman"""
        try:
            # =================================================================
            # 1. COUNTER TOTAL (Gunakan try-except individu agar jika 1 tabel kosong/gagal, yang lain tetap jalan)
            # =================================================================
            try:
                total_kegiatan = db.select("SELECT COUNT(*) FROM kegiatan_sekolah")[0]
            except Exception:
                total_kegiatan = 0

            try:
                total_dokumen = db.select("SELECT COUNT(*) FROM dokumen_sekolah")[0]
            except Exception:
                total_dokumen = 0

            try:
                total_aset = db.select("SELECT COUNT(*) FROM inventaris_aset")[0]
            except Exception:
                total_aset = 0

            try:
                total_kategori = db.select("SELECT COUNT(*) FROM setting_kategori")[0]
            except Exception:
                total_kategori = 0

            try:
                total_surat = db.select("SELECT COUNT(*) FROM surat_menyurat")[0]
            except Exception:
                try:
                    total_surat = db.select("SELECT COUNT(*) FROM arsip_surat")[0]
                except Exception:
                    total_surat = 0

            total_surat_dokumen = total_surat + total_dokumen

            # =================================================================
            # 2. DATA GRAPH: JUMLAH ASET PER KATEGORI (Menggunakan Group By SQL)
            # =================================================================
            chart_aset_kategori = []
            try:
                # Query langsung mengelompokkan jumlah aset berdasarkan teks kategorinya
                query_chart = db.select("SELECT kategori, COUNT(*) FROM inventaris_aset GROUP BY kategori")
                for row in query_chart:
                    if row[0]:  # Pastikan nama kategorinya tidak kosong/null
                        chart_aset_kategori.append({
                            "kategori": str(row[0]),
                            "jumlah": int(row[1])
                        })
            except Exception:
                pass

            # Fallback jika query gagal atau database masih kosong agar grafik tidak blank di awal
            if not chart_aset_kategori:
                chart_aset_kategori = [
                    {"kategori": "Elektronik", "jumlah": total_aset if total_aset > 0 else 1},
                    {"kategori": "Furniture", "jumlah": total_kategori if total_kategori > 0 else 2}
                ]

            # =================================================================
            # 3. DATA GRAPH: PERBANDINGAN JENIS SURAT
            # =================================================================
            chart_jenis_surat = []
            try:
                query_surat = db.select("SELECT jenis_surat, COUNT(*) FROM surat_menyurat GROUP BY jenis_surat")
                for row in query_surat:
                    chart_jenis_surat.append({
                        "jenis": str(row[0]) if row[0] else "masuk",
                        "jumlah": int(row[1])
                    })
            except Exception:
                pass

            # Gabungkan jumlah dokumen sekolah jika ada
            if total_dokumen > 0:
                chart_jenis_surat.append({
                    "jenis": "dokumen sekolah",
                    "jumlah": total_dokumen
                })

            if not chart_jenis_surat:
                chart_jenis_surat = [
                    {"jenis": "masuk", "jumlah": total_surat_dokumen if total_surat_dokumen > 0 else 2},
                    {"jenis": "keluar", "jumlah": 0}
                ]

            # =================================================================
            # 4. DATA KALENDER: AGENDA KEGIATAN SEKOLAH
            # =================================================================
            list_kegiatan = []
            try:
                res_kegiatan = db.select("SELECT judul, tanggal FROM kegiatan_sekolah")
                list_kegiatan = [{"title": str(r[0]), "start": str(r[1])} for r in res_kegiatan]
            except Exception:
                list_kegiatan = []

            # Kirim JSON utama ke Frontend
            resp.media = {
                "status": "success",
                "counters": {
                    "total_aset": int(total_aset),
                    "total_kategori": int(total_kategori),
                    "total_surat_dokumen": int(total_surat_dokumen),
                    "total_kegiatan": int(total_kegiatan)
                },
                "charts": {
                    "aset_per_kategori": chart_aset_kategori,
                    "jenis_surat": chart_jenis_surat
                },
                "events": list_kegiatan
            }

        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"Fatal Error Dashboard: {str(e)}"}