import json
import falcon
import time
from pony.orm import db_session, commit
from models.schema import Buku

class BukuResource:
    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            barcode_val = payload.get('barcode')
            if not barcode_val or barcode_val.strip() == "":
                barcode_val = f"BK{int(time.time())}"

            Buku(
                judul_buku=payload['judul_buku'],
                penulis=payload['penulis'],
                penerbit=payload['penerbit'],
                tahun=int(payload['tahun']),
                isbn=payload['isbn'],
                barcode=barcode_val,
                harga=payload.get('harga', 0),
                kondisi=payload['kondisi'],
                kategori=payload['kategori'],
                rak=payload['rak'],
                stok=int(payload.get('stok', 1))
            )
            commit()
            resp.status = falcon.HTTP_201
            resp.media = {"message": "Buku berhasil ditambahkan!", "barcode": barcode_val}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}

    @db_session
    def on_get(self, req, resp):
        search = req.get_param('search')
        if search:
            query = select(b for b in Buku if search in b.judul_buku or search in b.barcode)
        else:
            query = Buku.select()

        data = [b.to_dict() for b in query]
        resp.media = data

class BukuDetailResource:
    @db_session
    def on_put(self, req, resp, buku_id):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            b = Buku.get(id=buku_id)
            if not b:
                resp.status = falcon.HTTP_404
                resp.media = {"message": "Buku tidak ditemukan"}
                return

            if 'judul_buku' in payload: b.judul_buku = payload['judul_buku']
            if 'penulis' in payload: b.penulis = payload['penulis']
            if 'penerbit' in payload: b.penerbit = payload['penerbit']
            if 'tahun' in payload: b.tahun = int(payload['tahun'])
            if 'isbn' in payload: b.isbn = payload['isbn']
            if 'barcode' in payload: b.barcode = payload['barcode']
            if 'harga' in payload: b.harga = payload['harga']
            if 'kondisi' in payload: b.kondisi = payload['kondisi']
            if 'kategori' in payload: b.kategori = payload['kategori']
            if 'rak' in payload: b.rak = payload['rak']
            if 'stok' in payload: b.stok = int(payload['stok'])

            commit()
            resp.media = {"message": "Data buku berhasil diperbarui!"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}

    @db_session
    def on_delete(self, req, resp, buku_id):
        try:
            b = Buku.get(id=buku_id)
            if b:
                b.delete()
                commit()
                resp.media = {"message": "Buku berhasil dihapus!"}
            else:
                resp.status = falcon.HTTP_404
                resp.media = {"message": "Buku tidak ditemukan"}
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.media = {"error": str(e)}