import json
import falcon
from pony.orm import db_session, commit, rollback
from models.schema import Siswa, Kelas, Jurusan
from datetime import datetime


class SiswaResource:
    @db_session
    def on_get(self, req, resp):
        rollback()
        semua_siswa = Siswa.select().prefetch(Kelas, Jurusan)[:]
        data = []

        for s in semua_siswa:
            data.append({
                "id": s.id,
                "nis": s.nis,
                "nisn": s.nisn or "-",
                "nama": s.nama,
                "tempat_lahir": s.tempat_lahir or "-",
                "tgl_lahir": s.tgl_lahir.strftime("%Y-%m-%d") if isinstance(s.tgl_lahir, datetime) else str(s.tgl_lahir or "-"),
                "jenis_kelamin": s.jenis_kelamin or "-",
                "alamat": s.alamat or "-",
                "agama": s.agama or "-",
                "golongan_darah": s.golongan_darah or "-",
                "tahun_ajaran": s.tahun_ajaran or "-",
                "tahun_masuk": s.tahun_masuk or "-",
                "sekolah_asal": s.sekolah_asal or "-",
                "no_hp": s.no_hp or "-",
                "nama_ayah": s.nama_ayah or "-",
                "pekerjaan_ayah": s.pekerjaan_ayah or "-",
                "no_hp_ayah": s.no_hp_ayah or "-",
                "nama_ibu": s.nama_ibu or "-",
                "pekerjaan_ibu": s.pekerjaan_ibu or "-",
                "no_hp_ibu": s.no_hp_ibu or "-",
                "kelas": s.kelas.nama_kelas if s.kelas else "Belum Set",
                "jurusan": s.jurusan.nama_jurusan if s.jurusan else "Belum Set",
                "status_aktif": s.status_aktif
            })

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"data": data})

    @db_session
    def on_post(self, req, resp):
        try:
            payload = json.loads(req.stream.read(req.content_length or 0))

            tgl_lahir_obj = None
            if payload.get('tgl_lahir'):
                tgl_lahir_obj = datetime.strptime(payload.get('tgl_lahir'), '%Y-%m-%d')

            kelas_obj = Kelas.get(id=payload.get('id_kelas')) if payload.get('id_kelas') else None
            jurusan_obj = Jurusan.get(id=payload.get('id_jurusan')) if payload.get('id_jurusan') else None

            Siswa(
                nis=payload.get('nis'),
                nisn=payload.get('nisn'),
                nama=payload.get('nama'),
                tempat_lahir=payload.get('tempat_lahir'),
                tgl_lahir=tgl_lahir_obj,
                jenis_kelamin=payload.get('jenis_kelamin'),
                alamat=payload.get('alamat'),
                agama=payload.get('agama'),
                golongan_darah=payload.get('golongan_darah'),
                tahun_ajaran=payload.get('tahun_ajaran'),
                tahun_masuk=payload.get('tahun_masuk'),
                sekolah_asal=payload.get('sekolah_asal'),
                no_hp=payload.get('no_hp'),
                nama_ayah=payload.get('nama_ayah'),
                pekerjaan_ayah=payload.get('pekerjaan_ayah'),
                no_hp_ayah=payload.get('no_hp_ayah'),
                nama_ibu=payload.get('nama_ibu'),
                pekerjaan_ibu=payload.get('pekerjaan_ibu'),
                no_hp_ibu=payload.get('no_hp_ibu'),
                status_aktif=payload.get('status_aktif', 'Aktif'),
                kelas=kelas_obj,
                jurusan=jurusan_obj
            )

            commit()
            resp.status = falcon.HTTP_201
            resp.text = json.dumps({"message": "Siswa berhasil ditambahkan!"})

        except Exception as e:
            rollback()
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal simpan: {str(e)}"})


class SiswaWithIdResource:

    @db_session
    def on_get(self, req, resp, siswa_id):
        siswa = Siswa.get(id=siswa_id)

        if not siswa:
            resp.status = falcon.HTTP_404
            resp.text = json.dumps({"message": "Siswa tidak ketemu!"})
            return

        resp.status = falcon.HTTP_200
        resp.text = json.dumps({
            "data": {
                "id": siswa.id,
                "nis": siswa.nis,
                "nisn": siswa.nisn or "-",
                "nama": siswa.nama,
                "tempat_lahir": siswa.tempat_lahir or "-",
                "tgl_lahir": siswa.tgl_lahir.strftime("%Y-%m-%d") if siswa.tgl_lahir else "",
                "jenis_kelamin": siswa.jenis_kelamin or "-",
                "alamat": siswa.alamat or "-",
                "agama": siswa.agama or "-",
                "golongan_darah": siswa.golongan_darah or "-",
                "tahun_ajaran": siswa.tahun_ajaran or "-",
                "tahun_masuk": siswa.tahun_masuk or "-",
                "sekolah_asal": siswa.sekolah_asal or "-",
                "no_hp": siswa.no_hp or "-",
                "nama_ayah": siswa.nama_ayah or "-",
                "pekerjaan_ayah": siswa.pekerjaan_ayah or "-",
                "no_hp_ayah": siswa.no_hp_ayah or "-",
                "nama_ibu": siswa.nama_ibu or "-",
                "pekerjaan_ibu": siswa.pekerjaan_ibu or "-",
                "no_hp_ibu": siswa.no_hp_ibu or "-",
                "id_kelas": siswa.kelas.id if siswa.kelas else "",
                "id_jurusan": siswa.jurusan.id if siswa.jurusan else "",
                "status_aktif": siswa.status_aktif,
            }
        })

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
            if 'nisn' in payload: siswa.nisn = payload['nisn']
            if 'nama' in payload: siswa.nama = payload['nama']
            if 'tempat_lahir' in payload: siswa.tempat_lahir = payload['tempat_lahir']
            if 'tgl_lahir' in payload and payload['tgl_lahir']:
                siswa.tgl_lahir = datetime.strptime(payload['tgl_lahir'], '%Y-%m-%d')
            if 'jenis_kelamin' in payload: siswa.jenis_kelamin = payload['jenis_kelamin']
            if 'agama' in payload: siswa.agama = payload['agama']
            if 'golongan_darah' in payload: siswa.golongan_darah = payload['golongan_darah']
            if 'alamat' in payload: siswa.alamat = payload['alamat']
            if 'no_hp' in payload: siswa.no_hp = payload['no_hp']
            if 'nama_ayah' in payload: siswa.nama_ayah = payload['nama_ayah']
            if 'nama_ibu' in payload: siswa.nama_ibu = payload['nama_ibu']
            if 'id_kelas' in payload:
                siswa.kelas = Kelas.get(id=payload['id_kelas'])
            if 'id_jurusan' in payload:
                siswa.jurusan = Jurusan.get(id=payload['id_jurusan'])
            if 'status_aktif' in payload:
                siswa.status_aktif = payload['status_aktif']


            commit()
            resp.status = falcon.HTTP_200
            resp.text = json.dumps({"message": f"Data {siswa.nama} berhasil diupdate!"})

        except Exception as e:
            rollback()
            resp.status = falcon.HTTP_400
            resp.text = json.dumps({"message": f"Gagal update: {str(e)}"})

    @db_session
    def on_delete(self, req, resp, siswa_id):
        siswa = Siswa.get(id=siswa_id)
        if not siswa:
            resp.status = falcon.HTTP_404
            return
        siswa.delete()
        commit()
        resp.status = falcon.HTTP_200
        resp.text = json.dumps({"message": "Berhasil hapus"})