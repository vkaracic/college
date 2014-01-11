-- MySQL dump 10.13  Distrib 5.5.33, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: robot
-- ------------------------------------------------------
-- Server version	5.5.33-0+wheezy1

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
-- Table structure for table `cvor`
--

DROP TABLE IF EXISTS `cvor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cvor` (
  `cvorID` int(11) NOT NULL AUTO_INCREMENT,
  `cvorIme` varchar(255) NOT NULL,
  `tezina` int(11) DEFAULT NULL,
  `vezaID` int(11) DEFAULT NULL,
  `izracunato` tinyint(4) NOT NULL,
  PRIMARY KEY (`cvorID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cvor`
--

LOCK TABLES `cvor` WRITE;
/*!40000 ALTER TABLE `cvor` DISABLE KEYS */;
INSERT INTO `cvor` VALUES (1,'a',NULL,NULL,0),(2,'b',0,NULL,1),(3,'c',1,2,1),(4,'d',2,3,1);
/*!40000 ALTER TABLE `cvor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `veza`
--

DROP TABLE IF EXISTS `veza`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `veza` (
  `vezaID` int(11) NOT NULL AUTO_INCREMENT,
  `izCvorID` int(11) NOT NULL,
  `vezaIme` varchar(255) DEFAULT NULL,
  `doCvorID` int(11) NOT NULL,
  `tezina` int(11) NOT NULL,
  PRIMARY KEY (`vezaID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `veza`
--

LOCK TABLES `veza` WRITE;
/*!40000 ALTER TABLE `veza` DISABLE KEYS */;
INSERT INTO `veza` VALUES (1,1,'ima',2,1),(2,2,'sadrzi',3,1),(3,3,'krece se',4,1);
/*!40000 ALTER TABLE `veza` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'robot'
--
/*!50003 DROP PROCEDURE IF EXISTS `dijkstra` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `dijkstra`(pIzCvor varchar(255), pDoCvor varchar(255))
begin

    declare vIzCvorID, vDoCvorID, vCvorID, vTezina, vVezaID int;
    declare vIzCvor, vDoCvor, vVezaIme varchar(255);

    update cvor set
    vezaID = null,
    tezina = null,
    izracunato = 0;

    set vIzCvorID = (select cvorID from cvor where pIzCvor = cvorIme);
    if vIzCvorID is null then
        select concat('izCvor ime ', pIzCvor, ' nije nadjen.');

    else
        begin
        set vCvorID = vIzCvorID;
        set vDoCvorID = (select cvorID from cvor where cvorIme = pDoCvor);
        if vDoCvorID is null then
        select concat('Izvorisni cvor ', pDoCvor, 'nije nadjen.');
        else 
        begin
            update cvor set tezina = 0 where cvorID = vIzCvorID;

            while vCvorID is not null do
                begin
                    update
                    cvor as src
                    join veza as v on v.IzCvorID = src.cvorID
                    join cvor dest on dest.CvorID = v.DoCvorID

                    set dest.tezina = 
                    case
                        when dest.tezina is null then src.tezina + v.tezina
                        when src.tezina + v.tezina < dest.tezina then src.tezina + v.tezina
                        else dest.tezina
                    end,

                    dest.vezaID = v.vezaID
                    where
                    src.cvorID = vCvorID
                    and(dest.tezina is null or src.tezina + v.tezina < dest.tezina)
                    and dest.izracunato = 0;

                    update cvor set izracunato = 1 where cvorID = vCvorID;

                    set vCvorID = (select cvorID from cvor
                    where izracunato = 0 and tezina is not null
                    order by tezina limit 1);
                end;
            end while;
        end;
    end if;
    end;
    end if; 
    if exists( select 1 from cvor where cvorID = vDoCvorID and tezina is null) then 
    select concat('Cvor ', vCvorID, ' promasen.');
    else

    begin
    drop temporary table if exists map;

    create temporary table map(
    redID int primary key auto_increment,
    izCvorIme varchar(255),
    vezaIme varchar(255),
    doCvorIme varchar(255),
    tezina int) ENGINE=MEMORY;

    while vIzCvorID <> vDoCvorID do
    begin
    select
    src.CvorIme, dest.CvorIme, dest.Tezina, dest.vezaID, v.vezaIme
    into vIzCvor, vDoCvor, vTezina, vVezaID, vVezaIme
    from 
    cvor as dest
    join veza as v on v.vezaID = dest.vezaID
    join cvor as src on src.cvorID = v.IzCvorID
    where dest.cvorID = vDoCvorID;

    


    insert into map(izCvorIme, vezaIme, doCvorIme, tezina) values (vIzCvor, vVezaIme, vDoCvor, vTezina);

    set vDoCvorID = (select izCvorID from veza where vezaID = vVezaID);
    end;
    end while;

    select izCvorIme, vezaIme, DoCvorIme, tezina from map order by redID desc;
    drop temporary table map;
    end;
    end if;
end ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `dodajVezu` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8 */ ;
/*!50003 SET character_set_results = utf8 */ ;
/*!50003 SET collation_connection  = utf8_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = '' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `dodajVezu`(pIzCvor varchar(255), pVezaIme varchar(255), pDoCvor varchar(255), pTezina int)
begin

declare vIzCvor, vDoCvor, vVezaID int;

set vIzCvor = (select cvorID from cvor where cvorIme = pIzCvor);
if vIzCvor is null then
begin
insert into cvor (cvorIme, izracunato) values (pIzCvor, 0);
set vIzCvor = last_insert_id();
end;
end if;

set vDoCvor = (select cvorID from cvor where cvorIme = pDoCvor);
if vDoCvor is null then
begin
insert into cvor(cvorIme, izracunato) values (pDoCvor, 0);
set vDoCvor = last_insert_id();
end;
end if;

set vVezaID = (select vezaID from veza where izCvorID = vIzCvor and doCvorID = vDoCvor);
if vVezaID is null then
insert into veza(vezaIme, izCvorID, doCvorID, tezina) values(pVezaIme, vIzCvor, vDoCvor, pTezina);
else
update veza set tezina = pTezina
where izCvorID = vIzCvor and doCvorID = vDoCvor;
end if;

end ;;
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

-- Dump completed on 2014-01-11 14:18:13
