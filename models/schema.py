from pony.orm import *
from datetime import datetime

db = Database()


class AdminUser(db.Entity):
    _table_ = "admin_user"
    id = PrimaryKey(int, auto=True)
    name = Optional(str, default="Administrator")
    email = Required(str, unique=True)
    password = Required(str)
    last_login = Optional(datetime, nullable=True)
    created_date = Required(datetime, default=datetime.now)
    updated_date = Required(datetime, default=datetime.now)

    def to_response(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "last_login": self.last_login.strftime("%d %B %Y %H:%M:%S") if self.last_login else None,
            "created_date": self.created_date.strftime("%d %B %Y") if self.created_date else None
        }


class TahunAjaran(db.Entity):
    _table_ = "tahun_ajaran"
    id = PrimaryKey(int, auto=True)
    tahun = Required(str)
    nama = Required(str)
    is_active = Required(bool, default=False)
    kelas = Set('Kelas')


class Jurusan(db.Entity):
    _table_ = "jurusan"
    id = PrimaryKey(int, auto=True)
    kode_jurusan = Required(str, unique=True)
    nama_jurusan = Required(str)
    kelas = Set('Kelas')
    siswa = Set('Siswa')


class Kelas(db.Entity):
    _table_ = "kelas"
    id = PrimaryKey(int, auto=True)
    kode_kelas = Required(str)
    nama_kelas = Required(str)
    jurusan = Optional(Jurusan)
    tahun_ajaran = Optional(TahunAjaran)
    wali_kelas_name = Optional(str)
    siswa = Set('Siswa')


class Siswa(db.Entity):
    _table_ = "siswa"
    id = PrimaryKey(int, auto=True)
    nis = Required(str, unique=True)
    nama = Required(str)
    tgl_lahir = Optional(datetime)
    alamat = Optional(str)
    status_aktif = Required(bool, default=True)
    kelas = Optional(Kelas)
    jurusan = Optional(Jurusan)
    absensi = Set('Absensi')


class Absensi(db.Entity):
    _table_ = "absensi"
    id = PrimaryKey(int, auto=True)
    siswa = Required(Siswa)
    tanggal = Required(datetime)
    status_hadir = Required(str)  # "Hadir", "Izin", "Sakit", "Alfa"
    jam_masuk = Optional(str)
    jam_pulang = Optional(str)
    keterangan = Optional(str)

    def to_response(self):
        return {
            "id": self.id,
            "nama_siswa": self.siswa.nama,
            "nis": self.siswa.nis,
            "tanggal": self.tanggal.strftime("%d %B %Y"),
            "status": self.status_hadir,
            "keterangan": self.keterangan
        }
