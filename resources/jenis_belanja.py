import falcon
from models.schema import JenisBelanja
from pony.orm import db_session, select


class JenisBelanjaResource:
    @db_session
    def on_get(self, req, resp):
        try:
            query = JenisBelanja.select()

            data = []
            for obj in query:
                data.append({
                    "id": obj.id,
                    "akun_belanja": obj.akun_belanja or "",
                    "akun_harta": obj.akun_harta or "",
                    "kode_akun": obj.kode_akun or "",
                    "nama_akun": obj.nama_akun or "",
                    "jenis": obj.jenis or "",
                    "keterangan": obj.keterangan or "",
                    "status": obj.status or "Aktif"
                })

            resp.media = {
                "status": "success",
                "data": data
            }
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": f"Gagal narik data: {str(e)}"
            }

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            JenisBelanja(
                akun_belanja=data.get('akun_belanja'),
                akun_harta=data.get('akun_harta'),
                kode_akun=data.get('kode_akun'),
                nama_akun=data.get('nama_akun'),
                jenis=data.get('jenis'),
                keterangan=data.get('keterangan', ''),
                status=data.get('status', 'Aktif')
            )
            resp.status = falcon.HTTP_201
            resp.media = {
                "status": "success",
                "message": "Jenis belanja berhasil ditambahkan"
            }
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {
                "status": "error",
                "message": str(e)
            }


class JenisBelanjaDetailResource:
    @db_session
    def on_put(self, req, resp, id):
        data = req.media
        obj = JenisBelanja.get(id=id)
        if not obj:
            resp.status = falcon.HTTP_404
            resp.media = {"status": "error", "message": "Data tidak ditemukan"}
            return

        try:
            obj.set(**data)
            resp.media = {"status": "success", "message": "Data berhasil diperbarui"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        obj = JenisBelanja.get(id=id)
        if obj:
            obj.delete()
            resp.media = {"status": "success", "message": "Data berhasil dihapus"}
        else:
            resp.status = falcon.HTTP_404
            resp.media = {"status": "error", "message": "Data tidak ditemukan"}