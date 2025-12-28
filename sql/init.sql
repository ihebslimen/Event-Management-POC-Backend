-- MySQL dump 10.13  Distrib 8.0.43, for Linux (x86_64)
--
-- Host: localhost    Database: gtc_event_db
-- ------------------------------------------------------
-- Server version	8.0.43-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `event` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `subtitle` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `description` text COLLATE utf8mb4_general_ci,
  `location_name` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `city` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `state` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `country` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `latitude` float DEFAULT NULL,
  `longitude` float DEFAULT NULL,
  `is_online` tinyint(1) DEFAULT '0',
  `online_link` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `start_datetime` datetime NOT NULL,
  `end_datetime` datetime NOT NULL,
  `timezone` varchar(50) COLLATE utf8mb4_general_ci DEFAULT 'UTC',
  `recurrence_rule` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `registration_required` tinyint(1) DEFAULT '0',
  `max_attendees` int DEFAULT NULL,
  `tickets_available` int DEFAULT NULL,
  `ticket_price` float DEFAULT NULL,
  `ticket_currency` varchar(10) COLLATE utf8mb4_general_ci DEFAULT 'USD',
  `ticket_types` json DEFAULT NULL,
  `organizer` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `organizer_contact` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `co_hosts` json DEFAULT NULL,
  `banner_image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `thumbnail_image` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `tags` json DEFAULT NULL,
  `category` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `website_url` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `social_links` json DEFAULT NULL,
  `attendees_count` int DEFAULT '0',
  `views_count` int DEFAULT '0',
  `likes_count` int DEFAULT '0',
  `shares_count` int DEFAULT '0',
  `rating` float DEFAULT '0',
  `is_public` tinyint(1) DEFAULT '1',
  `is_featured` tinyint(1) DEFAULT '0',
  `status` varchar(50) COLLATE utf8mb4_general_ci DEFAULT 'draft',
  `access_code` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,'AI & Cybersecurity Summit 2025','Exploring the Future of Secure AI Systems','A two-day international conference bringing together AI researchers, cybersecurity experts, and industry leaders to discuss advances and challenges in secure machine learning.','Tech Innovation Center','123 Innovation Ave','San Francisco','California','USA',37.7749,-122.419,0,NULL,'2025-12-05 09:00:00','2025-12-06 18:00:00','America/Los_Angeles','FREQ=YEARLY;INTERVAL=1',1,500,300,199.99,'USD','{\"VIP\": 399.99, \"Student\": 99.99, \"Standard\": 199.99}','TechWorld Association','events@techworld.org','[\"OpenAI Research\", \"CyberTrust Labs\"]','https://example.com/images/ai_summit_banner.jpg','https://example.com/images/ai_summit_thumb.jpg','[\"AI\", \"Cybersecurity\", \"Conference\", \"Innovation\"]','Conference','https://aisummit2025.techworld.org','{\"twitter\": \"https://twitter.com/aisummit2025\", \"facebook\": \"https://facebook.com/aisummit2025\", \"linkedin\": \"https://linkedin.com/company/aisummit2025\"}',0,0,0,0,0,1,1,'published',NULL);
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `role` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'admin','pbkdf2:sha256:1000000$N9nW12zwrrlyx5A2$cafbef536171bc37d9608c0076c15d6fc47aa4812ed53f152bda4155f5c6bbbd','admin'),(2,'user','pbkdf2:sha256:1000000$oG1yY9gyLQf1NlCi$7682dd7e25633a73f2563eb2021592a6beb5848ac61299a0072115cfac3a9319','user');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password_hash` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `role` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','pbkdf2:sha256:1000000$N9nW12zwrrlyx5A2$cafbef536171bc37d9608c0076c15d6fc47aa4812ed53f152bda4155f5c6bbbd','admin'),(2,'user','pbkdf2:sha256:1000000$oG1yY9gyLQf1NlCi$7682dd7e25633a73f2563eb2021592a6beb5848ac61299a0072115cfac3a9319','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-23 10:35:48
