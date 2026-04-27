import json
import falcon
from pony.orm import db_session, commit, select
from models.schema import JadwalMengajar, Guru, MataPelajaran, Kelas, Semester


class JadwalResource:
    @db_session
    def on_get(self, req, resp):
        jadwals = JadwalMengajar.select()
        data = []
        for j in jadwals:
            data.append({
                "id": j.id,
                "guru": j.guru.nama,
                "mata_pelajaran": j.mapel.nama_mapel,
                "kelas": j.kelas.nama_kelas,
                "hari": j.hari,
                "jam": j.jam,
                "semester": j.semester.nama_semester
            })
        resp.text = json.dumps(data)

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            guru = Guru.get(id=payload.get('id_guru'))
            mapel = MataPelajaran.get(id=payload.get('id_mapel'))
            kelas = Kelas.get(id=payload.get('id_kelas'))
            semester = Semester.get(id=payload.get('id_semester'))

            if not all([guru, mapel, kelas, semester]):
                resp.status = falcon.HTTP_400
                resp.text = json.dumps({"error": "ID Guru/Mapel/Kelas/Semester tidak valid!"})
                return

            JadwalMengajar(
                hari=payload.get('hari'),
                jam=payload.get('jam'),
                guru=guru,
                mapel=mapel,
                kelas=kelas,
                semester=semester
            )
            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Jadwal berhasil dibuat!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})


class JadwalDetailResource:
    @db_session
    def on_put(self, req, resp, j_id):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))
            jadwal = JadwalMengajar.get(id=j_id)
            if not jadwal:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"error": "Jadwal tidak ditemukan!"})
                return

            if 'hari' in payload: jadwal.hari = payload['hari']
            if 'jam' in payload: jadwal.jam = payload['jam']
            if 'id_guru' in payload: jadwal.guru = Guru.get(id=payload['id_guru'])
            if 'id_mapel' in payload: jadwal.mapel = MataPelajaran.get(id=payload['id_mapel'])
            if 'id_kelas' in payload: jadwal.kelas = Kelas.get(id=payload['id_kelas'])

            commit()
            resp.text = json.dumps({"message": "Jadwal berhasil diupdate!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})

    @db_session
    def on_delete(self, req, resp, j_id):
        try:
            jadwal = JadwalMengajar.get(id=j_id)
            if not jadwal:
                resp.status = falcon.HTTP_404
                resp.text = json.dumps({"error": "Jadwal tidak ditemukan!"})
                return
            jadwal.delete()
            commit()
            resp.text = json.dumps({"message": "Jadwal berhasil dihapus!"})
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"error": str(e)})