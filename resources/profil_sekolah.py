import falcon
import os
import uuid
from models.schema import db
from pony.orm import db_session


class ProfilSekolahResource:

    @db_session
    def on_get(self, req, resp):
        """Ambil data profil sekolah"""

        try:

            sql = "SELECT * FROM profil_sekolah WHERE id = 1"

            res = db.select(sql)

            if not res:

                resp.media = {
                    "status": "error",
                    "message": "Data tidak ditemukan"
                }

                return

            r = res[0]

            resp.media = {
                "status": "success",
                "data": {
                    "nama_sekolah": r[1],
                    "npsn": r[2],
                    "alamat": r[3],
                    "telepon": r[4],
                    "email": r[5],
                    "website": r[6],
                    "kepala_sekolah": r[7],
                    "logo_sekolah": r[8]
                }
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }

    @db_session
    def on_post(self, req, resp):
        """Update profil sekolah & upload logo"""

        try:

            # bikin folder uploads/logo kalau belum ada
            os.makedirs('uploads/logo', exist_ok=True)

            form = req.get_media()

            nama = ""
            npsn = ""
            alamat = ""
            telepon = ""
            email = ""
            website = ""
            kepala = ""
            nama_file_baru = None

            for part in form:

                if part.name == 'nama_sekolah':
                    nama = part.text

                elif part.name == 'npsn':
                    npsn = part.text

                elif part.name == 'alamat':
                    alamat = part.text

                elif part.name == 'telepon':
                    telepon = part.text

                elif part.name == 'email':
                    email = part.text

                elif part.name == 'website':
                    website = part.text

                elif part.name == 'kepala_sekolah':
                    kepala = part.text

                elif part.name == 'logo_sekolah':

                    # skip kalau file kosong
                    if not part.filename:
                        continue

                    ext = os.path.splitext(part.filename)[1]

                    nama_file_baru = (
                        f"logo_{uuid.uuid4().hex}{ext}"
                    )

                    path_simpan = os.path.join(
                        'uploads',
                        'logo',
                        nama_file_baru
                    )

                    # baca binary file
                    data = part.stream.read()

                    with open(path_simpan, 'wb') as f:
                        f.write(data)

            # cek data sudah ada atau belum
            cek = db.select(
                "SELECT id FROM profil_sekolah WHERE id = 1"
            )

            if cek:

                # update dengan logo
                if nama_file_baru:

                    sql = """
                        UPDATE profil_sekolah SET
                            nama_sekolah = $nama,
                            npsn = $npsn,
                            alamat = $alamat,
                            telepon = $telp,
                            email = $email,
                            website = $web,
                            kepala_sekolah = $kepala,
                            logo_sekolah = $logo
                        WHERE id = 1
                    """

                    params = {
                        "nama": nama,
                        "npsn": npsn,
                        "alamat": alamat,
                        "telp": telepon,
                        "email": email,
                        "web": website,
                        "kepala": kepala,
                        "logo": nama_file_baru
                    }

                # update tanpa logo
                else:

                    sql = """
                        UPDATE profil_sekolah SET
                            nama_sekolah = $nama,
                            npsn = $npsn,
                            alamat = $alamat,
                            telepon = $telp,
                            email = $email,
                            website = $web,
                            kepala_sekolah = $kepala
                        WHERE id = 1
                    """

                    params = {
                        "nama": nama,
                        "npsn": npsn,
                        "alamat": alamat,
                        "telp": telepon,
                        "email": email,
                        "web": website,
                        "kepala": kepala
                    }

                db.execute(sql, params)

            else:

                sql = """
                    INSERT INTO profil_sekolah (
                        id,
                        nama_sekolah,
                        npsn,
                        alamat,
                        telepon,
                        email,
                        website,
                        kepala_sekolah,
                        logo_sekolah
                    )
                    VALUES (
                        1,
                        $nama,
                        $npsn,
                        $alamat,
                        $telp,
                        $email,
                        $web,
                        $kepala,
                        $logo
                    )
                """

                db.execute(sql, {
                    "nama": nama,
                    "npsn": npsn,
                    "alamat": alamat,
                    "telp": telepon,
                    "email": email,
                    "web": website,
                    "kepala": kepala,
                    "logo": nama_file_baru
                })

            resp.media = {
                "status": "success",
                "message": "Profil sekolah berhasil diupdate!"
            }

        except Exception as e:

            resp.status = falcon.HTTP_500

            resp.media = {
                "status": "error",
                "message": str(e)
            }