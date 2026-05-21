import falcon
import os
import uuid
from models.schema import db
from pony.orm import db_session


class SuratMenyuratResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil semua data surat menyurat secara realtime dari database MySQL"""
        try:
            # Mengambil data terbaru diletakkan di paling atas (ORDER BY id DESC)
            rows = db.select("SELECT * FROM arsip_surat ORDER BY id DESC")

            data = []
            for r in rows:
                data.append({
                    "id": r[0],
                    "nomor_surat": r[1] if len(r) > 1 else "",
                    "tgl_surat": str(r[2]) if len(r) > 2 and r[2] else "",
                    "tgl_terima": str(r[3]) if len(r) > 3 and r[3] else "",
                    "sumber_surat": r[4] if len(r) > 4 else "",
                    "perihal": r[5] if len(r) > 5 else "",
                    "jenis_surat": r[6] if len(r) > 6 else "Masuk",
                    "file_surat": r[7] if len(r) > 7 else "",
                    "keterangan": r[8] if len(r) > 8 else "",
                })

            resp.media = {"status": "success", "data": data}

        except Exception as sql_error:
            # Jika database mengalami masalah, kirim log internal dan jangan buat frontend crash
            print(f"Sistem Log - Kendala database: {str(sql_error)}")
            resp.media = {"status": "success", "data": []}

    @db_session
    def on_post(self, req, resp):
        """Menangani pembuatan data baru (INSERT) ATAU pembaruan data lama (UPDATE)"""
        try:
            # Ambil query parameter 'id' untuk mendeteksi mode Edit
            id_surat = req.get_param_as_int("id")
            content_type = req.content_type or ''

            fields = {}
            file_name = ""

            # Parsing body request berdasarkan tipe datanya (JSON / Multipart form-data)
            if 'application/json' in content_type:
                fields = req.get_media()
            else:
                try:
                    form = req.get_media()
                    for part in form:
                        if part.name == "file_surat" and part.filename:
                            ext = os.path.splitext(part.filename)[1]
                            file_name = f"surat_{uuid.uuid4().hex}{ext}"
                            os.makedirs(os.path.join("uploads", "surat"), exist_ok=True)
                            path = os.path.join("uploads", "surat", file_name)
                            with open(path, "wb") as f:
                                f.write(part.data)
                        else:
                            fields[part.name] = part.text
                except Exception:
                    pass

            # Pemetaan data input dari frontend
            no_surat = fields.get("nomor_surat")
            perihal = fields.get("perihal")
            tgl_s = fields.get("tgl_surat") or None
            tgl_t = fields.get("tgl_terima") or None
            sumber = fields.get("sumber_surat") or ""
            jenis = fields.get("jenis_surat") or "Masuk"
            ket = fields.get("keterangan") or ""

            if not no_surat or not perihal:
                raise ValueError("Nomor surat dan Perihal wajib diisi!")

            # ==========================================
            # PROSES EDIT / UPDATE DATA (Jika ada ID)
            # ==========================================
            if id_surat:
                if file_name:
                    # Jalankan update beserta pembaruan berkas file baru
                    db.execute("""
                        UPDATE arsip_surat 
                        SET nomor_surat = $no, tgl_surat = $tgl_s, tgl_terima = $tgl_t, 
                            sumber_surat = $sumber, perihal = $perihal, jenis_surat = $jenis, 
                            file_surat = $file, keterangan = $ket 
                        WHERE id = $id
                    """, {
                        "no": no_surat, "tgl_s": tgl_s, "tgl_t": tgl_t, "sumber": sumber,
                        "perihal": perihal, "jenis": jenis, "file": file_name, "ket": ket, "id": id_surat
                    })
                else:
                    # Jalankan update data tanpa mengubah file yang sudah diunggah sebelumnya
                    db.execute("""
                        UPDATE arsip_surat 
                        SET nomor_surat = $no, tgl_surat = $tgl_s, tgl_terima = $tgl_t, 
                            sumber_surat = $sumber, perihal = $perihal, jenis_surat = $jenis, 
                            keterangan = $ket 
                        WHERE id = $id
                    """, {
                        "no": no_surat, "tgl_s": tgl_s, "tgl_t": tgl_t, "sumber": sumber,
                        "perihal": perihal, "jenis": jenis, "ket": ket, "id": id_surat
                    })

                resp.media = {"status": "success", "message": "Arsip surat berhasil diperbarui!"}

            # ==========================================
            # PROSES TAMBAH BARU / INSERT (Jika tidak ada ID)
            # ==========================================
            else:
                db.execute("""
                    INSERT INTO arsip_surat 
                    (nomor_surat, tgl_surat, tgl_terima, sumber_surat, perihal, jenis_surat, file_surat, keterangan) 
                    VALUES ($no, $tgl_s, $tgl_t, $sumber, $perihal, $jenis, $file, $ket)
                """, {
                    "no": no_surat, "tgl_s": tgl_s, "tgl_t": tgl_t, "sumber": sumber,
                    "perihal": perihal, "jenis": jenis, "file": file_name, "ket": ket
                })

                resp.media = {"status": "success", "message": "Surat baru berhasil diarsipkan!"}

        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": f"Gagal memproses data: {str(e)}"}

    @db_session
    def on_delete(self, req, resp):
        """Hapus data arsip surat dari database berdasarkan parameter ID"""
        try:
            id_surat = req.get_param_as_int("id")

            if not id_surat:
                raise ValueError("Parameter ID surat tidak valid.")

            db.execute("DELETE FROM arsip_surat WHERE id = $id", {"id": id_surat})
            resp.media = {"status": "success", "message": "Arsip surat berhasil dihapus dari sistem."}

        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"status": "error", "message": f"Gagal menghapus: {str(e)}"}