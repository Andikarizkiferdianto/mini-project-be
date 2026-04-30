import json
import falcon
from pony.orm import db_session, commit, select
from models.schema import Buku, Siswa, Peminjaman


class PeminjamanResource:
    @db_session
    def on_get(self, req, resp):
        data = []
        for p in Peminjaman.select().order_by(lambda: p.id):
            data.append({
                "id": p.id,
                "nama": p.siswa.nama,
                "buku": p.buku.judul_buku,
                "jumlah": p.jumlah,
                "tgl_pinjam": p.tgl_pinjam,
                "tgl_kembali": p.tgl_kembali,
                "status": p.status
            })
        resp.media = data

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            siswa = Siswa.get(nis=payload['nis'])
            buku = Buku.get(id=payload['buku_id'])

            if not siswa or not buku:
                resp.status = falcon.HTTP_404
                resp.media = {"error": "Siswa atau Buku tidak ditemukan"}
                return

            Peminjaman(
                siswa=siswa,
                buku=buku,
                tgl_pinjam=payload['tgl_pinjam'],
                tgl_kembali=payload['tgl_kembali'],
                jumlah=payload.get('jumlah', 1),
                status='Dipinjam'
            )

            buku.stok -= int(payload.get('jumlah', 1))

            commit()
            resp.media = {"message": "Peminjaman berhasil disimpan!"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}


class ScanBukuResource:
    @db_session
    def on_get(self, req, resp):
        barcode = req.get_param('barcode')
        b = Buku.get(barcode=barcode)
        if b:
            resp.media = b.to_dict()
        else:
            resp.status = falcon.HTTP_404


class PeminjamanDetailResource:
    @db_session
    def on_put(self, req, resp, p_id):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            p = Peminjaman.get(id=p_id)
            if not p:
                resp.status = falcon.HTTP_404
                resp.media = {"message": "Data peminjaman tidak ditemukan"}
                return

            if 'status' in payload:
                if p.status == 'Dipinjam' and payload['status'] == 'Dikembalikan':
                    p.buku.stok += p.jumlah
                p.status = payload['status']

            if 'tgl_kembali' in payload: p.tgl_kembali = payload['tgl_kembali']
            if 'jumlah' in payload: p.jumlah = int(payload['jumlah'])

            commit()
            resp.media = {"message": "Data peminjaman berhasil diperbarui!"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}

    @db_session
    def on_delete(self, req, resp, p_id):
        try:
            p = Peminjaman.get(id=p_id)
            if p:
                if p.status == 'Dipinjam':
                    p.buku.stok += p.jumlah
                p.delete()
                commit()
                resp.media = {"message": "Data peminjaman berhasil dihapus!"}
            else:
                resp.status = falcon.HTTP_404
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}