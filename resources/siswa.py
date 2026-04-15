import json
import falcon
from pony.orm import db_session, select
from models.schema import Siswa, Kelas


class SiswaResource:
    @db_session
    def on_get(self, req, resp):
        semua_siswa = select(s for s in Siswa)[:]

        data = []
        for s in semua_siswa:
            data.append({
                "id": s.id,
                "nis": s.nis,
                "nama": s.nama,
                "status_aktif": s.status_aktif,
                "kelas": s.kelas.nama_kelas if s.kelas else "Belum Ada Kelas"
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "message": "Berhasil mengambil data siswa",
            "data": data
        })

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            kelas_id = payload.get('kelas_id')
            obj_kelas = Kelas.get(id=kelas_id)

            Siswa(
                nis=payload.get('nis'),
                nama=payload.get('nama'),
                status_aktif=True,
                kelas=obj_kelas
            )

            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Data siswa berhasil ditambahkan!"})

        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal: {str(e)}"})


class SiswaWithIdResource:
    @db_session
    def on_put(self, req, resp, siswa_id):
        payload = json.loads(req.stream.read(req.content_length or 0))
        siswa = Siswa.get(id=siswa_id)

        if not siswa:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Data siswa tidak ditemukan!"})
            return

        if 'nis' in payload:
            siswa.nis = payload['nis']
        if 'nama' in payload:
            siswa.nama = payload['nama']
        if 'status_aktif' in payload:
            siswa.status_aktif = payload['status_aktif']

        if 'kelas_id' in payload:
            obj_kelas = Kelas.get(id=payload['kelas_id'])
            if obj_kelas:
                siswa.kelas = obj_kelas

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": f"Data siswa {siswa.nama} berhasil diupdate!"})

    @db_session
    def on_delete(self, req, resp, siswa_id):
        siswa = Siswa.get(id=siswa_id)

        if not siswa:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Data siswa tidak ditemukan!"})
            return

        siswa.delete()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Data siswa berhasil dihapus!"})
