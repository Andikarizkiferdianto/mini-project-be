import falcon
from models.schema import db
from pony.orm import db_session


class InventarisAsetResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil daftar aset + hitung penyusutan secara dinamis"""
        try:
            # Menggunakan execute raw untuk mengambil data berdasarkan indeks yang konsisten
            cursor = db.execute("""
                SELECT id, nama_aset, kategori, lokasi, jumlah, harga_perolehan, umur_ekonomis 
                FROM inventaris_aset 
                ORDER BY id DESC
            """)
            result = cursor.fetchall()

            data = []
            for r in result:
                id_aset = r[0]
                nama_aset = r[1]
                kategori = r[2]
                lokasi = r[3]
                jumlah = int(r[4]) if r[4] else 0
                harga_perolehan = float(r[5]) if r[5] else 0.0
                umur_ekonomis = int(r[6]) if r[6] else 0

                # Formula penyusutan metode garis lurus
                penyusutan_per_unit = harga_perolehan / umur_ekonomis if umur_ekonomis > 0 else 0
                total_penyusutan = penyusutan_per_unit * jumlah

                data.append({
                    "id": id_aset,
                    "nama_aset": nama_aset,
                    "kategori": kategori,
                    "lokasi": lokasi,
                    "jumlah": jumlah,
                    "harga_perolehan": harga_perolehan,
                    "umur_ekonomis": umur_ekonomis,
                    "penyusutan_per_unit": penyusutan_per_unit,
                    "total_penyusutan": total_penyusutan
                })

            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah Aset Baru (Sanitasi & Konversi Tipe Data)"""
        raw_data = req.get_media()
        try:
            sql = """
                INSERT INTO inventaris_aset (nama_aset, kategori, lokasi, jumlah, harga_perolehan, umur_ekonomis)
                VALUES ($nama, $kat, $lok, $jml, $harga, $umur)
            """
            db.execute(sql, {
                "nama": raw_data['nama_aset'],
                "kat": raw_data['kategori'],
                "lok": raw_data['lokasi'],
                "jml": int(raw_data['jumlah']),
                "harga": float(raw_data['harga_perolehan']),
                "umur": int(raw_data['umur_ekonomis'])
            })
            resp.media = {"status": "success", "message": "Aset berhasil ditambahkan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp):
        """Update/Edit Data Aset"""
        raw_data = req.get_media()
        try:
            sql = """
                UPDATE inventaris_aset SET 
                nama_aset=$nama, kategori=$kat, lokasi=$lok, 
                jumlah=$jml, harga_perolehan=$harga, umur_ekonomis=$umur
                WHERE id=$id
            """
            db.execute(sql, {
                "id": int(raw_data['id']),
                "nama": raw_data['nama_aset'],
                "kat": raw_data['kategori'],
                "lok": raw_data['lokasi'],
                "jml": int(raw_data['jumlah']),
                "harga": float(raw_data['harga_perolehan']),
                "umur": int(raw_data['umur_ekonomis'])
            })
            resp.media = {"status": "success", "message": "Data aset berhasil diupdate"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus Aset Berdasarkan ID"""
        id_aset = req.get_param_as_int('id')
        try:
            db.execute("DELETE FROM inventaris_aset WHERE id = $id", {"id": id_aset})
            resp.media = {"status": "success", "message": "Aset berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}
