import falcon
from models.schema import db
from pony.orm import db_session
import traceback

class AkunBudgetingResource:
    @db_session
    def on_get(self, req, resp):
        """Menampilkan List Budgeting"""
        try:
            sql = "SELECT id, tahun_ajaran_id, akun_id, nominal_target, keterangan FROM budgeting ORDER BY id DESC"
            result = db.select(sql)
            data = []
            for row in result:
                data.append({
                    "id": row[0],
                    "tahun_ajaran_id": row[1],
                    "akun_id": row[2],
                    "nominal": float(row[3] or 0),
                    "keterangan": row[4]
                })
            resp.media = {"status": "success", "data": data}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": f"Gagal narik data: {str(e)}"}

    @db_session
    def on_post(self, req, resp):
        """Tambah Data"""
        raw_data = req.get_media()
        try:
            sql = "INSERT INTO budgeting (tahun_ajaran_id, akun_id, nominal_target, keterangan) VALUES ($tahun_id, $akun_id, $nominal, $ket)"
            db.execute(sql, {
                "tahun_id": raw_data['tahun_ajaran_id'],
                "akun_id": raw_data['akun_id'],
                "nominal": raw_data['nominal'],
                "ket": raw_data.get('keterangan', '')
            })
            resp.media = {"status": "success", "message": "Data budget berhasil disimpan"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_put(self, req, resp, budget_id):
        """Edit Data berdasarkan ID"""
        raw_data = req.get_media()
        try:
            sql = "UPDATE budgeting SET tahun_ajaran_id = $tahun_id, akun_id = $akun_id, nominal_target = $nominal, keterangan = $ket WHERE id = $id"
            db.execute(sql, {
                "tahun_id": raw_data['tahun_ajaran_id'],
                "akun_id": raw_data['akun_id'],
                "nominal": raw_data['nominal'],
                "ket": raw_data.get('keterangan', ''),
                "id": budget_id
            })
            resp.media = {"status": "success", "message": "Data budget berhasil diupdate"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, budget_id):
        """Hapus Data berdasarkan ID"""
        try:
            sql = "DELETE FROM budgeting WHERE id = $id"
            db.execute(sql, {"id": budget_id})
            resp.media = {"status": "success", "message": "Data budget berhasil dihapus"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

class OptionBudgetingResource:
    @db_session
    def on_get(self, req, resp):
        try:
            list_akun = db.select("SELECT id, kode_akun, nama_akun FROM masterdata")
            list_tahun = db.select("SELECT id, tahun_ajaran FROM tahun_ajaran")
            resp.media = {
                "status": "success",
                "options": {
                    "akun": [{"id": r[0], "label": f"{r[1]} - {r[2]}"} for r in list_akun],
                    "tahun_ajaran": [{"id": r[0], "label": r[1]} for r in list_tahun]
                }
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}