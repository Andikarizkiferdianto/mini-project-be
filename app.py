import falcon
import pymysql

pymysql.install_as_MySQLdb()
from falcon_cors import CORS
from models.schema import db, AdminUser
from pony.orm import db_session
from waitress import serve

from resources.siswa import SiswaResource, SiswaWithIdResource
from resources.auth import AdminLoginResource
from resources.dashboard import DashboardStatsResource
from resources.kelas import KelasResource, KelasWithIdResource
from resources.jurusan import JurusanResource, JurusanWithIdResource
from resources.absensi import AbsensiResource
from resources.ekskul import EkskulResource, EkskulDetailResource
from resources.aspek import AspekResource, AspekDetailResource
from resources.semester import SemesterResource, SemesterDetailResource
from resources.tahun_ajaran import TahunAjaranResource, TahunAjaranWithIdResource, TahunAjaranActiveResource
from resources.jenis_semester import JenisSemesterResource, JenisSemesterDetailResource
from resources.jadwal import JadwalResource, JadwalDetailResource
from resources.mata_pelajaran import MataPelajaranResource, MataPelajaranDetailResource
from resources.guru import GuruResource, GuruDetailResource
from resources.jenis_pembayaran import JenisPembayaranResource, JenisPembayaranDetailResource
from resources.buku import BukuResource, BukuDetailResource
from resources.peminjaman import PeminjamanResource, ScanBukuResource, PeminjamanDetailResource
from resources.dashboard_perpus import DashboardResource
from resources.kenaikan_kelas import KenaikanKelasResource
from resources.dashboard_keuangan import DashboardKeuanganResource
from resources.pembayaran_siswa import CariSiswaResource, ListTahunAjaranResource, SimpanPembayaranResource
from resources.tunggakan_siswa import TunggakanSiswaResource, ListKelasResource
from resources.tarif_pembayaran import TarifPembayaranOptionsResource, ListTarifSiswaResource
from resources.rekap_pembayaran import RekapBulananResource
from resources.data_transaksi import DataTransaksiResource
from resources.teller import TellerResource, RiwayatTabunganResource, RiwayatTransaksiGlobalResource
from resources.transaksi_penerimaan import TransaksiPenerimaanResource, TransaksiPenerimaanDetailResource
from resources.jenis_penerimaan import JenisPenerimaanResource, JenisPenerimaanDetailResource
from resources.laporan_penerimaan import LaporanPenerimaanResource
from resources.transaksi_belanja import TransaksiBelanjaResource, TransaksiBelanjaDetailResource
from resources.jenis_belanja import JenisBelanjaResource, JenisBelanjaDetailResource
from resources.laporan_belanja import LaporanBelanjaResource
from resources.transaksi_jurnal import TransaksiJurnalResource, AkunJurnalOptionResource
from resources.laporan_jurnal import LaporanJurnalResource, LaporanJurnalResource, LaporanJurnalDetailResource
from resources.laporan_buku_besar import LaporanBukuBesarResource
from resources.neraca_saldo import NeracaSaldoResource
from resources.laporan_jurnal_umum import JurnalUmumResource
from resources.penghasilan_komprehensif import PenghasilanKomprehensifResource
from resources.posisi_keuangan import PosisiKeuanganResource
from resources.arus_kas import ArusKasResource
from resources.perubahan_aset_neto import PerubahanAsetNetoResource
from resources.akun_budgeting import AkunBudgetingResource, OptionBudgetingResource
from resources.akun_keuangan import AkunKeuanganResource, OptionKeuanganResource
from resources.informasi_lembaga import InformasiLembagaResource
from resources.banner_aplikasi import BannerAplikasiResource
from resources.setting_user import SettingUserResource
from resources.backup_data import BackupDataResource
from resources.absensi_gps import AbsensiGpsResource
from resources.dashboard_aplikasi import DashboardAplikasiResource

cors = CORS(allow_all_origins=True,
            allow_all_headers=True,
            allow_all_methods=True)

app = falcon.App(middleware=[cors.middleware])

db.bind(provider='mysql', host='localhost', user='root', passwd='', db='sap_database')

app.add_route('/api/siswa', SiswaResource())
app.add_route('/api/siswa/{siswa_id}', SiswaWithIdResource())
app.add_route('/api/admin/login', AdminLoginResource())
app.add_route('/api/dashboard/stats', DashboardStatsResource())
app.add_route('/api/kelas', KelasResource())
app.add_route('/api/kelas/{kelas_id}', KelasWithIdResource())
app.add_route('/api/jurusan', JurusanResource())
app.add_route('/api/jurusan/{jurusan_id}', JurusanWithIdResource())
app.add_route('/api/absensi', AbsensiResource())
app.add_route('/api/ekskul', EkskulResource())
app.add_route('/api/ekskul/{ekskul_id}', EkskulDetailResource())
app.add_route('/api/aspek-penilaian', AspekResource())
app.add_route('/api/aspek-penilaian/{aspek_id}', AspekDetailResource())
app.add_route('/api/semester', SemesterResource())
app.add_route('/api/semester/{semester_id}', SemesterDetailResource())
app.add_route('/api/tahun-ajaran', TahunAjaranResource())
app.add_route('/api/tahun-ajaran/{ta_id}', TahunAjaranWithIdResource())
app.add_route('/api/tahun-ajaran/active', TahunAjaranActiveResource())
app.add_route('/api/jenis-semester', JenisSemesterResource())
app.add_route('/api/jenis-semester/{js_id}', JenisSemesterDetailResource())
app.add_route('/api/jadwal', JadwalResource())
app.add_route('/api/jadwal/{j_id}', JadwalDetailResource())
app.add_route('/api/mata-pelajaran', MataPelajaranResource())
app.add_route('/api/mata-pelajaran/{mp_id}', MataPelajaranDetailResource())
app.add_route('/api/guru', GuruResource())
app.add_route('/api/guru/{g_id}', GuruDetailResource())
app.add_route('/api/jenis-pembayaran', JenisPembayaranResource())
app.add_route('/api/jenis-pembayaran/{jp_id}', JenisPembayaranDetailResource())
app.add_route('/api/buku', BukuResource())
app.add_route('/api/buku/{buku_id}', BukuDetailResource())
app.add_route('/api/peminjaman', PeminjamanResource())
app.add_route('/api/peminjaman/{p_id}', PeminjamanDetailResource())
app.add_route('/api/peminjaman/scan', ScanBukuResource())
app.add_route('/api/dashboard-perpus', DashboardResource())
app.add_route('/api/kenaikan-kelas', KenaikanKelasResource())
app.add_route('/api/dashboard-keuangan', DashboardKeuanganResource())
app.add_route('/api/pembayaran/cari-siswa', CariSiswaResource())
app.add_route('/api/pembayaran/list-tahun', ListTahunAjaranResource())
app.add_route('/api/pembayaran/simpan', SimpanPembayaranResource())
app.add_route('/api/tunggakan/list', TunggakanSiswaResource())
app.add_route('/api/tunggakan/kelas', ListKelasResource())
app.add_route('/api/tarif/options', TarifPembayaranOptionsResource())
app.add_route('/api/tarif/list', ListTarifSiswaResource())
app.add_route('/api/rekap/bulanan', RekapBulananResource())
app.add_route('/api/transaksi/data', DataTransaksiResource())
app.add_route('/api/tabungan/teller', TellerResource())
app.add_route('/api/tabungan/riwayat', RiwayatTabunganResource())
app.add_route('/api/tabungan/riwayat-global', RiwayatTransaksiGlobalResource())
app.add_route('/api/penerimaan/transaksi', TransaksiPenerimaanResource())
app.add_route('/api/penerimaan/transaksi/{id:int}', TransaksiPenerimaanDetailResource())
app.add_route('/api/penerimaan/jenis', JenisPenerimaanResource())
app.add_route('/api/penerimaan/jenis/{id:int}', JenisPenerimaanDetailResource())
app.add_route('/api/penerimaan/laporan', LaporanPenerimaanResource())
app.add_route('/api/belanja/transaksi', TransaksiBelanjaResource())
app.add_route('/api/belanja/transaksi/{id:int}', TransaksiBelanjaDetailResource())
app.add_route('/api/belanja/jenis', JenisBelanjaResource())
app.add_route('/api/belanja/jenis/{id:int}', JenisBelanjaDetailResource())
app.add_route('/api/belanja/laporan', LaporanBelanjaResource())
app.add_route('/api/jurnal/transaksi', TransaksiJurnalResource())
app.add_route('/api/jurnal/options', AkunJurnalOptionResource())
app.add_route('/api/jurnal/laporan', LaporanJurnalResource())
app.add_route('/api/jurnal/laporan/{jurnal_id:int}', LaporanJurnalDetailResource())
app.add_route('/api/jurnal/buku-besar', LaporanBukuBesarResource())
app.add_route('/api/jurnal/neraca-saldo', NeracaSaldoResource())
app.add_route('/api/jurnal/umum', JurnalUmumResource())
app.add_route('/api/laporan/penghasilan-komprehensif', PenghasilanKomprehensifResource())
app.add_route('/api/laporan/posisi-keuangan', PosisiKeuanganResource())
app.add_route('/api/laporan/arus-kas', ArusKasResource())
app.add_route('/api/laporan/perubahan-aset-neto', PerubahanAsetNetoResource())
app.add_route('/api/budgeting', AkunBudgetingResource())
app.add_route('/api/budgeting/{budget_id}', AkunBudgetingResource())
app.add_route('/api/budgeting/options', OptionBudgetingResource())
app.add_route('/api/akun-keuangan', AkunKeuanganResource())
app.add_route('/api/akun-keuangan/{akun_id}', AkunKeuanganResource())
app.add_route('/api/akun-keuangan/options', OptionKeuanganResource())
app.add_route('/api/informasi-lembaga', InformasiLembagaResource())
app.add_route('/api/informasi-lembaga/{info_id}', InformasiLembagaResource())
app.add_route('/api/banner-aplikasi', BannerAplikasiResource())
app.add_route('/api/banner-aplikasi/{banner_id}', BannerAplikasiResource())
app.add_route('/api/setting-user', SettingUserResource())
app.add_route('/api/setting-user/options', SettingUserResource())
app.add_route('/api/backup-data', BackupDataResource())
app.add_route('/api/absensi-gps', AbsensiGpsResource())
app.add_route('/api/dashboard-statistik', DashboardAplikasiResource())

if __name__ == '__main__':
    from models.schema import *

    db.generate_mapping(create_tables=True)

    with db_session:
        if AdminUser.select().count() == 0:
            AdminUser(name="Bos Dika", email="admin@sap.com", password="password123")
            print("Akun admin default (Email: admin@sap.com, Pass: password123)")

    print("Server Mini Project jalan di http://localhost:8000")
    serve(app, host='0.0.0.0', port=8000)
