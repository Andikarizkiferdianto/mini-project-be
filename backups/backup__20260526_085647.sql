-- MySQL dump 10.16  Distrib 10.1.29-MariaDB, for Win32 (AMD64)
--
-- Host: localhost    Database: sap_database
-- ------------------------------------------------------
-- Server version	10.1.29-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_user`
--

LOCK TABLES `admin_user` WRITE;
/*!40000 ALTER TABLE `admin_user` DISABLE KEYS */;
INSERT INTO `admin_user` VALUES (1,'Bos Dika','admin@sap.com','password123','2026-05-21 07:24:33','2026-04-20 08:33:23','2026-04-20 08:33:23');
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
  `akun_id` int(11) NOT NULL,
  `nomor_rekening` varchar(50) DEFAULT NULL,
  `kategori` varchar(20) DEFAULT NULL,
  `jenis_arus_kas` varchar(20) DEFAULT NULL,
  `keterangan` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `akun_keuangan`
--

LOCK TABLES `akun_keuangan` WRITE;
/*!40000 ALTER TABLE `akun_keuangan` DISABLE KEYS */;
INSERT INTO `akun_keuangan` VALUES (1,1,'0883','Aset','Investasi','d');
/*!40000 ALTER TABLE `akun_keuangan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `arsip_surat`
--

DROP TABLE IF EXISTS `arsip_surat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `arsip_surat` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomor_surat` varchar(100) NOT NULL,
  `tgl_surat` date DEFAULT NULL,
  `tgl_terima` date DEFAULT NULL,
  `sumber_surat` varchar(255) DEFAULT NULL,
  `perihal` text NOT NULL,
  `jenis_surat` varchar(50) DEFAULT 'Masuk',
  `file_surat` varchar(255) DEFAULT NULL,
  `keterangan` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arsip_surat`
--

LOCK TABLES `arsip_surat` WRITE;
/*!40000 ALTER TABLE `arsip_surat` DISABLE KEYS */;
INSERT INTO `arsip_surat` VALUES (1,'2','2026-05-20','2026-05-22','','Mark','Masuk','surat_a038e71d7efe43108b135e522650b619.png','test'),(4,'1','2026-05-20','2026-05-28','','Kram','Keluar','','test1');
/*!40000 ALTER TABLE `arsip_surat` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aspek_penilaian`
--

LOCK TABLES `aspek_penilaian` WRITE;
/*!40000 ALTER TABLE `aspek_penilaian` DISABLE KEYS */;
INSERT INTO `aspek_penilaian` VALUES (1,'Nilai Ulangan','Nilai',1);
/*!40000 ALTER TABLE `aspek_penilaian` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `banner_aplikasi`
--

DROP TABLE IF EXISTS `banner_aplikasi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banner_aplikasi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_file` varchar(255) DEFAULT NULL,
  `preview_url` text,
  `diunggah` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banner_aplikasi`
--

LOCK TABLES `banner_aplikasi` WRITE;
/*!40000 ALTER TABLE `banner_aplikasi` DISABLE KEYS */;
INSERT INTO `banner_aplikasi` VALUES (4,'aaa','https://i.pinimg.com/webp/736x/8c/ae/d9/8caed990de04215502ef378d011c9a53.webp','2026-05-15 06:52:08'),(5,'gwe','data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMWFhUXGBUXFhgXGBgaGBcYGBgXFxgYGBcYHSggGBolGxUXITEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGxAQGy0lHyUvLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLS0tLf/AABEIAKgBLAMBIgACEQEDEQH/xAAcAAACAgMBAQAAAAAAAAAAAAAEBgMFAAIHAQj/xABHEAABAgQEAwUFBQUGAwkAAAABAhEAAwQhBRIxQVFhcQYTIoGRMqGxwdEHFEJS8BUjYnLhJXSSosLxU7KzFiQzNUNjgsPS/8QAGgEAAwEBAQEAAAAAAAAAAAAAAQIDAAQFBv/EACwRAAICAgICAQIGAgMBAAAAAAABAhEDIRIxBEETIlEUMmFxkbEjgWLR8AX/2gAMAwEAAhEDEQA/AJzPOWzjX3aMxtpGtDOykzM2RSQwAZ1Gz8jofWK+sxIIcmyeevMt5QVKkmaylCwbQe4R0+NFuekNHsPpVpILoIBdspDu1i52iypZEzKCSCdMxF/KPMNo7XDJGg47wVWVYQGFz8I9RJrXbKBiVhCb3MUOKYw2l/hFViWNFyked/1aK0YiQpKmBKSCxDpsXYjcRxZfI4yqP8iN0FVGMLOhaIZleo/iJgPEqjvJilhCUBRfIn2Rbbhe/nEAjkllm32K2HGuVxgujxBWmcDr/tFEZkR99e0bHlcHZk6Hejrf4wTwFrfreLVKnY7whJxnL4prFI1LX914ZaCuQsApP66R6+LLDKtFU7DMTS/mDCviV5KCRcOl+Q0hsSsGK7FcOCpbJ4k+bQ2SPKDiZiLljIkmJYxpHgtURMeMbfQbk6DzjBFditWXKEkgJseat3A1H0gpewpBqZyCSAu9rnQ9D9WjdSN9RxBceohdkLIsQW4hnH1H0g2irMimKnSbGz9CA+vyO8HTDSLIxgjaali0aZoUU9FzaC6GuMs8txAi1gkkBhsH+ZjVQdyNud7/ABh4ScHaCnQyUmIJWW0ixlnKXhJkzcphrwyq7xHMR6Xj+R8n0y7KRlZegDaI1JgdMwt0MFpOYPFXGhgeepho8V04pOgaLpMl4HnUA1AiuNBQuT8MCvZcH3RY4NTTUBlqdOw1I6cBFhJlbNB0ujVwiixwjLkaiww5Xh9p+XCJ5lKheoHUQHS0eUu/pFnLERm6dpisHk4YgE7vxiuxPD0gsQFJPEP8Yv0CNpkkKDEPCxytPZkxTk0qEewlKX1YARKAYuZmDDZUFU+HhIbWLPPBLQ9o5nSUv3h0qSSkvrqH2ENWGUGQJSdEgAA3JYNfyiGhQiUlt+H63iwpySHOp05RPFh+KNL+REqCTMbkBCfjOLeIpSd7n5RZdpMQ7tGUamEqYt45/JzfGuMe2LJ0ETFvf9GBVYsJSwQRmGgYK9QQR6wHXVrZUjUv6dYAEu76kxwQxuWzQheyw/azDSC6Ks7wEs20U5pFcNYuqelKJYtbc8/lByQSWjTil0SlIINw4ZgXvdrfG8CBjw3HnBCoglSwkMOZ9YiTAcUJ8KRzJ8v0YOpFKSlNzYCPT+vUH5CMJhuWkkNeqGLs/XqJyqV0fX1i1n4mEryK0I1hNp1kEFousSrpS0g3zt6dY9LB5H+Pb2vuMno2x+glpSFo3P1hdMGVlepYAOidPd9ICeOHyJxnO4iSdmyTyhaxZJlzlNcWIdvxAE2HNx5QxxNR4bLqamjlTPYXOCV7Ohs5S40JykPzMTi9MyPexPZddZInzik+EoTL4KLvNLaqZJQ1x7R1Zo8xvsOqm7mbmU0xZdCwHyjKVKBDsPGAx33MdtppAlLQiUnu5UtJSmSkSxd7KAd231csOcIf2p42ldQKZKnMlGZf88zZ+IQAW/8Ac5WlCTlP9CrilERpq3MQkx4TEalQzIm+aJEEMXJCrNwI3B3gRSo1M3lBTMblRizwOsyLHCKlaiT1ialpJhNkn0imKM+ScUFX6H/pGVRUJE7K4PdrIbV2OnOI8DkrCQFl/l57xa5Wj3OFx2XKrsOFd1MQpRVkWwcuwyiw4DX1hiKYHo5KJKJkwm11K5BI34ln62jygr0zpYmocJLgg6gixiMNfSwGTpW41iSmq9jHqjEE6Rm6xZb7CHprEg8Y3TiHBMKeIY4ZE+RKKAoTFJCiSbAqCXA84cJVQgbiF+m6Ss1G8rEP4DBMmsB2I6iIkVcviIITVo/MInKP/E1BMsgxKI1l3EShMc7Ypz6iRnUOGsWylga2gPC0MCfIRpiR8Tco9OX1SoIr9p6h163b/aKIrsOUHY4t5qhsPkIrhHheXLlmkSl2G09NTlIUsnOeG3AQOmYE+yG2eNCI0zRP5ZVSDzdUF5SNRre/MP8AMQbIrJndzQlbBQT3gJHjSDZgRcgl7XvFWibo4cC7F2PHQ2jETGvw84VSp2LZZrkLRJRNChlm94ggajIUuD1dJgEmJamSUhASsTMyUrZLnKV2ykfmsPURAJaihSwPCgpCjwzOzjyMaS9GZmaL7CPu8oBc9BmE3Cc2UNo5a5uDblu8LRXHveE84EWkZHQ6btTRGyqNATuwSogbm6QTB1f2WpauX3tKQgnS5yE8CLlJ6W5Qg0eGKLKI8J2MMfYmumU9SmQq8ua4DaBWoPqffFXdBFKokKQopILgkEcxG02impSFFCglV0kggHoTrHV6zCkLXORMlju1jNLmJSDMEwsSEsHV4sym6vYmI6iZWpTnnZUyUh15DLCmA/i8KdtCeAhKiDRzOmwOomS1TUS1KQnUgfLU/KBJFYqQ87IFGUQtIU7PdN22ZRHnHa8PXJWUiXLIJSFOpCkFi7e2AVKfYO2paziYv2HoarMlcsgguTLWtJBN7gHK93uN+ca4oydCPS/alVDDFzjKQZqZvcCY6mGZOdKykg5iBa6rkAneFSoxFdSkT1IAUpgvK5fKlKQovdzlB6vHRKv7KUijXSSKghK5yZ2aanMoFKcuV0s45tAuB/ZTLkH9/Omzls4RKUJSSA3HxFuR35wsVFB5N9nPpFNMmFkJUo8ACT6CBphYtHY59YJCVSpcmXISQUnXNe11nVV94Xa7sGuYgrymWsl0ktkKW0VuhRLkEjKzB3hnBUA5wVx6kOYJxXCJ1PMMuagpUNv9tYjkImy1AhJB2t9YEIXKmZIvcGw/IRMmMBsCb3+EM1NTP7VuW8L2DUSleOY5UfZB+J+kNVHSlNzrwj6PDFY8dJV/ZZaROAAGEaGoDtEVVUNYa/CK6bUJRdSgOsOo6tmQyUKgXSbgjQ6HiI1w+jRKlBAPhdWvMkt5aRV4diaVMpN2MHmZ+8I2VcRyZKu0Fmv3kJOU+RjY1EQ1yBYnpHhRZoXlYALHKYTkpUAMyCCPIgs/UCKbEu1c2SpihJHQj5xdU8xix0MUvayhCpZIu3wMLk5xTcXszutENP2/ST45X+FXyIhgw7tJTziAlbKOyre/SOPqSxIjeWojSOSH/wBDIvzbEWRneZVQpPsqIixlYysBiAeccXw3tVVITlBzBIe4zMLb6gXi3k/aEpvFKSTyJHuvHX+KwZFsfnFnQpSWAAgHER4vKLCWYGxOXYHhaOmD+oyOa4ivxq6n4xvRSndR0F42xqnInKHN/W/zibEJfdSUDdTkjltHlLE1knKXoSt2V1RMBMRBcQFcbyklRYRxpOT0TJXjDOuzhLgA6t5trpGk1JTbeIkEZgoh2cgc7M/LfygqNSqWgrvYRLnEEEFmuCLEcw0EJlgy84mArz5e7Y5mbNnfQh3EBSlpJ8RIG5Ac+jj4xpKGZw4FiblhYEt1LMOcBGJSuCsLmIExJX7Lh30beK5EwPcPY2drkEA+RY+UerSUhJO4cMQdyNtC40jLWwDijFAsKylKSNHdjysYraqunS1Z3Dn2VJuE7kJ4E+G5vaF3vOBgqkqCygo+Frk3bhrFefJ0NdnSOwGJYhNmpz5l07HMuYmwF27tTAklQAa4tD/MQkHvJpDJPgB9lPBTbrPHbQbk/MUzFp6FlUqbMl6DwKUn3jWL3Bu21YVoTMInB7lb5wl7nMC1hxF4SrYp3mpqu/aTJJ8TFa8j92jinMGzlmS+l1XysSkSlU4ZKVTJbkm5VMBNySTeZ8dIr+xWIypsh5ZBJUSeOydOTN5c4vp4UQyCAeJD+geFemYC/bEn83JmLvwbjyjWtp1z0ZQ8oahf/qpOykJ0Sf5uJBSxIM1JhyUKzqJWv8ytv5eHvMR4ljEuWkkKSSOfhA3KjoI1fYxHSUBQtXeHvMxJQtQ8QtdChpZiQoAOHBDh1ey6KXL8IWQnQIzsEjgliGTy20DANCyftPonI76UW1ZRA8iUsfImIK37ScPzplTgoBTeJSHQHs+bYDc7QaZhjrOzNLNbNLdtCFrcdLxR9pTUSsqQR3Z8KMoDBgGSXu7Pq+kVWIdpZVItTVAShzkBVmzJ2ISHzDm0S0faNVXLzJm5pR1YAOQdCGcM2/LbXowQbyL2ho9kcuSQStZBJAcszNry4QHV4hw03JjfFZx9nzhB7R4ySTLQfCNTxP0j2Zzhhhyl/pFLoMxftJlOWXf+L6fWFmqr1rLqJL84EUsm8eJXHiZ/KyZXt6+xNybHrsZOJSoecN0xXhQrhb0vCX2JHtHl8xDclXhI6H5R3+PvGikej0omKnTQS8tSErSPykMLdbvG1FO/CddosqEvLHJxAX3fKsgixuk/KDHVxCBYjLKXI4EiKBOOS1JUib4bEPtDlUSMw5wjdoezpUStA4uOH9IWcpcbiZt+hMqyMxaB88TTpJBY7R5IlPePJfZAnkTlJfKspzJKFMSAUqspJbVJ4co0VLudNTpp5collU8FIpB1jGOzUqnSOkSVKMySIEwucCgX4N53EWCpbi1jtH0L1IuJeK0jrSpn2Pr/AFis7USFKWABbKPiYcJsghRzC8U+MyCVDYNr5mKTwxnFp+xnHQqSMKJsT5CLaVhwSLaxvMqkSxr5xWzsfG0RUcODql/YukGqwtJuWeI1YOiAk48OcboxlI/EY3yYJbuILQRMwlDRU1tKlIsCSYshjaOI9DE0qrlr4eULLHhyKlV/pRqTFdQI1BjV4bJ1GkpJJGXcq09YX6lUqWfCcx4nQdAbnrHnZ/E+PqX/AGI40RIpjqohPX6RHWVASAlILceJ5xFMrX2J6xqEZmWuydhurpy5+kRSS6FIZchU3kkanYfU8oPlT0yxlQLHUnVRGhP00gabUE8gNANBEKjCOf2MMFB2qm0K1qlAFUzuloc+BBCSlRyDUlhvduVzsZ+1WunZO7UJACEhfdgZlKtnIKnygnTe3lCliN0y1cin0JP+oQBDPbMx+qe2tXNpJk7vMi0zAgN4rNKuSp3UcyrwnYhi0+f/AONOXM5KUcv+HT3Ra09MP2VNmZg4qQnLv7Mkvrz4QvRgG0lGZSU8SB6losp88KUpKg6ST1B4p4GBcNHjB/KCr0Bb3tBeD0ZmzANtT03hoxcmox9hRHimHzktOW60KygL5AZUpUPwWAA20aLDsxjZplOm6T7aOPMfxCOk0tIlMrIpIIUGIIcM2hHBo512kwQSZhXJcof2dSg8Oaee0deXx3ifLH6/9/AzjW0XmK44mYgmWrxKsyhlIG+tn21hIqApJ8QIMTSqobjzEFJnJUMp8Q4bjpEM+WWauXoDdlRE0xBDONRqd+nk0Fqw/dBChw0PpvA65Z3BDXjkcWuxR77GSwJJO7tDRRozZhxB91/lCr2JW8tXJvnDfhI/eDm/wMevif8AiRePQThJsU8/18IKnyXDb/OAaBBE0jr84tVIhcmpAfYIkWeIKqn8Jtc69ItaakGRSzoCTAdPNSt1AgvwiiqKsPRyHtPhhRMPDUdIDoqVRICUv5R1DHcHTNs3T6RWVWGinlZUh1Kso8uAjml4vJuXoXh7FOTQ5iw34Q+YT2KeUCp36QV2G7Pd4rOoWe3COnJyIASLNCx44l1bZlUTi3ZqqK5eX8rX5HSHjDhmQD5Qm9lqTKhTcnPrDfRTkoQokgBNyToABcmPUcXHEk+yi6NsSkgAKhI7XzV5ApGgseXCHGhrDPllRTlBJyjfLsTwJ4bRU4hQeEhQdJcHzgQfKDinszOSTZpJuXiMqgzGaMypiknY+o2MVxMeBkUlJqXZzs3KoLk5G/C/MkRXkxPIQAM6x4Rp/EdgI0OzILnzgg5QgOWIbxODuHjFVQSysiQX5g+jtEaVZiZnFrq0SNAOelgOG0DzaobAEj8SgCfIaJirlWwhM+qmzb3bYmwHR7DyiOmpJRV+8nN/KH/zKsPQwHNnqVckmIyYHy7tq/3BY50mD07DKjMeKyVe72fdAeKYJqoKvz09YrcGxUyyyj4fhDlLSidKUQu9gAA4UC732a3rHfH4ssOiqpo56sEFjHkWWIYflUlJdJ0UpXsa+EgpDgNq41eKtdjHmTg4uiTVEs4vKHJR94f/AEwKuURrBcpLy24zE/8AKp4ImywQx/2ii6Ri4ph/Yc7++p/6cmFRKHtDpSUqv2HUf3xIH+GnMLMina+p+EBAPaCnOZaRc5WHmpMOGD4Z3KQlnWWf6dIWKWYUKUpOvgbq5/pHQez0lxLKrnKC553+cen4HBXJ9pFYotCkgAEud+sI2L1mWeGPsgnzP6EPlaWSdI5d2gUVTVKBsSQPJvpDZ8zhC/1C3RXVNWSSVJSp+IufMXjxPdq2Uk8i49Df3xDPgpE6SJIAEzvs5dTpyZG0A1ePJUnJt2SJEylD2VpWOD5Vf5re8xIutIYKHksF268IqgST1P66Rb0UiYvMAQpKSPaYhswTo9iSx6XcQVM1hVNja5N0sAS7BFj5/wBYb8BxGtmZJkqRJIIzDPMIcHdgC3nC7WdmFoQVSvEGJXKPtDV8h36G/Mwf9n/aSXJmCTNWyCklClaJJOZn2Bc9CG3jri5Q+mXvodNrsecFSorJmAJWxzJSSpIL6AkB/SLaYiAsHKZilTEEFKrpI3vrFrKl5lN69OMPLchn2A4wspplJGuVSvdHMMJXOTPCpZIfW9j1GhjpuKzHVyuPLSK7s/g6TP8AZvboDvFXFav9xi4RQNLzq9o/owIMK7yxFobaqkzFKBokXgqXQpBHL3mJ/iqQOSIsHoRKQAA3KNJ0tSiS0WE6Y3Xb6xWrnlRdKVKGjuQPIDaOWMpNuQib7OaYdNCXSOH6+MbYfWJnJUgnUZV8n3ig7N1eecu/4S3kRAeAVeSqyvZRKT56e9o9eWVOl6eilnTpKAkBI0GkeTZYIYwNLn+EcR7xBqS4cQji4mEPthgBmDMkOpI/xD6iObz5ZSWIaO/VEgKDGFPH+zMua5Iyq2UN+o3jnz+Os31R7/sWUbOY0uXdn/i0/rG9QQS5mDYEB9OScrQZjHZ6ZJNw42I0MDYRhZnLyaKLs+5F2jg4Ti+FbJ0+gSoqHslwl3uXPD5QOTBOIUC5SilQII4wHEZXexWbpBJtHhiagS8xI4n5GLCvw8ggkFJdtNdffY+kFQuNjKNqyq01EXVHjAlFJQ7EHODxezeUTYxheWTKWBZSX8wb/KF8xSXPC6NuJ0Z5NRKG5OzWba76u9mhd7QdnTKui7XLEK1vYix1gDAcRMteUnwH3HjD9Lmy1y0gg5gSSp/CUnk1jzjsjwzw2UVSRz9CQGT+UXF9VXPuy++NjG/eZ3XpmJUBwCi4HkCB5R4qORkxqp1D9hzRdzWjY/8ADk7+UKYhsQn+wz/fv/oT9IVUwqATYcgLmJR+bw6Gz3HvAjpOHSTmTsNugjmXe5GWNUELHVJzD4R2WXLDhtkj3x6HiTSjJFI9FZjhyofqfQGOX1s0m/6tHUcdlZkqfQJMKE3D0gFrAqcjUHZm4RDzXqKFmJs2iXrlN3bpxbhG0qX3S3mSgoCxSp2cjiGuHeGDEpUxPhTlAUNNSBYMOA56xNR4NnSHDgjTgRx6mOOMZN6FQvU9GCnMyjqGZ2trY8xrxi+whKlzJZCQMpAJAFynQm3AxbYbgJQSCPEd3dmJYEWceySOUWGFYYEqUq3Acmt6tr1i+PC/kpjKOyzSkk8+UVWJ/Z6ZqQuQrKpSlZkrPhYn8JCSRd7aMdovKeWXYecMSZxCQE7DWPQzQ5JKijVix2epMRp1S5U3u5srRSwp1pGUs7hObQDc3hxlTgmXMV+L2RAchcxb5Q8F01GQkqXrsOZ3ifHj2ZIoqkEs8MfZ6jynvFWJgygwuWRma8WUuUlPWEzeQmuMQOS6JUpjWdOCevD9bRrNm7J1+EBS1BayDoNX1UefLlHHGN7YiRIEqW50B35chBEqXlAD6co3M0DWPEzgdiYzbf7Ads+ZqGoVJU45jUPwLjziKXOImhY1cEeReNlU5BO4BbMNN2vzYmLKnwgrkzJoUgd2UukllkKLOkbh46knSRSh/p1hSUqGigCPODaOYxY6GE7Dcb7qlU7FaPZB3BPyL+oifBu2EqYck0d2rj+H6iO95oNU32PaHgh9IiVL4iB5SyGKS49xgz7wnKVEsEglXIAOTCyjx2CisrMLSoEMCDsdIXP+zMtE0LGZJBBbb6w8SWWlKkl0qAUDxBDg+kZOpkqDGApp/mVmEbtLgoqJZYDvB7J4/wAJjldTTqQohQZteMd5qqIo5jjFPivZ6VOGaYi+mYWPmd/OJ+R4yzfVF7BKPI4/htSETpa1B0hQzD+HRXuJgvFMZVPm5zZIPgTwFteKi1zF12s7KCQkLlkqRoX1SfLYwHhmB99IWpPtIILcRd/hHn/BkUuH+ydPoa6KnFTRBI9pLgdRf3vHPKuRkUQdn+MdE7AyVZFSz+ZPvcfKJu03ZcTSSPCvd9FcOh5x3ZcDzY4tfmoeUbRzNN26+n6AENMnEf8AuazlyqTL7twT4io5Aq5N/ENLWisq8EmSj4kaEa6aehHnGs6c0lI/NMDjWyf6kRwY3LHJpk1aMAaPVN+uukeZxxjUmABDesNgKedaf+kf/wAwoiHCvZGByU5kkqqwrwl2BlTjfnYgjiITwYCMekPaOxYGrPIlTN1S5Z/yj5xx4KHER2DsBNCqGUSNMyPRSgB6AR04JVY0SDFFeGZ0MLCZgJvu366Q64nTFSJhsLFI52JhPp6c5S7hThiOYYv6wPJXJxo0jeVgxnTHHn+vKHajwMS5Yt57mPexuHWv16w31NNmYDQRXksDUV37Y+o6EM4aoGyYKp8DUrZn0EOEqhA1gWvrgnwo10fh0hvxLk/pWw8vsV9LgCEWUsPvB9Th6cjIZhrFb3RN3iwopC3/AIYGRy7cjMnwwJTLLBgHvxiFNItRzHfbgIkqZZSCAQx2iOTVrvppEle5IH6oNmTLhALAan5ROKRPOAcNmJ39qCqysSkXU0SlFp8UK7vRLMTlHhGsV8mkU8Qy8XL8RBiMTB2huE4eg00SLpjt6xGmSsaRIqvHCB1YkdhCpTfoGzgVGlwhBQCyios4KwcvhJ2AYtwzGDBSsNH5RY0VODwFr/0g5VPbl+njtSocpe0FSJqUAS5UtKUs0oX1/GdSbPfjzhQqZJBdPl9IdqqgKtmGl9+YA5RCOzYUPG4HVj6CObLFsSSs87FY/MSkImgmUSUhbFkqZ8oOhsXbzh8VLCgQbpUCDwIIY+6FGh7N0qZcwL7wrdJleI5R+YEA7hvSDhKFgokgaAksPLSLY/I4R4vYylSGkYxSy0AKmoRlASwLsBYabRtV4vSgHNPl+SwT7o5viyhNmlGXwS7M4DqO5HABvUx592QhBIQkMCdPc8J8j9DJDdU9oJYshRWDxt8Ykw/HJQLKJynUEEt6Qq0SkrQFAs+1gRyghA8WRL5mcu7NpDfPKqDRf4iqnWkhKwpCrFKgQfeIXMNwpdNUeEFUpdn4cM3TjHs8K7pRPtMroGLWh0rchIUkMCAeVxFsWTm99r2YFRh6UKCkgDNlIYa+fKLfFMOMwBSR4ve0E0tMlctD7fKLCXLZ2OsCeZp69CtidUYeFpKVJzDgd/8AZvdHKe09KJVWJQ0SMw5ZiSx8gI+ifu6QC6RfW3F3+MfOfaCo7zEKhWwmLSOkv93b/C/nEs2VTj0LJ2iFUaERIRHsqW6gLtuQHIG5be0clCDeuclGCUilICx99WFJLgKAFXZxceyLjhCfNy5iUpyhyUgl2D2DtduMN9cn+wqe1hWTCPM1fyhXBEtaFAOQEKKZiQxOrEfiQbeR84y+xiJcwqJUdSSTs5NzYR1r7IVZqaYACcswjo6UK+KjHJ56gVEgAAl2AYB7kAObDQco6b9i1SwqUc0K9Qof6IZPsI5YhSJN7h7ECFX9mgliA725AQy1tTsCXc6l4ipsqVBw/H6R1Qh036HSJsEeWQDpDSg2ivORRT01iWdVZS2wiGZvJK62LLZPVPltFSmgJLxLMxEjeN5WJvuI0YzitBSaJabDwLmDCkQLIrXN48qixeJtSctitNvZvUUz6QDMoDwgoVrCPP2kBrDx+RdBXJAsugUNIgq6FWpMW6a5HGN0TUK4QflmnbRuTF+XSnhFlh0lI11izAEC1FOXcQHm56ZuVkhpAbkxn3MRDLnkaxL96ibU0DZyyiouMWaaMcI8oZZLARfU9KAOJj0ZSUSr0Uq6MgOwB9T/AEivnSWhoqJcU1XJOwjkk7EKWVT5VlWuZSSQdPCAGHAED3wVi9TISrNKBSGDpNyFOdLm2noYr8XztkStlH8oYJHMm/o0V0qhSln8Sjubkn5QEtbCkVsnByVCYVlJIzFrnMSSblwzHW7tE2M0oEvO6ixAueNnAFtYJlBc6Y2YiWhg3EDQdLacIuMRpCZExOX2kAi12Scwyk6OU6wxUXMPphnlEbkP1CiPkIZUU/75+KB7lf1ip7PSxMUg8C58r/SGcSf3w/kP/NCmZUYtT/u3H5iD0J+oENlPSFdPJmD/AIaH6hLH4RWYhS/ul+vvBMNvZumallpJds3o5ho5HB2JJ0SYbKAQOnxjYrUFtl8LWMGyqdv1b0idMgamEeRW2Tsr8WqEypMyarRCFKJ5AEn4R8v0KipSlK9ouVdVFz73jv32v1ok4ZNA1mNKA/nICv8ALmPlHAqBBuQeGz8YS9CsNjaXMKS6SUm9wWNwxuORIiO/Aevyj0Hl8IBhzrf/ACKmTxqiffWD/TC3WYjMnJkomkNKTkSoi4QWYKIuoJGnKGXElNgdIz3nqe1varh8D7oVKGmXOXkQHUyjewZCSo3NgwSY0TI1XIAzeIHKWBDkLu1i3AveHb7KwpH3pYHhIkpdwWIMxnGoHi109IRQbaH1Hyh2+zCUpdVNBLZpac2zgK3G75orjrlsZdj6mUWCjv8Aox6tQYMDb09ItcSASgAD+giuEp7R1RnyVjo3oKshQBgvGZzeIbxXBBSVApU4ysdi4e3SMrFKKGMBJOSaMayytdjpBRpuFjG+G5cgJIHW0eU2JyZhOSYklOoe8LPJTpAbIcy0HWD1V2aW/CA5pzF4FWkh4alLsJ6a5W14AStSlHNEoXlHit1/V43p1BSw1wBw+sXi0noKBV1SkqABgyVXqd3bpAC0Osnh843CIs4Ra2MXSMYO8WdHirwvSpNo2RZUcs8EH0K0hvExCg8YFIilkFZFriNu9Mcnw77E4lZh9OEjnuYtEJ4f0jIyKT+4WaTpIFz6xR100kkIH/y28oyMhUvYEUk+na5NyfMnlAWIysiT+ZVvLe8ZGRmUR7gdMMum5HzHxMXcuT+vlePIyFCA4RhiJE0pCzmJJSkixQRqFcQQxHQxaqltOTzSR84yMgGCaiS6VDiD8Ia8FlNIlc0JPrf5xkZE5k8jDREqRGRkSZJnF/t/xJ101MNs01XL8CPjM9I5nh/snr8hGRkV9G9hUZGRkYI7Y4hsEoec5Z/zVZ+ZhLBjIyFiZE1PL7xaUlaUuQMyyyRzJvZhDh9liT9+LuR3SyDdiErlhw+ojIyKxGR2NLKS43GsQSJKUOVC9r9Y8jIHT4hRXYvPllRQpaUuCPaAN+ERUdXTISkKmgsANCdAzkgR5GRX1SGKbtROkIUkpWFJWlQBQQcqxe42cH3QhYpha0qzybKZ/rGRkNFX2FaRNgvack5J4Y6O0NVMrvA6AVDlGRkTbpBeiU0az+H1aLfA6ZnfgfhGRkUxzbTFsHCPEYJRIjIyO2cmMw5Em0CZPGYyMiEG2AYsKkslzvAFajKsgRkZHLjbeRiRdyP/2Q==','2026-05-19 02:19:40');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bayar_tagihan`
--

LOCK TABLES `bayar_tagihan` WRITE;
/*!40000 ALTER TABLE `bayar_tagihan` DISABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
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
  `tahun_ajaran_id` int(11) NOT NULL,
  `akun_id` int(11) NOT NULL,
  `nominal_target` decimal(15,2) NOT NULL DEFAULT '0.00',
  `keterangan` text,
  PRIMARY KEY (`id`),
  KEY `tahun_ajaran_id` (`tahun_ajaran_id`),
  KEY `akun_id` (`akun_id`),
  CONSTRAINT `budgeting_ibfk_1` FOREIGN KEY (`tahun_ajaran_id`) REFERENCES `tahun_ajaran` (`id`) ON DELETE CASCADE,
  CONSTRAINT `budgeting_ibfk_2` FOREIGN KEY (`akun_id`) REFERENCES `siswa` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `budgeting`
--

LOCK TABLES `budgeting` WRITE;
/*!40000 ALTER TABLE `budgeting` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buku`
--

LOCK TABLES `buku` WRITE;
/*!40000 ALTER TABLE `buku` DISABLE KEYS */;
INSERT INTO `buku` VALUES (2,'Yuiga','Reyn','Erlangga',2025,'2','BK1778123958',0.00,'Baik','Asf','1',1),(3,'yy','pp','Erlangga',2098,'1','BK1778896254',0.00,'Baik','pp','1',0);
/*!40000 ALTER TABLE `buku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dokumen_sekolah`
--

DROP TABLE IF EXISTS `dokumen_sekolah`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dokumen_sekolah` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judul` varchar(255) NOT NULL,
  `tanggal` date NOT NULL,
  `deskripsi` text,
  `file_dokumen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dokumen_sekolah`
--

LOCK TABLES `dokumen_sekolah` WRITE;
/*!40000 ALTER TABLE `dokumen_sekolah` DISABLE KEYS */;
INSERT INTO `dokumen_sekolah` VALUES (1,'Surat','2026-05-20','Test','dok_1f111bc85fbc4a24868cd1691f29e804.png');
/*!40000 ALTER TABLE `dokumen_sekolah` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ekstrakurikuler`
--

LOCK TABLES `ekstrakurikuler` WRITE;
/*!40000 ALTER TABLE `ekstrakurikuler` DISABLE KEYS */;
INSERT INTO `ekstrakurikuler` VALUES (1,'Pramuka','Bob','Jum\'at','2026-04-24 00:00:00','ddd'),(2,'Futsal','Nan','Senin','2026-04-28 00:00:00','PP');
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guru`
--

LOCK TABLES `guru` WRITE;
/*!40000 ALTER TABLE `guru` DISABLE KEYS */;
/*!40000 ALTER TABLE `guru` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `guru_pegawai`
--

DROP TABLE IF EXISTS `guru_pegawai`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `guru_pegawai` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tipe` varchar(20) NOT NULL DEFAULT 'GURU',
  `nama` varchar(150) NOT NULL,
  `nip` varchar(50) DEFAULT '-',
  `jabatan` varchar(100) DEFAULT NULL,
  `no_hp` varchar(20) DEFAULT '-',
  `email` varchar(100) DEFAULT '-',
  `status` varchar(20) DEFAULT 'Aktif',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `guru_pegawai`
--

LOCK TABLES `guru_pegawai` WRITE;
/*!40000 ALTER TABLE `guru_pegawai` DISABLE KEYS */;
INSERT INTO `guru_pegawai` VALUES (1,'GURU','Aizen Sosuke','123400','PJOK','0871','Aizen123@gmail.com','Aktif'),(2,'PEGAWAI','Ichigo','1223','Tata Usaha','0881','Mnrva@gmail.com','Aktif'),(3,'GURU','Nagumo','1223','ORDER','082321','amjay21@gmail.com','Aktif');
/*!40000 ALTER TABLE `guru_pegawai` ENABLE KEYS */;
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `informasi_lembaga`
--

LOCK TABLES `informasi_lembaga` WRITE;
/*!40000 ALTER TABLE `informasi_lembaga` DISABLE KEYS */;
INSERT INTO `informasi_lembaga` VALUES (1,'Informasi Maintenance Sistem','Sedang ada informasi maintenance siste','2026-05-15');
/*!40000 ALTER TABLE `informasi_lembaga` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventaris_aset`
--

DROP TABLE IF EXISTS `inventaris_aset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `inventaris_aset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_aset` varchar(255) NOT NULL,
  `kategori` varchar(100) NOT NULL,
  `lokasi` varchar(100) NOT NULL,
  `jumlah` int(11) NOT NULL DEFAULT '0',
  `harga_perolehan` decimal(15,2) NOT NULL DEFAULT '0.00',
  `umur_ekonomis` int(11) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventaris_aset`
--

LOCK TABLES `inventaris_aset` WRITE;
/*!40000 ALTER TABLE `inventaris_aset` DISABLE KEYS */;
INSERT INTO `inventaris_aset` VALUES (2,'Komputer','Furniture','Ruangan Kelas 1',2,2000.00,5,'2026-05-20 07:25:05'),(3,'Kulkas','Elektronik','Ruangan Kelas 2',2,200000.00,5,'2026-05-21 01:19:43'),(4,'Test','Furniture','Ruangan Kelas 1',1,200.00,2,'2026-05-21 01:31:50');
/*!40000 ALTER TABLE `inventaris_aset` ENABLE KEYS */;
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
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jadwal_mengajar`
--

LOCK TABLES `jadwal_mengajar` WRITE;
/*!40000 ALTER TABLE `jadwal_mengajar` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_belanja`
--

LOCK TABLES `jenis_belanja` WRITE;
/*!40000 ALTER TABLE `jenis_belanja` DISABLE KEYS */;
INSERT INTO `jenis_belanja` VALUES (1,'5.0.9 - Beban Gaji Guru dan Karyawan','1.0.1 - Kas','1','Bos','Tanpa Pembatasan','','Aktif');
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
  `nominal_ketetapan` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_pembayaran`
--

LOCK TABLES `jenis_pembayaran` WRITE;
/*!40000 ALTER TABLE `jenis_pembayaran` DISABLE KEYS */;
INSERT INTO `jenis_pembayaran` VALUES (2,'123213','Test','1.0.1 - Kas','1.0.1 - Kas','1.0.1 - Kas','Bebas','Aktif',0);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_penerimaan`
--

LOCK TABLES `jenis_penerimaan` WRITE;
/*!40000 ALTER TABLE `jenis_penerimaan` DISABLE KEYS */;
INSERT INTO `jenis_penerimaan` VALUES (1,'1.0.1 - Kas','4.0.4 - Pendapatan BOS','1','Pendapatan BOS','Tanpa Pembatasan','','Aktif');
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jenis_semester`
--

LOCK TABLES `jenis_semester` WRITE;
/*!40000 ALTER TABLE `jenis_semester` DISABLE KEYS */;
INSERT INTO `jenis_semester` VALUES (1,'Penilaian Akhir Tahun (PAT)');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jurnal`
--

LOCK TABLES `jurnal` WRITE;
/*!40000 ALTER TABLE `jurnal` DISABLE KEYS */;
INSERT INTO `jurnal` VALUES (1,'2026-05-15','Lunas','1','Bos',222,20,'Posting'),(2,'2026-05-16','Lunas','1','Bos',111,111,'Posting');
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jurusan`
--

LOCK TABLES `jurusan` WRITE;
/*!40000 ALTER TABLE `jurusan` DISABLE KEYS */;
INSERT INTO `jurusan` VALUES (2,'1','PJOK'),(4,'2','IPA');
/*!40000 ALTER TABLE `jurusan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `kegiatan_sekolah`
--

DROP TABLE IF EXISTS `kegiatan_sekolah`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kegiatan_sekolah` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `judul` varchar(255) NOT NULL,
  `tanggal` date NOT NULL,
  `deskripsi` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kegiatan_sekolah`
--

LOCK TABLES `kegiatan_sekolah` WRITE;
/*!40000 ALTER TABLE `kegiatan_sekolah` DISABLE KEYS */;
INSERT INTO `kegiatan_sekolah` VALUES (1,'Gladi Bersih','2026-05-12','R'),(2,'voli','2026-08-06','dd');
/*!40000 ALTER TABLE `kegiatan_sekolah` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kelas`
--

LOCK TABLES `kelas` WRITE;
/*!40000 ALTER TABLE `kelas` DISABLE KEYS */;
INSERT INTO `kelas` VALUES (1,'X-TKJ-1','X TKJ 1',NULL,NULL,'Pak Lu'),(2,'XII-TKJ-2','XII TKJ 2',NULL,NULL,'Pak Budi'),(3,'Alumni','Alumni',NULL,NULL,'PAk');
/*!40000 ALTER TABLE `kelas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_cuti`
--

DROP TABLE IF EXISTS `log_cuti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_cuti` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_guru_pegawai` int(11) NOT NULL,
  `tanggal_mulai` date NOT NULL,
  `tanggal_selesai` date NOT NULL,
  `alasan` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_cuti`
--

LOCK TABLES `log_cuti` WRITE;
/*!40000 ALTER TABLE `log_cuti` DISABLE KEYS */;
INSERT INTO `log_cuti` VALUES (2,1,'2026-05-21','2026-05-23','voli','Pending');
/*!40000 ALTER TABLE `log_cuti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_izin`
--

DROP TABLE IF EXISTS `log_izin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_izin` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_guru_pegawai` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `jenis_izin` varchar(255) NOT NULL,
  `keterangan` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_izin`
--

LOCK TABLES `log_izin` WRITE;
/*!40000 ALTER TABLE `log_izin` DISABLE KEYS */;
INSERT INTO `log_izin` VALUES (1,2,'2026-05-20','Sakit','ww','Pending');
/*!40000 ALTER TABLE `log_izin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log_lembur`
--

DROP TABLE IF EXISTS `log_lembur`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_lembur` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_guru_pegawai` int(11) NOT NULL,
  `tanggal` date NOT NULL,
  `jam_mulai` time NOT NULL,
  `jam_selesai` time NOT NULL,
  `kegiatan` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_lembur`
--

LOCK TABLES `log_lembur` WRITE;
/*!40000 ALTER TABLE `log_lembur` DISABLE KEYS */;
INSERT INTO `log_lembur` VALUES (1,2,'2026-05-26','10:59:00','11:56:00','s','Pending');
/*!40000 ALTER TABLE `log_lembur` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mata_pelajaran`
--

LOCK TABLES `mata_pelajaran` WRITE;
/*!40000 ALTER TABLE `mata_pelajaran` DISABLE KEYS */;
INSERT INTO `mata_pelajaran` VALUES (3,'Bahasa Jawa'),(4,'Bahasa Inggris');
/*!40000 ALTER TABLE `mata_pelajaran` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `nilai_kinerja`
--

DROP TABLE IF EXISTS `nilai_kinerja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `nilai_kinerja` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_guru_pegawai` int(11) NOT NULL,
  `id_indikator` int(11) NOT NULL,
  `bulan` varchar(255) NOT NULL,
  `tahun` int(11) NOT NULL,
  `nilai` double NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nilai_kinerja`
--

LOCK TABLES `nilai_kinerja` WRITE;
/*!40000 ALTER TABLE `nilai_kinerja` DISABLE KEYS */;
INSERT INTO `nilai_kinerja` VALUES (1,1,1,'May',2026,1),(2,1,2,'May',2026,0),(3,1,3,'May',2026,0),(4,1,4,'May',2026,0),(5,1,5,'May',2026,0),(6,1,6,'May',2026,0),(7,1,7,'May',2026,0),(8,1,1,'May',2026,1),(9,1,2,'May',2026,1220),(10,1,3,'May',2026,0),(11,1,4,'May',2026,0),(12,1,5,'May',2026,0),(13,1,6,'May',2026,0),(14,1,7,'May',2026,0),(15,1,1,'May',2026,1),(16,1,2,'May',2026,10),(17,1,3,'May',2026,0),(18,1,4,'May',2026,0),(19,1,5,'May',2026,0),(20,1,6,'May',2026,0),(21,1,7,'May',2026,0),(22,1,1,'May',2026,1),(23,1,2,'May',2026,100),(24,1,3,'May',2026,0),(25,1,4,'May',2026,0),(26,1,5,'May',2026,0),(27,1,6,'May',2026,0),(28,1,7,'May',2026,0);
/*!40000 ALTER TABLE `nilai_kinerja` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `peminjaman`
--

LOCK TABLES `peminjaman` WRITE;
/*!40000 ALTER TABLE `peminjaman` DISABLE KEYS */;
INSERT INTO `peminjaman` VALUES (1,8,3,'2026-05-20','2026-05-21',NULL,'Dikembalikan',1),(2,8,3,'2026-05-20','2026-05-21',NULL,'Dipinjam',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `penerimaan`
--

LOCK TABLES `penerimaan` WRITE;
/*!40000 ALTER TABLE `penerimaan` DISABLE KEYS */;
INSERT INTO `penerimaan` VALUES (2,'Pendapatan BOSREG','Bos',2000000,'2026-05-15','Gua','YA');
/*!40000 ALTER TABLE `penerimaan` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `riwayat_aset`
--

DROP TABLE IF EXISTS `riwayat_aset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `riwayat_aset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_aset` int(11) NOT NULL,
  `aktivitas` varchar(100) NOT NULL,
  `keterangan` text,
  `pengguna` varchar(100) NOT NULL DEFAULT 'Petugas',
  `tanggal` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `id_aset` (`id_aset`),
  CONSTRAINT `riwayat_aset_ibfk_1` FOREIGN KEY (`id_aset`) REFERENCES `inventaris_aset` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `riwayat_aset`
--

LOCK TABLES `riwayat_aset` WRITE;
/*!40000 ALTER TABLE `riwayat_aset` DISABLE KEYS */;
INSERT INTO `riwayat_aset` VALUES (2,2,'Pengadaan Baru','Pinjam','Petugas','2026-05-20 07:25:39');
/*!40000 ALTER TABLE `riwayat_aset` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `semester`
--

LOCK TABLES `semester` WRITE;
/*!40000 ALTER TABLE `semester` DISABLE KEYS */;
INSERT INTO `semester` VALUES (2,8,'Penilaian Akhir Tahun (PAT)','Semester 1');
/*!40000 ALTER TABLE `semester` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setting_indikator`
--

DROP TABLE IF EXISTS `setting_indikator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `setting_indikator` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_indikator` varchar(255) NOT NULL,
  `bobot` int(11) NOT NULL,
  `keterangan` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setting_indikator`
--

LOCK TABLES `setting_indikator` WRITE;
/*!40000 ALTER TABLE `setting_indikator` DISABLE KEYS */;
INSERT INTO `setting_indikator` VALUES (1,'Kehadiran',100,'fqf'),(2,'Kerajinan',100,'11'),(3,'Kedisiplinan',100,'22'),(4,'Prestasi',100,'12'),(5,'Kepemimpinan',100,'223'),(6,'Literasi Digital',100,'44'),(7,'Keterampilan',100,'123');
/*!40000 ALTER TABLE `setting_indikator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setting_kategori_aset`
--

DROP TABLE IF EXISTS `setting_kategori_aset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `setting_kategori_aset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_kategori` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setting_kategori_aset`
--

LOCK TABLES `setting_kategori_aset` WRITE;
/*!40000 ALTER TABLE `setting_kategori_aset` DISABLE KEYS */;
INSERT INTO `setting_kategori_aset` VALUES (1,'Elektronik'),(2,'Furniture');
/*!40000 ALTER TABLE `setting_kategori_aset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setting_lokasi_aset`
--

DROP TABLE IF EXISTS `setting_lokasi_aset`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `setting_lokasi_aset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_lokasi` varchar(255) DEFAULT NULL,
  `latitude` varchar(100) DEFAULT NULL,
  `longitude` varchar(100) DEFAULT NULL,
  `radius` int(11) DEFAULT NULL,
  `jam_masuk` time DEFAULT NULL,
  `jam_selesai` time DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setting_lokasi_aset`
--

LOCK TABLES `setting_lokasi_aset` WRITE;
/*!40000 ALTER TABLE `setting_lokasi_aset` DISABLE KEYS */;
INSERT INTO `setting_lokasi_aset` VALUES (5,'garut','-6.209639584635776','106.83517456054689',-4,'15:12:00','14:13:00');
/*!40000 ALTER TABLE `setting_lokasi_aset` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `setting_lokasi_inventaris`
--

DROP TABLE IF EXISTS `setting_lokasi_inventaris`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `setting_lokasi_inventaris` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nama_lokasi` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `setting_lokasi_inventaris`
--

LOCK TABLES `setting_lokasi_inventaris` WRITE;
/*!40000 ALTER TABLE `setting_lokasi_inventaris` DISABLE KEYS */;
INSERT INTO `setting_lokasi_inventaris` VALUES (1,'Ruangan Kelas 1'),(3,'Ruangan Kelas 2');
/*!40000 ALTER TABLE `setting_lokasi_inventaris` ENABLE KEYS */;
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
  `status_aktif` varchar(20) DEFAULT NULL,
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
  `kelas` int(11) DEFAULT NULL,
  `jurusan` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nis` (`nis`),
  KEY `idx_siswa__jurusan` (`jurusan`),
  KEY `idx_siswa__kelas` (`kelas`),
  CONSTRAINT `fk_siswa__jurusan` FOREIGN KEY (`jurusan`) REFERENCES `jurusan` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_siswa__kelas` FOREIGN KEY (`kelas`) REFERENCES `kelas` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `siswa`
--

LOCK TABLES `siswa` WRITE;
/*!40000 ALTER TABLE `siswa` DISABLE KEYS */;
INSERT INTO `siswa` VALUES (8,'1234555','1234555','herz im fine????','garot','2026-05-16 00:00:00','L','JL Garot Reng','Islam','O','Aktif','2025','2027','SMP 1','08123456789','gsff','','','','','',2,2),(13,'123456711','123455511','Minji','Semarang','2026-05-19 00:00:00','L','Mijen','ISlam','O','Aktif','2025','2025','SMP 1','005555','Kai','Pegawai','','Bu Ani','IRT','',1,2),(14,'123456788','888888','cocoopamm88','Semarang','2026-05-26 00:00:00','L','Mijen','Islam','O','Aktif','2024/2025','2025','Stm','7467','67547','6575765','67657','657567','657567','567657',2,4);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tabungan`
--

LOCK TABLES `tabungan` WRITE;
/*!40000 ALTER TABLE `tabungan` DISABLE KEYS */;
INSERT INTO `tabungan` VALUES (1,8,'2026-05-25 14:21:26','Penarikan',111,'fwf'),(2,8,'2026-05-25 14:21:58','Setoran',111,'asd');
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tahun_ajaran`
--

LOCK TABLES `tahun_ajaran` WRITE;
/*!40000 ALTER TABLE `tahun_ajaran` DISABLE KEYS */;
INSERT INTO `tahun_ajaran` VALUES (8,'2025','2025/2026',1),(9,'2022','2022/2023',1),(10,'2045','2044/2045',0);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transaksi_belanja`
--

LOCK TABLES `transaksi_belanja` WRITE;
/*!40000 ALTER TABLE `transaksi_belanja` DISABLE KEYS */;
INSERT INTO `transaksi_belanja` VALUES (1,'Beban Lain-Lain','BOS','Gua','Kas','2026-05-15 00:00:00','Gua',20000,'Ya');
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

-- Dump completed on 2026-05-26  8:56:48
