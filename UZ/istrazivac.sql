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
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `polje`
--

LOCK TABLES `polje` WRITE;
/*!40000 ALTER TABLE `polje` DISABLE KEYS */;
INSERT INTO `polje` VALUES (1,0,0,3,1,270),(2,0,1,10002,9999,270),(3,1,0,5,1,180),(4,0,-1,9999,9999,180),(5,-1,0,9999,9999,270),(6,2,0,10001,9999,270),(7,1,-1,9999,9999,180),(8,1,1,8,1,270),(9,1,2,11,1,0),(10,2,1,6,1,270),(11,1,3,14,1,0),(12,2,2,10004,9999,270),(13,0,2,6,1,270),(14,1,4,10002,9999,0),(15,2,3,8,1,90),(16,0,3,9,1,270),(17,-1,3,10000,9999,270),(18,0,4,10000,9999,0),(19,-1,2,9999,9999,270),(20,3,3,10001,9999,0),(21,2,4,10000,9999,0),(22,3,1,9,1,180),(23,4,1,10000,9999,90),(24,3,0,4,1,180),(25,3,2,4,1,0),(26,3,-1,9999,9999,180),(27,4,0,9999,9999,90),(28,4,2,9999,9999,90);
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
INSERT INTO `stanje` VALUES (1,180,22);
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
    INSERT INTO polje (xkoord, ykoord, tezina, d_tezina) VALUES (0, 0, 0, 1);
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
        SET tezina = tezina + 2
        WHERE xkoord = x AND ykoord = y;
    ELSE
        INSERT INTO polje (xkoord, ykoord, tezina) VALUES (x, y, 2);
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `spremi_polje_ispred` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `spremi_polje_ispred`(smjer INT)
BEGIN
    DECLARE x, y INT DEFAULT 0;
    DECLARE n_tezina INT;
    CASE smjer
        WHEN 0 THEN 
            SET x = @t_x;
            SET y = @t_y + 1;
        
        WHEN 90 THEN 
            SET x = @t_x + 1;
            SET y = @t_y;
        
        WHEN 180 THEN 
            SET x = @t_x;
            SET y = @t_y - 1;
        
        WHEN 270 THEN 
            SET x = @t_x - 1;
            SET y = @t_y;
        
        ELSE 
            SET x = @t_x;
            SET y = @t_y;
        
    END CASE;

    SET @pi_x = x;
    SET @pi_y = y;

    IF ((SELECT COUNT(*) FROM polje WHERE xkoord = x AND ykoord = y) > 0) THEN 
        UPDATE polje 
        SET tezina = tezina + 1
        WHERE xkoord = x AND ykoord = y;
    ELSE
        BEGIN
        IF @koncept = 'zid' THEN SET n_tezina = 9999;
        ELSE SET n_tezina = 1;
        END IF;
        INSERT INTO polje (xkoord, ykoord, tezina, d_tezina) VALUES (x, y, n_tezina, n_tezina);
        END;
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

-- Dump completed on 2014-03-05 22:31:44
