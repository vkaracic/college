-- MySQL dump 10.13  Distrib 5.5.35, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: istrazivac
-- ------------------------------------------------------
-- Server version	5.5.35-0+wheezy1

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
-- Table structure for table `polje`
--

DROP TABLE IF EXISTS `polje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `polje` (
  `poljeID` int(11) NOT NULL AUTO_INCREMENT,
  `xkoord` int(11) DEFAULT '0',
  `ykoord` int(11) DEFAULT '0',
  `tezina` int(11) DEFAULT '0',
  `d_tezina` int(11) DEFAULT '0',
  `t_smjer` int(11) DEFAULT '-90',
  PRIMARY KEY (`poljeID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `polje`
--

LOCK TABLES `polje` WRITE;
/*!40000 ALTER TABLE `polje` DISABLE KEYS */;
INSERT INTO `polje` VALUES (1,0,0,0,0,-90);
/*!40000 ALTER TABLE `polje` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stanje`
--

DROP TABLE IF EXISTS `stanje`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `stanje` (
  `vrijeme` int(11) NOT NULL AUTO_INCREMENT,
  `smjer` int(11) DEFAULT '0',
  `poljeID` int(11) NOT NULL,
  PRIMARY KEY (`vrijeme`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stanje`
--

LOCK TABLES `stanje` WRITE;
/*!40000 ALTER TABLE `stanje` DISABLE KEYS */;
INSERT INTO `stanje` VALUES (1,0,1);
/*!40000 ALTER TABLE `stanje` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'istrazivac'
--
/*!50003 DROP PROCEDURE IF EXISTS `init` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `init`()
BEGIN
DELETE FROM polje;
    DELETE FROM stanje;
    SET @t_x = 0;
    SET @t_y = 0;
    ALTER TABLE stanje AUTO_INCREMENT = 1;
    ALTER TABLE polje AUTO_INCREMENT = 1;
    INSERT INTO polje (xkoord, ykoord, tezina, d_tezina) VALUES (0, 0, 0, 0);
    INSERT INTO stanje (poljeID, smjer) VALUES (1, 0);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `povecaj_tezinu` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `povecaj_tezinu`(x INT, y INT)
BEGIN
    IF EXISTS (SELECT 1 FROM polje WHERE xkoord = x AND ykoord = y) THEN
        UPDATE polje
        SET tezina = tezina + 1
        WHERE xkoord = x AND ykoord = y;
    ELSE
        INSERT INTO polje (xkoord, ykoord, tezina) VALUES (x, y, 1);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-02-25 17:05:51
