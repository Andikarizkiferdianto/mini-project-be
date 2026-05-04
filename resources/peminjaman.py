import json
import falcon
from datetime import datetime
from pony.orm import db_session, commit, select, rollback
from models.schema import Buku, Siswa, Peminjaman
from pony.orm import db_session, rollback

class PeminjamanResource:
    @db_session
    def on_get(self, req, resp):
        rollback()

        peminjamans = Peminjaman.select().order_by(lambda p: p.id)
        data = []
        for p in peminjamans:
            data.append({
                "id": p.id,
                "nama": p.siswa.nama,
                "nis": p.siswa.nis,
                "buku": p.buku.judul_buku,
                "buku_id": p.buku.id,
                "jumlah": p.jumlah,
                "tgl_pinjam": p.tgl_pinjam.strftime("%Y-%m-%d") if isinstance(p.tgl_pinjam, datetime) else str(p.tgl_pinjam),
                "tgl_kembali": p.tgl_kembali.strftime("%Y-%m-%d") if isinstance(p.tgl_kembali, datetime) else str(p.tgl_kembali),
                "status": p.status
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"data": data})

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            nis_input = str(payload['nis'])
            buku_id_input = int(payload['buku_id'])

            siswa = Siswa.get(nis=nis_input)
            buku = Buku.get(id=buku_id_input)

            if not siswa:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"error": f"Siswa dengan NIS {nis_input} tidak ditemukan"})
                return

            if not buku:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"error": f"Buku dengan ID {buku_id_input} tidak ditemukan"})
                return

            jumlah_pinjam = int(payload.get('jumlah', 1))
            if buku.stok < jumlah_pinjam:
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({"error": "Stok buku tidak mencukupi!"})
                return

            Peminjaman(
                siswa=siswa,
                buku=buku,
                tgl_pinjam=payload['tgl_pinjam'],
                tgl_kembali=payload['tgl_kembali'],
                jumlah=jumlah_pinjam,
                status='Dipinjam'
            )

            buku.stok -= jumlah_pinjam
            commit()

            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Peminjaman berhasil disimpan!"})

        except Exception as e:
            rollback()
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})


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