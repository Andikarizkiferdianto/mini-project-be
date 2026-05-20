import json
import falcon
from pony.orm import db_session, commit, rollback
from models.schema import Siswa, Kelas, Jurusan
from datetime import datetime


class SiswaResource:

    @db_session
    def on_get(self, req, resp):

        rollback()

        kelas = req.get_param("kelas")
        tahun = req.get_param("tahun")

        query = Siswa.select()

        # FILTER KELAS
        if kelas:
            try:
                kelas_id = int(kelas)
                query = query.filter(lambda s: s.kelas.id == kelas_id)
            except:
                pass

        # FILTER TAHUN
        if tahun:
            query = query.filter(lambda s: s.tahun_ajaran == tahun)

        data = []

        for s in query:

            data.append({
                "id": s.id,
                "nis": s.nis,
                "nisn": s.nisn,
                "nama": s.nama,
                "tempat_lahir": s.tempat_lahir,
                "tgl_lahir": s.tgl_lahir.strftime("%Y-%m-%d") if s.tgl_lahir else "",
                "jenis_kelamin": s.jenis_kelamin,
                "alamat": s.alamat,
                "agama": s.agama,
                "golongan_darah": s.golongan_darah,
                "tahun_ajaran": s.tahun_ajaran,
                "tahun_masuk": s.tahun_masuk,
                "sekolah_asal": s.sekolah_asal,
                "no_hp": s.no_hp,

                "nama_ayah": s.nama_ayah,
                "pekerjaan_ayah": s.pekerjaan_ayah,
                "no_hp_ayah": s.no_hp_ayah,

                "nama_ibu": s.nama_ibu,
                "pekerjaan_ibu": s.pekerjaan_ibu,
                "no_hp_ibu": s.no_hp_ibu,

                "status_aktif": s.status_aktif,

                "kelas": s.kelas.nama_kelas if s.kelas else "-",
                "jurusan": s.jurusan.nama_jurusan if s.jurusan else "-",

                "id_kelas": s.kelas.id if s.kelas else None,
                "id_jurusan": s.jurusan.id if s.jurusan else None,
            })

        resp.status = falcon.HTTP_200

        resp.text = json.dumps({
            "data": data
        })

    @db_session
    def on_post(self, req, resp):

        try:

            payload = json.loads(
                req.stream.read(req.content_length or 0)
            )

            # VALIDASI NIS DUPLIKAT
            cek_nis = Siswa.get(
                nis=payload.get('nis')
            )

            if cek_nis:
                raise Exception("NIS sudah digunakan!")

            tgl_lahir_obj = None

            if payload.get('tgl_lahir'):

                tgl_lahir_obj = datetime.strptime(
                    payload.get('tgl_lahir'),
                    '%Y-%m-%d'
                )

            kelas_obj = Kelas.get(
                id=payload.get('id_kelas')
            ) if payload.get('id_kelas') else None

            jurusan_obj = Jurusan.get(
                id=payload.get('id_jurusan')
            ) if payload.get('id_jurusan') else None

            Siswa(

                nis=payload.get('nis'),
                nisn=payload.get('nisn', ''),
                nama=payload.get('nama'),

                tempat_lahir=payload.get(
                    'tempat_lahir',
                    ''
                ),

                tgl_lahir=tgl_lahir_obj,

                jenis_kelamin=payload.get(
                    'jenis_kelamin',
                    ''
                ),

                alamat=payload.get('alamat', ''),
                agama=payload.get('agama', ''),

                golongan_darah=payload.get(
                    'golongan_darah',
                    ''
                ),

                tahun_ajaran=payload.get(
                    'tahun_ajaran',
                    ''
                ),

                tahun_masuk=payload.get(
                    'tahun_masuk',
                    ''
                ),

                sekolah_asal=payload.get(
                    'sekolah_asal',
                    ''
                ),

                no_hp=payload.get('no_hp', ''),

                nama_ayah=payload.get(
                    'nama_ayah',
                    ''
                ),

                pekerjaan_ayah=payload.get(
                    'pekerjaan_ayah',
                    ''
                ),

                no_hp_ayah=payload.get(
                    'no_hp_ayah',
                    ''
                ),

                nama_ibu=payload.get(
                    'nama_ibu',
                    ''
                ),

                pekerjaan_ibu=payload.get(
                    'pekerjaan_ibu',
                    ''
                ),

                no_hp_ibu=payload.get(
                    'no_hp_ibu',
                    ''
                ),

                status_aktif=payload.get(
                    'status_aktif',
                    'Aktif'
                ),

                kelas=kelas_obj,
                jurusan=jurusan_obj
            )

            commit()

            resp.status = falcon.HTTP_201

            resp.text = json.dumps({
                "message": "Siswa berhasil ditambahkan!"
            })

        except Exception as e:

            rollback()

            import traceback
            traceback.print_exc()

            resp.status = falcon.HTTP_400

            resp.text = json.dumps({
                "message": f"Gagal simpan: {str(e)}"
            })


class SiswaWithIdResource:

    @db_session
    def on_get(self, req, resp, siswa_id):

        siswa = Siswa.get(id=siswa_id)

        if not siswa:

            resp.status = falcon.HTTP_404

            resp.text = json.dumps({
                "message": "Siswa tidak ditemukan!"
            })

            return

        resp.status = falcon.HTTP_200

        resp.text = json.dumps({
            "data": {
                "id": siswa.id,
                "nis": siswa.nis,
                "nisn": siswa.nisn,
                "nama": siswa.nama,
                "tempat_lahir": siswa.tempat_lahir,
                "tgl_lahir": siswa.tgl_lahir.strftime("%Y-%m-%d") if siswa.tgl_lahir else "",
                "jenis_kelamin": siswa.jenis_kelamin,
                "alamat": siswa.alamat,
                "agama": siswa.agama,
                "golongan_darah": siswa.golongan_darah,
                "tahun_ajaran": siswa.tahun_ajaran,
                "tahun_masuk": siswa.tahun_masuk,
                "sekolah_asal": siswa.sekolah_asal,
                "no_hp": siswa.no_hp,

                "nama_ayah": siswa.nama_ayah,
                "pekerjaan_ayah": siswa.pekerjaan_ayah,
                "no_hp_ayah": siswa.no_hp_ayah,

                "nama_ibu": siswa.nama_ibu,
                "pekerjaan_ibu": siswa.pekerjaan_ibu,
                "no_hp_ibu": siswa.no_hp_ibu,

                "status_aktif": siswa.status_aktif,

                "kelas": siswa.kelas.nama_kelas if siswa.kelas else "-",
                "jurusan": siswa.jurusan.nama_jurusan if siswa.jurusan else "-",

                "id_kelas": siswa.kelas.id if siswa.kelas else None,
                "id_jurusan": siswa.jurusan.id if siswa.jurusan else None,
            }
        })

    @db_session
    def on_put(self, req, resp, siswa_id):

        try:

            payload = json.loads(
                req.stream.read(req.content_length or 0)
            )

            siswa = Siswa.get(id=siswa_id)

            if not siswa:

                resp.status = falcon.HTTP_404

                resp.text = json.dumps({
                    "message": "Siswa tidak ditemukan!"
                })

                return

            # VALIDASI NIS DUPLIKAT
            cek_nis = Siswa.get(
                lambda s:
                s.nis == payload.get('nis')
                and s.id != siswa_id
            )

            if cek_nis:
                raise Exception("NIS sudah digunakan!")

            # TANGGAL LAHIR
            if payload.get('tgl_lahir'):

                siswa.tgl_lahir = datetime.strptime(
                    payload.get('tgl_lahir'),
                    '%Y-%m-%d'
                )

            # RELASI
            kelas_obj = Kelas.get(
                id=payload.get('id_kelas')
            ) if payload.get('id_kelas') else None

            jurusan_obj = Jurusan.get(
                id=payload.get('id_jurusan')
            ) if payload.get('id_jurusan') else None

            # UPDATE
            siswa.nis = payload.get('nis')
            siswa.nisn = payload.get('nisn', '')
            siswa.nama = payload.get('nama')

            siswa.tempat_lahir = payload.get(
                'tempat_lahir',
                ''
            )

            siswa.jenis_kelamin = payload.get(
                'jenis_kelamin',
                ''
            )

            siswa.alamat = payload.get('alamat', '')
            siswa.agama = payload.get('agama', '')

            siswa.golongan_darah = payload.get(
                'golongan_darah',
                ''
            )

            siswa.tahun_ajaran = payload.get(
                'tahun_ajaran',
                ''
            )

            siswa.tahun_masuk = payload.get(
                'tahun_masuk',
                ''
            )

            siswa.sekolah_asal = payload.get(
                'sekolah_asal',
                ''
            )

            siswa.no_hp = payload.get('no_hp', '')

            siswa.nama_ayah = payload.get(
                'nama_ayah',
                ''
            )

            siswa.pekerjaan_ayah = payload.get(
                'pekerjaan_ayah',
                ''
            )

            siswa.no_hp_ayah = payload.get(
                'no_hp_ayah',
                ''
            )

            siswa.nama_ibu = payload.get(
                'nama_ibu',
                ''
            )

            siswa.pekerjaan_ibu = payload.get(
                'pekerjaan_ibu',
                ''
            )

            siswa.no_hp_ibu = payload.get(
                'no_hp_ibu',
                ''
            )

            siswa.status_aktif = payload.get(
                'status_aktif',
                'Aktif'
            )

            siswa.kelas = kelas_obj
            siswa.jurusan = jurusan_obj

            commit()

            resp.status = falcon.HTTP_200

            resp.text = json.dumps({
                "message": f"Data {siswa.nama} berhasil diupdate!"
            })

        except Exception as e:

            rollback()

            import traceback
            traceback.print_exc()

            resp.status = falcon.HTTP_400

            resp.text = json.dumps({
                "message": f"Gagal update: {str(e)}"
            })

    @db_session
    def on_delete(self, req, resp, siswa_id):

        try:

            siswa = Siswa.get(id=siswa_id)

            if not siswa:

                resp.status = falcon.HTTP_404

                resp.text = json.dumps({
                    "message": "Siswa tidak ditemukan!"
                })

                return

            nama_siswa = siswa.nama

            siswa.delete()

            commit()

            resp.status = falcon.HTTP_200

            resp.text = json.dumps({
                "message": f"{nama_siswa} berhasil dihapus!"
            })

        except Exception as e:

            rollback()

            import traceback
            traceback.print_exc()

            resp.status = falcon.HTTP_400

            resp.text = json.dumps({
                "message": f"Gagal hapus: {str(e)}"
            })