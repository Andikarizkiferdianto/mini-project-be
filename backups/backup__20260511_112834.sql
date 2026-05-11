-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: sap_database
-- ------------------------------------------------------
-- Server version	10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `absensi`
--

DROP TABLE IF EXISTS `absensi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `absensi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `siswa` int(11) NOT NULL,
  `tanggal` datetime NOT NULL,
  `status_hadir` varchar(255) NOT NULL,
  `jam_masuk` varchar(255) NOT NULL,
  `jam_pulang` varchar(255) NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_absensi__siswa` (`siswa`),
  CONSTRAINT `fk_absensi__siswa` FOREIGN KEY (`siswa`) REFERENCES `siswa` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `absensi`
--

LOCK TABLES `absensi` WRITE;
/*!40000 ALTER TABLE `absensi` DISABLE KEYS */;
/*!40000 ALTER TABLE `absensi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `admin_user`
--

DROP TABLE IF EXISTS `admin_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `admin_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `created_date` datetime NOT NULL,
  `updated_date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_user`
--

LOCK TABLES `admin_user` WRITE;
/*!40000 ALTER TABLE `admin_user` DISABLE KEYS */;
INSERT INTO `admin_user` VALUES (1,'Bos Dika','admin@sap.com','password123','2026-05-11 09:55:50','2026-04-16 09:08:28','2026-04-16 09:08:28');
/*!40000 ALTER TABLE `admin_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `akun_keuangan`
--

DROP TABLE IF EXISTS `akun_keuangan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `akun_keuangan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `akun_id` int(11) DEFAULT NULL,
  `nomor_rekening` varchar(50) DEFAULT NULL,
  `kategori` enum('KAS','BANK') DEFAULT NULL,
  `jenis_arus_kas` enum('Operasi','Investasi','Pendanaan') DEFAULT NULL,
  `keterangan` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `akun_keuangan`
--

LOCK TABLES `akun_keuangan` WRITE;
/*!40000 ALTER TABLE `akun_keuangan` DISABLE KEYS */;
INSERT INTO `akun_keuangan` VALUES (1,1,'123-456-789','BANK','Operasi','Bank BNI Operasional Sekolah');
/*!40000 ALTER TABLE `akun_keuangan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aspek_penilaian`
--

DROP TABLE IF EXISTS `aspek_penilaian`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `aspek_penilaian` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_aspek` varchar(255) NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  `can_edit` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aspek_penilaian`
--

LOCK TABLES `aspek_penilaian` WRITE;
/*!40000 ALTER TABLE `aspek_penilaian` DISABLE KEYS */;
INSERT INTO `aspek_penilaian` VALUES (1,'Nilai Harian','Nilai dari tugas dan kuis harian',1),(2,'Ujian kompetisi','Ujian yang dilakukan 6 bulan sekali\'',1);
/*!40000 ALTER TABLE `aspek_penilaian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `role` varchar(50) NOT NULL,
  `username` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`role`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `banner_aplikasi`
--

DROP TABLE IF EXISTS `banner_aplikasi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banner_aplikasi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_file` varchar(255) NOT NULL,
  `preview_url` varchar(255) DEFAULT NULL,
  `diunggah` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banner_aplikasi`
--

LOCK TABLES `banner_aplikasi` WRITE;
/*!40000 ALTER TABLE `banner_aplikasi` DISABLE KEYS */;
INSERT INTO `banner_aplikasi` VALUES (1,'banner_1758514505.jpg','https://link-gambar-kamu.com/banner.jpg','2026-05-11 03:22:30');
/*!40000 ALTER TABLE `banner_aplikasi` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bayar_tagihan`
--

DROP TABLE IF EXISTS `bayar_tagihan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `bayar_tagihan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `siswa` int(11) NOT NULL,
  `jenis_pembayaran` int(11) NOT NULL,
  `nominal` double NOT NULL,
  `tanggal_bayar` datetime NOT NULL,
  `metode_pembayaran` varchar(255) NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_bayar_tagihan__jenis_pembayaran` (`jenis_pembayaran`),
  KEY `idx_bayar_tagihan__siswa` (`siswa`),
  CONSTRAINT `fk_bayar_tagihan__jenis_pembayaran` FOREIGN KEY (`jenis_pembayaran`) REFERENCES `jenis_pembayaran` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_bayar_tagihan__siswa` FOREIGN KEY (`siswa`) REFERENCES `siswa` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bayar_tagihan`
--

LOCK TABLES `bayar_tagihan` WRITE;
/*!40000 ALTER TABLE `bayar_tagihan` DISABLE KEYS */;
INSERT INTO `bayar_tagihan` VALUES (2,6,1,250000,'2026-05-05 00:00:00','',''),(4,6,1,250000,'2026-05-05 00:00:00','','');
/*!40000 ALTER TABLE `bayar_tagihan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `belanja`
--

DROP TABLE IF EXISTS `belanja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `belanja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_item` varchar(255) NOT NULL,
  `nominal` double NOT NULL,
  `tanggal` datetime NOT NULL,
  `kategori` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `belanja`
--

LOCK TABLES `belanja` WRITE;
/*!40000 ALTER TABLE `belanja` DISABLE KEYS */;
/*!40000 ALTER TABLE `belanja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `budgeting`
--

DROP TABLE IF EXISTS `budgeting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `budgeting` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tahun_ajaran_id` int(11) DEFAULT NULL,
  `akun_id` int(11) DEFAULT NULL,
  `nominal_target` decimal(15,2) DEFAULT NULL,
  `keterangan` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budgeting`
--

LOCK TABLES `budgeting` WRITE;
/*!40000 ALTER TABLE `budgeting` DISABLE KEYS */;
INSERT INTO `budgeting` VALUES (1,1,5,5000000.00,'Budget untuk pemeliharaan gedung');
/*!40000 ALTER TABLE `budgeting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buku`
--

DROP TABLE IF EXISTS `buku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `buku` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judul_buku` varchar(255) NOT NULL,
  `penulis` varchar(255) NOT NULL,
  `penerbit` varchar(255) NOT NULL,
  `tahun` int(11) NOT NULL,
  `isbn` varchar(255) NOT NULL,
  `barcode` varchar(255) DEFAULT NULL,
  `harga` decimal(12,2) DEFAULT NULL,
  `kondisi` varchar(255) NOT NULL,
  `kategori` varchar(255) NOT NULL,
  `rak` varchar(255) NOT NULL,
  `stok` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `barcode` (`barcode`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buku`
--

LOCK TABLES `buku` WRITE;
/*!40000 ALTER TABLE `buku` DISABLE KEYS */;
INSERT INTO `buku` VALUES (4,'Pemrograman Python Pro','Narendra Sakti','Erlangga',2026,'978-623-123-456-7','BK1777864965',150000.00,'Baik','Teknologi','Rak A1',4),(5,'Bahasa indonesia','Fadhill','Erlangga',2026,'978-623-123-456-8','BK1777866095',150000.00,'Baik','Pelajaran','Rak A2',1),(6,'Bahasa inggris','Fadhill','Erlangga',2026,'999-777-133-556-3','BK1777866467',150000.00,'Baik','Pelajaran','Rak A2',5),(7,'Bahasa Java','Sakti','Erlangga',2026,'999-777-133-556-1','BK1777866557',0.00,'Baik','Pelajaran','Rak A3',2);
/*!40000 ALTER TABLE `buku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ekstrakurikuler`
--

DROP TABLE IF EXISTS `ekstrakurikuler`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ekstrakurikuler` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_ekskul` varchar(255) NOT NULL,
  `pembina` varchar(255) NOT NULL,
  `jadwal` varchar(255) NOT NULL,
  `tanggal` datetime DEFAULT NULL,
  `keterangan` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ekstrakurikuler`
--

LOCK TABLES `ekstrakurikuler` WRITE;
/*!40000 ALTER TABLE `ekstrakurikuler` DISABLE KEYS */;
INSERT INTO `ekstrakurikuler` VALUES (1,'Pramuka','Jayadi','Sabtu','2025-07-12 00:00:00','Latihan rutin persiapan lomba');
/*!40000 ALTER TABLE `ekstrakurikuler` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guru`
--

DROP TABLE IF EXISTS `guru`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guru` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  `nip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nip` (`nip`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guru`
--

LOCK TABLES `guru` WRITE;
/*!40000 ALTER TABLE `guru` DISABLE KEYS */;
INSERT INTO `guru` VALUES (1,'Eka Prasetyo','12345');
/*!40000 ALTER TABLE `guru` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `informasi_lembaga`
--

DROP TABLE IF EXISTS `informasi_lembaga`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `informasi_lembaga` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judul` varchar(255) NOT NULL,
  `isi` text NOT NULL,
  `tanggal` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informasi_lembaga`
--

LOCK TABLES `informasi_lembaga` WRITE;
/*!40000 ALTER TABLE `informasi_lembaga` DISABLE KEYS */;
INSERT INTO `informasi_lembaga` VALUES (1,'Informasi Maintenance Sistem','Sedang ada informasi maintenance sistem hari ini','2025-05-11','2026-05-11 03:15:36');
/*!40000 ALTER TABLE `informasi_lembaga` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jadwal_mengajar`
--

DROP TABLE IF EXISTS `jadwal_mengajar`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jadwal_mengajar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hari` varchar(255) NOT NULL,
  `jam` varchar(255) NOT NULL,
  `guru` int(11) NOT NULL,
  `mapel` int(11) NOT NULL,
  `kelas` int(11) NOT NULL,
  `semester` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_jadwal_mengajar__guru` (`guru`),
  KEY `idx_jadwal_mengajar__kelas` (`kelas`),
  KEY `idx_jadwal_mengajar__mapel` (`mapel`),
  KEY `idx_jadwal_mengajar__semester` (`semester`),
  CONSTRAINT `fk_jadwal_mengajar__guru` FOREIGN KEY (`guru`) REFERENCES `guru` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_jadwal_mengajar__kelas` FOREIGN KEY (`kelas`) REFERENCES `kelas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_jadwal_mengajar__mapel` FOREIGN KEY (`mapel`) REFERENCES `mata_pelajaran` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_jadwal_mengajar__semester` FOREIGN KEY (`semester`) REFERENCES `semester` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jadwal_mengajar`
--

LOCK TABLES `jadwal_mengajar` WRITE;
/*!40000 ALTER TABLE `jadwal_mengajar` DISABLE KEYS */;
INSERT INTO `jadwal_mengajar` VALUES (1,'Senin','12:00 - 17:00',1,1,7,1);
/*!40000 ALTER TABLE `jadwal_mengajar` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jenis_belanja`
--

DROP TABLE IF EXISTS `jenis_belanja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jenis_belanja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `akun_belanja` varchar(255) NOT NULL,
  `akun_harta` varchar(255) NOT NULL,
  `kode_akun` varchar(255) NOT NULL,
  `nama_akun` varchar(255) NOT NULL,
  `jenis` varchar(255) NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kode_akun` (`kode_akun`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_belanja`
--

LOCK TABLES `jenis_belanja` WRITE;
/*!40000 ALTER TABLE `jenis_belanja` DISABLE KEYS */;
INSERT INTO `jenis_belanja` VALUES (1,'5.0.9','1.0.1','5.1','Bisyarah Guru','Tanpa Pembatasan','','Aktif');
/*!40000 ALTER TABLE `jenis_belanja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jenis_pembayaran`
--

DROP TABLE IF EXISTS `jenis_pembayaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jenis_pembayaran` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kode_akun` varchar(255) NOT NULL,
  `nama_pembayaran` varchar(255) NOT NULL,
  `akun_harta` varchar(255) NOT NULL,
  `akun_pendapatan` varchar(255) NOT NULL,
  `akun_hutang` varchar(255) NOT NULL,
  `tipe` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `nominal_ketetapan` double DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_pembayaran`
--

LOCK TABLES `jenis_pembayaran` WRITE;
/*!40000 ALTER TABLE `jenis_pembayaran` DISABLE KEYS */;
INSERT INTO `jenis_pembayaran` VALUES (1,'400.1','SPP Bulanan','1.0.1 Kas','2.0.2 Pendapatan SPP','--','Bulanan','aktif',0);
/*!40000 ALTER TABLE `jenis_pembayaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jenis_penerimaan`
--

DROP TABLE IF EXISTS `jenis_penerimaan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jenis_penerimaan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `akun_harta` varchar(255) NOT NULL,
  `akun_pendapatan` varchar(255) NOT NULL,
  `kode_penerimaan` varchar(255) NOT NULL,
  `nama_akun` varchar(255) NOT NULL,
  `jenis` varchar(255) NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_penerimaan`
--

LOCK TABLES `jenis_penerimaan` WRITE;
/*!40000 ALTER TABLE `jenis_penerimaan` DISABLE KEYS */;
INSERT INTO `jenis_penerimaan` VALUES (2,'1.0.1 - Kas','4.0.4 - Pendapatan BOS','3','Pendapatan BOSDA','Dengan Pembatasan','Dana BOS Daerah','Aktif');
/*!40000 ALTER TABLE `jenis_penerimaan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jenis_semester`
--

DROP TABLE IF EXISTS `jenis_semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jenis_semester` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_semester`
--

LOCK TABLES `jenis_semester` WRITE;
/*!40000 ALTER TABLE `jenis_semester` DISABLE KEYS */;
INSERT INTO `jenis_semester` VALUES (1,'Penilaian Tengah Semester (PTS)');
/*!40000 ALTER TABLE `jenis_semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jurnal`
--

DROP TABLE IF EXISTS `jurnal`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jurnal` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tanggal` date NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  `kode_akun` varchar(255) NOT NULL,
  `nama_akun` varchar(255) NOT NULL,
  `debet` double NOT NULL,
  `kredit` double NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jurnal`
--

LOCK TABLES `jurnal` WRITE;
/*!40000 ALTER TABLE `jurnal` DISABLE KEYS */;
INSERT INTO `jurnal` VALUES (1,'2026-05-08','Pembayaran Gaji Guru Mei','5.1.1','Beban Gaji Guru dan Karyawan',5000000,0,'Posting'),(2,'2026-05-08','Pembayaran Gaji Guru Mei','5.1.1','Beban Gaji Guru dan Karyawan',5000000,0,'Posting');
/*!40000 ALTER TABLE `jurnal` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jurusan`
--

DROP TABLE IF EXISTS `jurusan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jurusan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kode_jurusan` varchar(255) NOT NULL,
  `nama_jurusan` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `kode_jurusan` (`kode_jurusan`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jurusan`
--

LOCK TABLES `jurusan` WRITE;
/*!40000 ALTER TABLE `jurusan` DISABLE KEYS */;
INSERT INTO `jurusan` VALUES (1,'RPL','Rekayasa Perangkat Lunak'),(2,'DKV','Desain Komunikasi Visual'),(3,'TSM','Teknik Sepeda motor'),(4,'TKJ','Teknik komputer dan jaringan'),(5,'TE','Teknik Elektronik');
/*!40000 ALTER TABLE `jurusan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kelas`
--

DROP TABLE IF EXISTS `kelas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kelas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `kode_kelas` varchar(255) NOT NULL,
  `nama_kelas` varchar(255) NOT NULL,
  `jurusan` int(11) DEFAULT NULL,
  `tahun_ajaran` int(11) DEFAULT NULL,
  `wali_kelas_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_kelas__jurusan` (`jurusan`),
  KEY `idx_kelas__tahun_ajaran` (`tahun_ajaran`),
  CONSTRAINT `fk_kelas__jurusan` FOREIGN KEY (`jurusan`) REFERENCES `jurusan` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_kelas__tahun_ajaran` FOREIGN KEY (`tahun_ajaran`) REFERENCES `tahun_ajaran` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kelas`
--

LOCK TABLES `kelas` WRITE;
/*!40000 ALTER TABLE `kelas` DISABLE KEYS */;
INSERT INTO `kelas` VALUES (3,'X-DKV','Sepuluh DKV',1,NULL,'Sakti'),(4,'X-RPL','Sepuluh RPL',2,NULL,'Fadhil'),(5,'X-TKJ','Sepuluh TKJ',3,NULL,'Luna'),(6,'X-TE','Sepuluh TE',4,NULL,'Elaina'),(7,'7A','VII A',NULL,NULL,'Nama Wali Kelasnya');
/*!40000 ALTER TABLE `kelas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mata_pelajaran`
--

DROP TABLE IF EXISTS `mata_pelajaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mata_pelajaran` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_mapel` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mata_pelajaran`
--

LOCK TABLES `mata_pelajaran` WRITE;
/*!40000 ALTER TABLE `mata_pelajaran` DISABLE KEYS */;
INSERT INTO `mata_pelajaran` VALUES (1,'Bahasa Indonesia'),(2,'Bahasa Jepang');
/*!40000 ALTER TABLE `mata_pelajaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `peminjaman`
--

DROP TABLE IF EXISTS `peminjaman`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `peminjaman` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `siswa` int(11) NOT NULL,
  `buku` int(11) NOT NULL,
  `tgl_pinjam` date NOT NULL,
  `tgl_kembali` date NOT NULL,
  `tgl_aktual_kembali` date DEFAULT NULL,
  `status` varchar(255) NOT NULL,
  `jumlah` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_peminjaman__buku` (`buku`),
  KEY `idx_peminjaman__siswa` (`siswa`),
  CONSTRAINT `fk_peminjaman__buku` FOREIGN KEY (`buku`) REFERENCES `buku` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_peminjaman__siswa` FOREIGN KEY (`siswa`) REFERENCES `siswa` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peminjaman`
--

LOCK TABLES `peminjaman` WRITE;
/*!40000 ALTER TABLE `peminjaman` DISABLE KEYS */;
/*!40000 ALTER TABLE `peminjaman` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `penerimaan`
--

DROP TABLE IF EXISTS `penerimaan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `penerimaan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_penerimaan` varchar(255) NOT NULL,
  `sumber` varchar(255) NOT NULL,
  `nominal` double NOT NULL,
  `tanggal` date NOT NULL,
  `menyetujui` varchar(255) NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penerimaan`
--

LOCK TABLES `penerimaan` WRITE;
/*!40000 ALTER TABLE `penerimaan` DISABLE KEYS */;
INSERT INTO `penerimaan` VALUES (1,'Pendapatan BOS','Pemerintah Pusat',5000000,'2026-05-06','Kepala Sekolah','Dana BOS Reguler Tahap 1');
/*!40000 ALTER TABLE `penerimaan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `riwayat_backup`
--

DROP TABLE IF EXISTS `riwayat_backup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `riwayat_backup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_file` varchar(255) NOT NULL,
  `path_file` text NOT NULL,
  `ukuran_file` varchar(50) DEFAULT NULL,
  `dibuat_pada` timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `riwayat_backup`
--

LOCK TABLES `riwayat_backup` WRITE;
/*!40000 ALTER TABLE `riwayat_backup` DISABLE KEYS */;
/*!40000 ALTER TABLE `riwayat_backup` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `semester`
--

DROP TABLE IF EXISTS `semester`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `semester` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tahun_ajaran` int(11) NOT NULL,
  `jenis_semester` varchar(255) NOT NULL,
  `nama_semester` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_semester__tahun_ajaran` (`tahun_ajaran`),
  CONSTRAINT `fk_semester__tahun_ajaran` FOREIGN KEY (`tahun_ajaran`) REFERENCES `tahun_ajaran` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (1,1,'Ganjil','Semester 1');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `siswa`
--

DROP TABLE IF EXISTS `siswa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `siswa` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nis` varchar(255) NOT NULL,
  `nisn` varchar(255) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `tempat_lahir` varchar(255) NOT NULL,
  `tgl_lahir` datetime DEFAULT NULL,
  `jenis_kelamin` varchar(255) NOT NULL,
  `alamat` longtext NOT NULL,
  `agama` varchar(255) NOT NULL,
  `golongan_darah` varchar(255) NOT NULL,
  `status_aktif` tinyint(1) NOT NULL,
  `tahun_ajaran` varchar(255) NOT NULL,
  `tahun_masuk` varchar(255) NOT NULL,
  `sekolah_asal` varchar(255) NOT NULL,
  `no_hp` varchar(255) NOT NULL,
  `nama_ayah` varchar(255) NOT NULL,
  `pekerjaan_ayah` varchar(255) NOT NULL,
  `no_hp_ayah` varchar(255) NOT NULL,
  `nama_ibu` varchar(255) NOT NULL,
  `pekerjaan_ibu` varchar(255) NOT NULL,
  `no_hp_ibu` varchar(255) NOT NULL,
  `nama_wali` varchar(255) NOT NULL,
  `no_hp_wali` varchar(255) NOT NULL,
  `hubungan_wali` varchar(255) NOT NULL,
  `kelas` int(11) DEFAULT NULL,
  `jurusan` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nis` (`nis`),
  KEY `idx_siswa__jurusan` (`jurusan`),
  KEY `idx_siswa__kelas` (`kelas`),
  CONSTRAINT `fk_siswa__jurusan` FOREIGN KEY (`jurusan`) REFERENCES `jurusan` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_siswa__kelas` FOREIGN KEY (`kelas`) REFERENCES `kelas` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `siswa`
--

LOCK TABLES `siswa` WRITE;
/*!40000 ALTER TABLE `siswa` DISABLE KEYS */;
INSERT INTO `siswa` VALUES (6,'42534523','42534523','yurayura','wwww','2026-05-06 00:00:00','L','wwwwwwwwww','islam','B',0,'2025/2026','2025','wwwwwwwwwwww','23523523523','','','','','','','','','',3,2);
/*!40000 ALTER TABLE `siswa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tabungan`
--

DROP TABLE IF EXISTS `tabungan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tabungan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `siswa` int(11) NOT NULL,
  `tanggal` datetime NOT NULL,
  `jenis_transaksi` varchar(255) NOT NULL,
  `nominal` double NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_tabungan__siswa` (`siswa`),
  CONSTRAINT `fk_tabungan__siswa` FOREIGN KEY (`siswa`) REFERENCES `siswa` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabungan`
--

LOCK TABLES `tabungan` WRITE;
/*!40000 ALTER TABLE `tabungan` DISABLE KEYS */;
INSERT INTO `tabungan` VALUES (1,6,'2026-05-06 09:59:13','Setoran',50000,'Menabung awal'),(2,6,'2026-05-06 10:07:46','Setoran',25000,'Menabung awal');
/*!40000 ALTER TABLE `tabungan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tahun_ajaran`
--

DROP TABLE IF EXISTS `tahun_ajaran`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tahun_ajaran` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tahun` varchar(255) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tahun_ajaran`
--

LOCK TABLES `tahun_ajaran` WRITE;
/*!40000 ALTER TABLE `tahun_ajaran` DISABLE KEYS */;
INSERT INTO `tahun_ajaran` VALUES (1,'2026/2027','Tahun Pelajaran Baru',1),(2,'2024/2025','Semester Ganjil 2024',1),(3,'2024/2025','Semester Ganjil 2024',1);
/*!40000 ALTER TABLE `tahun_ajaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transaksi_belanja`
--

DROP TABLE IF EXISTS `transaksi_belanja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `transaksi_belanja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jenis_belanja` varchar(255) NOT NULL,
  `bidang` varchar(255) NOT NULL,
  `penerima` varchar(255) NOT NULL,
  `sumber` varchar(255) NOT NULL,
  `tanggal` datetime NOT NULL,
  `menyetujui` varchar(255) NOT NULL,
  `nominal` double NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaksi_belanja`
--

LOCK TABLES `transaksi_belanja` WRITE;
/*!40000 ALTER TABLE `transaksi_belanja` DISABLE KEYS */;
INSERT INTO `transaksi_belanja` VALUES (2,'Belanja Barang','Sarana Prasarana','Toko Bangunan Jaya','Dana Komite','2026-05-06 00:00:00','Kepala Sekolah',2500000,'Pembelian semen dan cat untuk renovasi pagar');
/*!40000 ALTER TABLE `transaksi_belanja` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-05-11 11:28:35
