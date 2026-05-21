import falcon
from models.schema import db
from pony.orm import db_session


class DashboardManajemenSekolahResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil data ringkasan dashboard manajemen sekolah - Versi Fix Syntax MariaDB"""
        try:
            # =================================================================
            # 1. COUNTER TOTAL
            # =================================================================

            # --- CARD 1: Total Jumlah Aset ---
            try:
                total_aset_aktif = db.select("SELECT COUNT(*) FROM inventaris_aset")[0]
            except Exception:
                total_aset_aktif = 0

            try:
                total_riwayat_aset = db.select("SELECT COUNT(*) FROM riwayat_aset")[0]
            except Exception:
                total_riwayat_aset = 0

            total_aset = total_aset_aktif + total_riwayat_aset

            # --- CARD 2: Total Kategori Aset ---
            try:
                total_kategori = db.select("SELECT COUNT(*) FROM setting_kategori_aset")[0]
            except Exception:
                total_kategori = 0

            # --- CARD 3: Total Kegiatan Sekolah ---
            try:
                total_kegiatan = db.select("SELECT COUNT(*) FROM kegiatan_sekolah")[0]
            except Exception:
                total_kegiatan = 0

            # --- CARD 4: Total Surat & Dokumentasi ---
            try:
                total_dokumen = db.select("SELECT COUNT(*) FROM dokumen_sekolah")[0]
            except Exception:
                total_dokumen = 0

            try:
                total_surat = db.select("SELECT COUNT(*) FROM arsip_surat")[0]
            except Exception:
                try:
                    total_surat = db.select("SELECT COUNT(*) FROM surat_menyurat")[0]
                except Exception:
                    total_surat = 0

            total_surat_dokumen = total_surat + total_dokumen

            # =================================================================
            # 2. DATA GRAPH: JUMLAH ASET PER KATEGORI (Fix Syntax MariaDB)
            # =================================================================
            chart_aset_kategori = []
            try:
                # Query ditulis rapat dan bersih agar tidak memicu error syntax 1064 di MariaDB
                sql_aset = (
                    "SELECT sk.nama_kategori, COUNT(ia.id) "
                    "FROM setting_kategori_aset sk "
                    "LEFT JOIN inventaris_aset ia ON LOWER(TRIM(sk.nama_kategori)) = LOWER(TRIM(ia.kategori)) "
                    "GROUP BY sk.nama_kategori"
                )
                query_chart = db.select(sql_aset)
                for row in query_chart:
                    chart_aset_kategori.append({
                        "kategori": str(row[0]),
                        "jumlah": int(row[1])
                    })
            except Exception as e:
                print(f" Backend Warning (Chart Aset): {str(e)}")
                pass

            # Fallback jika query utama gagal
            if not chart_aset_kategori:
                try:
                    jml_elektronik = db.select("SELECT COUNT(*) FROM inventaris_aset WHERE LOWER(kategori) LIKE '%elektronik%'")[0]
                    jml_furniture = db.select("SELECT COUNT(*) FROM inventaris_aset WHERE LOWER(kategori) LIKE '%furnit%'")[0]
                except Exception:
                    jml_elektronik = total_aset_aktif
                    jml_furniture = 0

                chart_aset_kategori = [
                    {"kategori": "Elektronik", "jumlah": jml_elektronik},
                    {"kategori": "Furniture", "jumlah": jml_furniture}
                ]

            # =================================================================
            # 3. DATA GRAPH: PERBANDINGAN JENIS SURAT (Fix Nama Tabel)
            # =================================================================
            chart_jenis_surat = []
            try:
                # Mencoba query ke arsip_surat yang terbukti ada di database kamu
                query_surat = db.select("SELECT jenis_surat, COUNT(*) FROM arsip_surat GROUP BY jenis_surat")
                for row in query_surat:
                    chart_jenis_surat.append({
                        "jenis": str(row[0]) if row[0] else "masuk",
                        "jumlah": int(row[1])
                    })
            except Exception:
                try:
                    # Alternatif kedua jika menggunakan nama tabel lain
                    query_surat = db.select("SELECT jenis_surat, COUNT(*) FROM surat_menyurat GROUP BY jenis_surat")
                    for row in query_surat:
                        chart_jenis_surat.append({
                            "jenis": str(row[0]) if row[0] else "masuk",
                            "jumlah": int(row[1])
                        })
                except Exception as e:
                    print(f" Backend Warning (Chart Surat): {str(e)}")
                    pass

            if total_dokumen > 0:
                chart_jenis_surat.append({
                    "jenis": "dokumen sekolah",
                    "jumlah": total_dokumen
                })

            if not chart_jenis_surat:
                chart_jenis_surat = [
                    {"jenis": "masuk", "jumlah": total_surat_dokumen},
                    {"jenis": "keluar", "jumlah": 0}
                ]

            # =================================================================
            # 4. DATA KALENDER: AGENDA KEGIATAN SEKOLAH
            # =================================================================
            list_kegiatan = []
            try:
                res_kegiatan = db.select("SELECT judul, tanggal FROM kegiatan_sekolah")
                list_kegiatan = [{"title": str(r[0]), "start": str(r[1])} for r in res_kegiatan]
            except Exception as e:
                print(f" Backend Warning (Kalender): {str(e)}")
                list_kegiatan = []

            # Response JSON Utama ke Frontend
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