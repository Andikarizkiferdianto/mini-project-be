import json
import falcon
from pony.orm import db_session, select
from models.schema import Kelas, Jurusan, TahunAjaran


class KelasResource:
    @db_session
    def on_get(self, req, resp):
        semua_kelas = Kelas.select()[:]

        data = []
        for k in semua_kelas:
            data.append({
                "id": k.id,
                "kode_kelas": k.kode_kelas,
                "nama_kelas": k.nama_kelas,
                "jurusan": k.jurusan.nama_jurusan if k.jurusan else "Tanpa Jurusan",
                "tahun_ajaran": k.tahun_ajaran.nama if k.tahun_ajaran else "Tanpa Tahun Ajaran",
                "wali_kelas": k.wali_kelas_name or "Belum Ditentukan",
                "total_siswa": k.siswa.count()
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "message": "Berhasil mengambil data kelas",
            "data": data
        })

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            jurusan_obj = Jurusan.get(id=payload.get('id_jurusan'))
            tahun_obj = TahunAjaran.get(id=payload.get('id_tahun_ajaran'))

            Kelas(
                kode_kelas=payload.get('kode_kelas'),
                nama_kelas=payload.get('nama_kelas'),
                jurusan=jurusan_obj,
                tahun_ajaran=tahun_obj,
                wali_kelas_name=payload.get('wali_kelas_name')
            )

            resp.status = falcon.HTTP_201
            resp.text = json.dumps({
                "message": f"Kelas {payload.get('nama_kelas')} berhasil ditambahkan!"
            })
        except Exception as e:
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal tambah kelas: {str(e)}"})

@db_session
def on_put(self, req, resp, kelas_id):
    kelas = Kelas.get(id=kelas_id)

    if not kelas:
        resp.status = falcon.HTTP_404
        resp.text = json.dumps({"message": "Kelas tidak ditemukan!"})
        return

    payload = json.loads(req.stream.read(req.content_length or 0))

    kelas.kode_kelas = payload.get('kode_kelas', kelas.kode_kelas)
    kelas.nama_kelas = payload.get('nama_kelas', kelas.nama_kelas)
    kelas.wali_kelas_name = payload.get('wali_kelas_name', kelas.wali_kelas_name)

    resp.status = falcon.HTTP_200
    resp.text = json.dumps({
        "message": f"Kelas {kelas.nama_kelas} berhasil diupdate!"
    })

class KelasWithIdResource:
    @db_session
    def on_delete(self, req, resp, kelas_id):
        kelas = Kelas.get(id=kelas_id)
        if not kelas:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Kelas tidak ditemukan!"})
            return

        nama_kelas = kelas.nama_kelas
        kelas.delete()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": f"Kelas {nama_kelas} berhasil dihapus!"})