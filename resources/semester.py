import json
import falcon
from pony.orm import db_session, commit
from models.schema import Semester, TahunAjaran


class SemesterResource:
    @db_session
    def on_get(self, req, resp):
        semua_semester = Semester.select()[:]
        data = []

        for s in semua_semester:
            data.append({
                "id": s.id,
                "tahun_ajaran": s.tahun_ajaran.tahun,
                "jenis_semester": s.jenis_semester,
                "nama_semester": s.nama_semester
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"data": data})

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            ta = TahunAjaran.get(id=payload.get('id_tahun_ajaran'))
            if not ta:
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({"message": "Tahun Ajaran tidak ditemukan!"})
                return

            Semester(
                tahun_ajaran=ta,
                jenis_semester=payload.get('jenis_semester'),
                nama_semester=payload.get('nama_semester')
            )

            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Data Semester berhasil ditambah!"})

        except Exception as ex:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal simpan: {str(ex)}"})


class SemesterDetailResource:
    @db_session
    def on_delete(self, req, resp, semester_id):
        sem = Semester.get(id=semester_id)
        if not sem:
            resp.status = falcon.HTTP_404
            return

        sem.delete()
        commit()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Semester berhasil dihapus!"})