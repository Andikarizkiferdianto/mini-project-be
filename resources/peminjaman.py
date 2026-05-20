import json
import falcon

from pony.orm import db_session, commit, rollback

from models.schema import (
    Buku,
    Siswa,
    Peminjaman
)


class PeminjamanResource:

    @db_session
    def on_get(self, req, resp):

        data = []

        peminjaman = Peminjaman.select().order_by(
            lambda p: p.id
        )

        for p in peminjaman:

            data.append({
                "id": p.id,
                "nama": p.siswa.nama,
                "nis": p.siswa.nis,
                "buku": p.buku.judul_buku,
                "buku_id": p.buku.id,
                "jumlah": p.jumlah,
                "tgl_pinjam": str(p.tgl_pinjam),
                "tgl_kembali": str(p.tgl_kembali),
                "status": p.status
            })

        resp.media = {
            "data": data
        }

    @db_session
    def on_post(self, req, resp):

        try:

            raw_json = req.bounded_stream.read()

            if not raw_json:
                raise Exception("Body request kosong")

            payload = json.loads(raw_json.decode("utf-8"))

            nis = str(payload.get("nis", "")).strip()

            buku_input = str(
                payload.get("buku_id", "")
            ).strip()

            jumlah = int(
                payload.get("jumlah", 1)
            )

            tgl_pinjam = payload.get("tgl_pinjam")
            tgl_kembali = payload.get("tgl_kembali")

            if nis == "":
                resp.status = falcon.HTTP_400
                resp.media = {
                    "error": "NIS wajib diisi"
                }
                return

            if buku_input == "":
                resp.status = falcon.HTTP_400
                resp.media = {
                    "error": "ID Buku wajib diisi"
                }
                return

            siswa = Siswa.get(
                nis=nis
            )

            if not siswa:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "error": f"Siswa dengan NIS {nis} tidak ditemukan"
                }
                return

            buku = None

            if buku_input.isdigit():

                buku = Buku.get(
                    id=int(buku_input)
                )

            if not buku:

                buku = Buku.get(
                    barcode=buku_input
                )

            if not buku:
                resp.status = falcon.HTTP_404
                resp.media = {
                    "error": "Buku tidak ditemukan"
                }
                return

            if buku.stok < jumlah:
                resp.status = falcon.HTTP_400
                resp.media = {
                    "error": "Stok buku tidak cukup"
                }
                return

            Peminjaman(
                siswa=siswa,
                buku=buku,
                jumlah=jumlah,
                tgl_pinjam=tgl_pinjam,
                tgl_kembali=tgl_kembali,
                status="Dipinjam"
            )

            buku.stok -= jumlah

            commit()

            resp.status = falcon.HTTP_201

            resp.media = {
                "message": "Peminjaman berhasil"
            }

        except Exception as e:

            rollback()

            print("ERROR PEMINJAMAN:", str(e))

            resp.status = falcon.HTTP_400

            resp.media = {
                "error": str(e)
            }


class PeminjamanDetailResource:

    @db_session
    def on_put(self, req, resp, p_id):

        try:

            raw_json = req.bounded_stream.read()

            payload = json.loads(
                raw_json.decode("utf-8")
            )

            p = Peminjaman.get(
                id=int(p_id)
            )

            if not p:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "error": "Data tidak ditemukan"
                }

                return

            if (
                p.status == "Dipinjam"
                and
                payload["status"] == "Dikembalikan"
            ):

                p.buku.stok += p.jumlah

            p.status = payload["status"]

            commit()

            resp.media = {
                "message": "Buku berhasil dikembalikan"
            }

        except Exception as e:

            rollback()

            resp.status = falcon.HTTP_400

            resp.media = {
                "error": str(e)
            }

    @db_session
    def on_delete(self, req, resp, p_id):

        try:

            p = Peminjaman.get(
                id=int(p_id)
            )

            if not p:

                resp.status = falcon.HTTP_404

                resp.media = {
                    "error": "Data tidak ditemukan"
                }

                return

            if p.status == "Dipinjam":

                p.buku.stok += p.jumlah

            p.delete()

            commit()

            resp.media = {
                "message": "Data berhasil dihapus"
            }

        except Exception as e:

            rollback()

            resp.status = falcon.HTTP_400

            resp.media = {
                "error": str(e)
            }


class ScanBukuResource:

    @db_session
    def on_get(self, req, resp):

        barcode = req.get_param("barcode")

        buku = Buku.get(
            barcode=barcode
        )

        if not buku:

            resp.status = falcon.HTTP_404

            resp.media = {
                "error": "Buku tidak ditemukan"
            }

            return

        resp.media = {
            "id": buku.id,
            "judul_buku": buku.judul_buku,
            "stok": buku.stok
        }