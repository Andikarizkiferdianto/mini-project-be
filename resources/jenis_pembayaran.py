import json
import falcon
from pony.orm import db_session, commit
from models.schema import JenisPembayaran


class JenisPembayaranResource:
    @db_session
    def on_get(self, req, resp):
        data = [j.to_dict() for j in JenisPembayaran.select()]
        resp.media = data

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            JenisPembayaran(
                kode_akun=payload['kode_akun'],
                nama_pembayaran=payload['nama_pembayaran'],
                akun_harta=payload.get('akun_harta', '--'),
                akun_pendapatan=payload.get('akun_pendapatan', '--'),
                akun_hutang=payload.get('akun_hutang', '--'),
                tipe=payload['tipe'],
                status=payload.get('status', 'aktif')
            )
            commit()
            resp.status = falcon.HTTP_201
            resp.media = {"message": "Jenis pembayaran berhasil disimpan!"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}


class JenisPembayaranDetailResource:
    @db_session
    def on_put(self, req, resp, jp_id):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            jp = JenisPembayaran.get(id=jp_id)
            if not jp:
                resp.status = falcon.HTTP_404
                return

            if 'kode_akun' in payload: jp.kode_akun = payload['kode_akun']
            if 'nama_pembayaran' in payload: jp.nama_pembayaran = payload['nama_pembayaran']
            if 'akun_harta' in payload: jp.akun_harta = payload['akun_harta']
            if 'akun_pendapatan' in payload: jp.akun_pendapatan = payload['akun_pendapatan']
            if 'akun_hutang' in payload: jp.akun_hutang = payload['akun_hutang']
            if 'tipe' in payload: jp.tipe = payload['tipe']
            if 'status' in payload: jp.status = payload['status']

            commit()
            resp.media = {"message": "Data berhasil diperbarui!"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}

    @db_session
    def on_delete(self, req, resp, jp_id):
        jp = JenisPembayaran.get(id=jp_id)
        if jp:
            jp.delete()
            commit()
            resp.media = {"message": "Data berhasil dihapus!"}