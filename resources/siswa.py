import json
import falcon
from pony.orm import db_session
from models.schema import Siswa, Kelas, Jurusan
from datetime import datetime


class SiswaResource:
    @db_session
    def on_get(self, req, resp):
        from pony.orm import rollback
        rollback()

        semua_siswa = Siswa.select().prefetch(Kelas, Jurusan)[:]

        data = []
        for s in semua_siswa:
            data.append({
                "id": s.id,
                "nis": s.nis,
                "nama": s.nama,
                "status_aktif": s.status_aktif,
                "kelas": s.kelas.nama_kelas if s.kelas else "Belum Set Kelas",
                "jurusan": s.jurusan.nama_jurusan if s.jurusan else "Belum Set Jurusan"
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Berhasil", "data": data})

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            obj_kelas = Kelas.get(id=payload.get('id_kelas'))
            obj_jurusan = Jurusan.get(id=payload.get('id_jurusan'))

            Siswa(
                nis=payload.get('nis'),
                nama=payload.get('nama'),
                status_aktif=True,
                kelas=obj_kelas,
                jurusan=obj_jurusan
            )

            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Siswa berhasil ditambahkan ke kelas & jurusan!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal: {str(e)}"})


class SiswaWithIdResource:
    @db_session
    def on_put(self, req, resp, siswa_id):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            siswa = Siswa.get(id=siswa_id)

            if not siswa:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"message": "Siswa tidak ketemu!"})
                return

            if 'nis' in payload: siswa.nis = payload['nis']
            if 'nama' in payload: siswa.nama = payload['nama']

            if 'id_kelas' in payload:
                obj_kelas = Kelas.get(id=payload['id_kelas'])
                if obj_kelas:
                    siswa.kelas = obj_kelas

            if 'id_jurusan' in payload:
                obj_jurusan = Jurusan.get(id=payload['id_jurusan'])
                if obj_jurusan:
                    siswa.jurusan = obj_jurusan

            from pony.orm import commit
            commit()

            resp.status = falcon.HTTP_200
            resp.text = json.dumps({"message": f"Data {siswa.nama} berhasil diupdate!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal update: {str(e)}"})

    @db_session
    def on_delete(self, req, resp, siswa_id):
        siswa = Siswa.get(id=siswa_id)
        if not siswa:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Siswa tidak ditemukan!"})
            return

        siswa.delete()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Data siswa berhasil dihapus!"})