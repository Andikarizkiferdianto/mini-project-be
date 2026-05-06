import falcon
from pony.orm import db_session
from models.schema import db, JenisPenerimaan


class JenisPenerimaanResource:
    @db_session
    def on_get(self, req, resp):
        try:
            sql = "SELECT id, akun_harta, akun_pendapatan, kode_penerimaan, " \
                  "nama_akun, jenis, keterangan, status FROM jenis_penerimaan ORDER BY id DESC"
            data = db.select(sql)

            results = []
            for d in data:
                results.append({
                    "id": d[0],
                    "akun_harta": d[1],
                    "akun_pendapatan": d[2],
                    "kode_penerimaan": d[3],
                    "nama_akun": d[4],
                    "jenis": d[5],
                    "keterangan": d[6] or "-",
                    "status": d[7]
                })

            resp.media = {"status": "success", "data": results}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_post(self, req, resp):
        data = req.media
        try:
            JenisPenerimaan(
                akun_harta=data['akun_harta'],
                akun_pendapatan=data['akun_pendapatan'],
                kode_penerimaan=data['kode_penerimaan'],
                nama_akun=data['nama_akun'],
                jenis=data['jenis'],
                keterangan=data.get('keterangan', ''),
                status=data.get('status', 'Aktif')
            )
            resp.status = falcon.HTTP_201
            resp.media = {"status": "success", "message": "Jenis penerimaan berhasil ditambah"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}


class JenisPenerimaanDetailResource:
    @db_session
    def on_put(self, req, resp, id):
        data = req.media
        try:
            obj = JenisPenerimaan.get(id=id)
            if not obj:
                resp.status = falcon.HTTP_404
                return

            if 'akun_harta' in data: obj.akun_harta = data['akun_harta']
            if 'akun_pendapatan' in data: obj.akun_pendapatan = data['akun_pendapatan']
            if 'kode_penerimaan' in data: obj.kode_penerimaan = data['kode_penerimaan']
            if 'nama_akun' in data: obj.nama_akun = data['nama_akun']
            if 'jenis' in data: obj.jenis = data['jenis']
            if 'keterangan' in data: obj.keterangan = data['keterangan']
            if 'status' in data: obj.status = data['status']

            resp.media = {"status": "success", "message": "Data berhasil diperbarui"}
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}

    @db_session
    def on_delete(self, req, resp, id):
        try:
            obj = JenisPenerimaan.get(id=id)
            if obj:
                obj.delete()
                resp.media = {"status": "success", "message": "Data berhasil dihapus"}
            else:
                resp.status = falcon.HTTP_404
        except Exception as e:
            resp.status = falcon.HTTP_500
            resp.media = {"status": "error", "message": str(e)}