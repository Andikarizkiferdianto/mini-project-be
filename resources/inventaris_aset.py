import falcon
from models.schema import db
from pony.orm import db_session


class InventarisAsetResource:
    @db_session
    def on_get(self, req, resp):
        """Ambil daftar aset + hitung penyusutan"""
        try:
            sql = "SELECT * FROM inventaris_aset ORDER BY id DESC"
            result = db.select(sql)

            data = []
            for r in result:
                harga = float(r[5])
                umur = r[6]
                # Hitung penyusutan per unit
                penyusutan_per_tahun = harga / umur if umur > 0 else 0
                total_penyusutan = penyusutan_per_tahun * r[4]

                data.append({
                    "id": r[0],
                    "nama_aset": r[1],
                    "kategori": r[2],
                    "lokasi": r[3],
                    "jumlah": r[4],
                    "harga_perolehan": harga,
                    "umur_ekonomis": umur,
                    "penyusutan_per_unit": penyusutan_per_tahun,
                    "total_penyusutan": total_penyusutan
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        """Tambah Aset Baru"""
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
                "jml": raw_data['jumlah'],
                "harga": raw_data['harga_perolehan'],
                "umur": raw_data['umur_ekonomis']
            })
            resp.media = {"status": "success", "message": "Aset berhasil ditambahkan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp):
        """Edit Data Aset"""
        raw_data = req.get_media()
        try:
            sql = """
                UPDATE inventaris_aset SET 
                nama_aset=$nama, kategori=$kat, lokasi=$lok, 
                jumlah=$jml, harga_perolehan=$harga, umur_ekonomis=$umur
                WHERE id=$id
            """
            db.execute(sql, {
                "id": raw_data['id'],
                "nama": raw_data['nama_aset'],
                "kat": raw_data['kategori'],
                "lok": raw_data['lokasi'],
                "jml": raw_data['jumlah'],
                "harga": raw_data['harga_perolehan'],
                "umur": raw_data['umur_ekonomis']
            })
            resp.media = {"status": "success", "message": "Data aset berhasil diupdate"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp):
        """Hapus Aset"""
        id_aset = req.get_param_as_int('id')
        try:
            db.execute("DELETE FROM inventaris_aset WHERE id = $id", {"id": id_aset})
            resp.media = {"status": "success", "message": "Aset berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}