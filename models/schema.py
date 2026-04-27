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
    semesters = Set('Semester')


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
    jadwal = Set('JadwalMengajar')


class Siswa(db.Entity):
    _table_ = "siswa"
    id = PrimaryKey(int, auto=True)
    nis = Required(str, unique=True)
    nisn = Optional(str)
    nama = Required(str)
    tempat_lahir = Optional(str)
    tgl_lahir = Optional(datetime)
    jenis_kelamin = Optional(str)
    alamat = Optional(LongStr)
    agama = Optional(str)
    golongan_darah = Optional(str)
    status_aktif = Required(bool, default=True)
    tahun_ajaran = Optional(str)
    tahun_masuk = Optional(str)
    sekolah_asal = Optional(str)
    no_hp = Optional(str)

    nama_ayah = Optional(str)
    pekerjaan_ayah = Optional(str)
    no_hp_ayah = Optional(str)
    nama_ibu = Optional(str)
    pekerjaan_ibu = Optional(str)
    no_hp_ibu = Optional(str)

    kelas = Optional("Kelas")
    jurusan = Optional("Jurusan")
    absensi = Set("Absensi")


class Absensi(db.Entity):
    _table_ = "absensi"
    id = PrimaryKey(int, auto=True)
    siswa = Required(Siswa)
    tanggal = Required(datetime)
    status_hadir = Required(str)
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

class Ekstrakurikuler(db.Entity):
    _table_ = "ekstrakurikuler"
    id = PrimaryKey(int, auto=True)
    nama_ekskul = Required(str)
    pembina = Required(str)
    jadwal = Optional(str)
    tanggal = Optional(datetime)
    keterangan = Optional(str)

class AspekPenilaian(db.Entity):
    _table_ = "aspek_penilaian"
    id = PrimaryKey(int, auto=True)
    nama_aspek = Required(str)
    keterangan = Optional(str)
    can_edit = Required(bool, default=True)

class Semester(db.Entity):
    _table_ = "semester"
    id = PrimaryKey(int, auto=True)
    tahun_ajaran = Required('TahunAjaran')
    jenis_semester = Required(str)
    nama_semester = Required(str)
    jadwal = Set('JadwalMengajar')

class JenisSemester(db.Entity):
    _table_ = "jenis_semester"
    id = PrimaryKey(int, auto=True)
    nama = Required(str)

class Guru(db.Entity):
    _table_ = "guru"
    id = PrimaryKey(int, auto=True)
    nama = Required(str)
    nip = Optional(str, unique=True)
    jadwal = Set('JadwalMengajar')

class MataPelajaran(db.Entity):
    _table_ = "mata_pelajaran"
    id = PrimaryKey(int, auto=True)
    nama_mapel = Required(str)
    jadwal = Set('JadwalMengajar')

class JadwalMengajar(db.Entity):
    _table_ = "jadwal_mengajar"
    id = PrimaryKey(int, auto=True)
    hari = Required(str)
    jam = Required(str)
    guru = Required(Guru)
    mapel = Required(MataPelajaran)
    kelas = Required(Kelas)
    semester = Required(Semester)