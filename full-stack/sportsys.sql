-- MySQL dump 10.13  Distrib 8.0.28, for macos11 (x86_64)
--
-- Host: localhost    Database: sportsys
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(30) DEFAULT NULL,
  `hashed_password` varchar(128) DEFAULT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  `phone_number` int DEFAULT NULL,
  `is_member` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name` (`user_name`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_number` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (2,'dave','$2b$12$hbsrCvocq2hr3dnwN4K8OOPcsIQ/e.wyCzsR/cIrC5a.bqttLQoNe','dave1','Abboud','david.abboud@hotmail.com',71779051,0),(3,'tamer3','$2b$12$pXtWMkMHelP54WS2NUQvR.Mi5Qj037jqhMEq1LjObQ.zHUXsL/5P2','Tamer','chalita','tamer.boutros@hotmail.com',81333333,0),(6,'carloseid','$2b$12$tXb5nuxBJa7nhmtBKelfze43TDlrit11TFRtjSQ2Z2D3YHAVchJDW','Carlos','Eid','carloseid@gmail.com',71777222,0),(7,'yara','$2b$12$D17CZmHiyf.bWAdyF3eZkuEMZO1tqHZPwwXcHVWpmB9WrN4GxxW/S','Yara','Issa El Khoury','yara@gmail.com',71888222,0),(8,'tatiana','$2b$12$U29Jq3QMvhqJd1Co.Ed2IORmZzNvjEqFnn8rs6Jifn4pNgLJQC25e','Tatiana','Abdallah','tatianabdallah@gmail.com',81888222,0),(52,'dijemail','$2b$12$mUihxuPaWf40SBxhmjKaLuzK/XypVQMJouIan5JT6/EFDNXqzZJ1K','dasd','sfdfsdg','ryan.alam001@gmail.com',12344109,0),(53,'jerome','$2b$12$1m3Ql5.pA4Fd2YyWqfUoVObImSBvPfPt007odS4bYvqrS5cEf8y7G','jafasf','jafsj','adafjl@mfa.co',12408,0),(54,'heap','$2b$12$4BquOXVZF7gZ1bIp1ee82eLHRbd852nCVmZ.Al4g2CD4nqw6PdAry','hadsap','asdaf','adsai@mf.ac',124309,0),(55,'macbook','$2b$12$E2P2qX9fNCrwBY4hpGbSA.3XRzhwkcvq6qrsUYE7vxoRTj9YPSNFW','asfoq','asfafj','davsj@mga.co',913408,0),(56,'adj','$2b$12$IsK.S9ZtXTlCu.IBGav/P.nb82ulAPtHxfqRUyrs5Pq1XI5Y3zHi2','asdj','fsk','davn19@mail.co',123,0),(57,'datt','$2b$12$lPKbMB.yPRPVGtbvJWXD/.qHCgOFKoxMl.HEC9x1KFsbenkpah1QG','dafao','ofa','fasd@ma.co',123914,0),(58,'asf','$2b$12$7wNA5Vi984q3v1Zwt7Bx/Ozhry1gRKpGZptNiEPmdqdodEF7CW686','asdjoq','oifasja','faoisfj@mai.co',13248,0),(59,'faf','$2b$12$Z158nWNjsGWHM5F9JcGfb.r3./A3DvHKj.inhafTI9MIbf0wWEny2','faio','jfao','1foai2@ma.co',12938,0);
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `events`
--

DROP TABLE IF EXISTS `events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `events` (
  `id` int NOT NULL AUTO_INCREMENT,
  `reservation_id` int DEFAULT NULL,
  `seats_left` int DEFAULT NULL,
  `date` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `reservation_id` (`reservation_id`),
  CONSTRAINT `events_ibfk_1` FOREIGN KEY (`reservation_id`) REFERENCES `reservations` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `events`
--

LOCK TABLES `events` WRITE;
/*!40000 ALTER TABLE `events` DISABLE KEYS */;
INSERT INTO `events` VALUES (0,34,298,'2022-04-28T20:00'),(1,35,49,'2022-04-29T18:00'),(2,27,19,'2022-05-01T18:00'),(3,28,39,'2022-05-09T18:00'),(4,29,15,'2022-05-12T18:00');
/*!40000 ALTER TABLE `events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fields`
--

DROP TABLE IF EXISTS `fields`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fields` (
  `id` int NOT NULL AUTO_INCREMENT,
  `type` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fields`
--

LOCK TABLES `fields` WRITE;
/*!40000 ALTER TABLE `fields` DISABLE KEYS */;
INSERT INTO `fields` VALUES (1,'basketball'),(2,'tennis'),(3,'boxing'),(4,'volleyball'),(5,'football');
/*!40000 ALTER TABLE `fields` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservations`
--

DROP TABLE IF EXISTS `reservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `date` datetime DEFAULT NULL,
  `type` tinyint(1) NOT NULL,
  `user_id` int DEFAULT NULL,
  `field_id` int DEFAULT NULL,
  `event_id` int DEFAULT NULL,
  `reservation_time` varchar(32) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `reservations_ibfk_1` (`event_id`),
  KEY `reservations_ibfk_3` (`field_id`),
  CONSTRAINT `reservations_ibfk_1` FOREIGN KEY (`event_id`) REFERENCES `events` (`id`),
  CONSTRAINT `reservations_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `reservations_ibfk_3` FOREIGN KEY (`field_id`) REFERENCES `fields` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservations`
--

LOCK TABLES `reservations` WRITE;
/*!40000 ALTER TABLE `reservations` DISABLE KEYS */;
INSERT INTO `reservations` VALUES (27,'2022-04-21 18:46:14',1,3,2,NULL,'2022-04-23T18:00:00.000Z'),(28,'2022-04-21 18:47:02',1,2,3,NULL,'2022-04-23T19:00:00.000Z'),(29,'2022-04-21 18:51:44',1,2,3,NULL,'2022-04-23T20:00:00.000Z'),(34,'2022-05-20 18:00:00',0,NULL,3,0,'2022-04-28 20:00:00'),(35,'2022-05-25 18:00:00',0,NULL,4,1,'2022-04-29 18:00:00'),(55,'2022-04-21 20:30:26',1,2,5,NULL,'2022-04-21T21:30'),(57,'2022-04-21 21:11:44',0,NULL,1,2,'2022-05-01 18:00:00'),(58,'2022-04-21 21:07:44',0,NULL,2,3,'2022-05-09 18:00:00'),(59,'2022-04-21 21:07:44',0,NULL,3,4,'2022-05-21 21:07:44'),(60,'2022-04-21 21:17:14',0,2,NULL,0,'2022-04-28 20:00:00'),(61,'2022-04-21 21:18:51',0,2,NULL,2,'2022-05-01 18:00:00'),(62,'2022-04-21 21:19:49',0,3,NULL,3,'2022-05-09 18:00:00'),(63,'2022-04-21 21:47:07',1,2,1,NULL,'2022-04-21T21:48'),(64,'2022-04-21 21:48:54',1,2,3,NULL,'2022-04-21T21:50'),(65,'2022-04-23 18:41:27',1,2,2,NULL,'2022-04-23T18:44'),(66,'2022-04-23 18:42:37',1,2,4,NULL,'2022-04-23T18:44'),(67,'2022-04-23 19:43:02',1,2,3,NULL,'2022-04-23T07:43'),(70,'2022-04-23 20:06:39',1,2,2,NULL,'2022-01-02T01:00'),(71,'2022-04-23 20:08:00',1,2,2,NULL,'2022-03-04T13:00'),(72,'2022-04-23 20:08:56',1,2,2,NULL,'2022-04-12T13:00'),(73,'2022-04-23 20:09:02',1,2,3,NULL,'2022-04-12T13:00'),(75,'2022-04-25 19:56:59',1,2,1,NULL,'2022-02-02T01:00'),(76,'2022-04-26 19:51:33',0,2,NULL,1,'2022-04-29 18:00:00'),(77,'2022-04-26 19:51:53',1,2,3,NULL,'2022-02-03T10:00');
/*!40000 ALTER TABLE `reservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(30) DEFAULT NULL,
  `hashed_password` varchar(128) DEFAULT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_name` (`user_name`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-04-27  2:25:08
