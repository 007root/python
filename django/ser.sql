-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: server_list
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_0e939a4f` (`group_id`),
  KEY `auth_group_permissions_8373b171` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_417f1b1c` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add permission',2,'add_permission'),(5,'Can change permission',2,'change_permission'),(6,'Can delete permission',2,'delete_permission'),(7,'Can add group',3,'add_group'),(8,'Can change group',3,'change_group'),(9,'Can delete group',3,'delete_group'),(10,'Can add user',4,'add_user'),(11,'Can change user',4,'change_user'),(12,'Can delete user',4,'delete_user'),(13,'Can add content type',5,'add_contenttype'),(14,'Can change content type',5,'change_contenttype'),(15,'Can delete content type',5,'delete_contenttype'),(16,'Can add session',6,'add_session'),(17,'Can change session',6,'change_session'),(18,'Can delete session',6,'delete_session'),(19,'Can add server list',7,'add_serverlist'),(20,'Can change server list',7,'change_serverlist'),(21,'Can delete server list',7,'delete_serverlist'),(22,'Can add user',8,'add_user'),(23,'Can change user',8,'change_user'),(24,'Can delete user',8,'delete_user'),(25,'Can add server view',9,'add_serverview'),(26,'Can change server view',9,'change_serverview'),(27,'Can delete server view',9,'delete_serverview');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$15000$R97Bvb8sVltS$f6JuTWQGRUKG6CnA7HfhebIgFHX7CScKaIGFt3i0iX4=','2017-02-04 08:39:57',1,'zhishuai','','','798399268@qq.com',1,1,'2017-02-04 08:39:49');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_e8701ad4` (`user_id`),
  KEY `auth_user_groups_0e939a4f` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_e8701ad4` (`user_id`),
  KEY `auth_user_user_permissions_8373b171` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_417f1b1c` (`content_type_id`),
  KEY `django_admin_log_e8701ad4` (`user_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_45f3b1d93ec8c61c_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'log entry','admin','logentry'),(2,'permission','auth','permission'),(3,'group','auth','group'),(4,'user','auth','user'),(5,'content type','contenttypes','contenttype'),(6,'session','sessions','session'),(7,'server list','server_manage','serverlist'),(8,'user','server_manage','user'),(9,'server view','server_view','serverview');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=29 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-02-04 02:45:17'),(2,'auth','0001_initial','2017-02-04 02:45:17'),(3,'admin','0001_initial','2017-02-04 02:45:17'),(4,'server_manage','0001_initial','2017-02-04 02:45:17'),(5,'server_manage','0002_serverlist_serverid','2017-02-04 02:45:17'),(6,'server_manage','0003_user','2017-02-04 02:45:17'),(7,'sessions','0001_initial','2017-02-04 02:45:17'),(8,'server_view','0001_initial','2017-02-15 23:26:17'),(9,'server_view','0002_auto_20170208_0103','2017-02-15 23:26:17'),(10,'server_view','0003_delete_serverview','2017-02-15 23:26:17'),(11,'server_view','0004_serverview','2017-02-15 23:26:17'),(12,'server_view','0005_auto_20170220_0125','2017-02-22 01:23:19'),(13,'server_view','0006_auto_20170220_0139','2017-02-22 01:25:42'),(14,'server_view','0007_delete_serverview','2017-02-22 01:25:42'),(15,'server_view','0008_serverview','2017-02-22 01:25:42'),(16,'server_view','0009_delete_serverview','2017-02-22 01:25:42'),(17,'server_view','0010_serverviews','2017-02-22 01:25:42'),(18,'server_view','0011_auto_20170220_0151','2017-02-22 01:25:42'),(19,'server_view','0012_delete_serverview','2017-02-22 01:25:42'),(20,'server_view','0013_serverview','2017-02-22 01:25:42'),(21,'server_view','0014_auto_20170220_0203','2017-02-22 01:25:42'),(22,'server_view','0015_serverview_redisuse','2017-02-22 01:25:42'),(23,'server_view','0016_auto_20170220_0304','2017-02-22 01:25:42'),(24,'server_view','0017_delete_serverview','2017-02-22 01:25:42'),(25,'server_view','0018_serverview','2017-02-22 01:25:42'),(26,'server_view','0019_delete_serverview','2017-02-22 01:25:42'),(27,'server_view','0020_serverview','2017-02-22 01:25:42'),(28,'server_view','0021_auto_20170222_0127','2017-02-22 01:28:13');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_de54fa62` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('pubo6qmsc3dj0ooj9d9s3sa5pfrilnpk','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-02-18 03:24:51'),('99946s310jqv2xa7k4xk88f25j4kxh34','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-02-22 23:37:18'),('cdmbk1pr6lk0rkd3nm42tfiegle18isg','NjhkMzRhODc4YmVjYWQwMzhkYTIxNjdkNGIzNmE1ZDViYjAwODQ0Yjp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfaGFzaCI6ImJhMTcyZGU2ZGEyMmYzMDhmYzJiMjQzODc1OWRiMTAxMGJlMmI5OWYiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2017-03-13 23:49:57'),('640sd2d9r4z2nflu0pyzdgveh1ed72yy','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-02-22 23:57:01'),('5lfgs5jlofz67zi6uxcql07mrx5zcyz8','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-02-23 00:02:20'),('fw7vibdgr01fp09upedwj49e5r75xqvw','MzRkYjZjNzk5MjJiZmVhNTI2NzA0MTYyMzQ4NWE4ZWUzYTlhMGU0ODp7fQ==','2017-02-23 00:04:13'),('dzm6qzra7ht8ibko59awdpvhbc0094hx','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-03-24 02:36:59'),('uftnglzagz440757jzzrs35cb86narca','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-03-07 01:29:26'),('jerf4rr4v5nlsgo3qtpd8zd90x54qj9k','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-03-08 01:32:55'),('uzkfbtvmcfw1fj44fyuitulem3l8wr6q','MzRkYjZjNzk5MjJiZmVhNTI2NzA0MTYyMzQ4NWE4ZWUzYTlhMGU0ODp7fQ==','2017-03-08 07:27:09'),('qywrn8y5cl3fjcv4lelxhzqpsyz928t3','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-03-13 03:06:13'),('p2n1nxfz7429mwxgsvs4viq1y87zo2hs','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-03-14 06:04:40'),('woeq2bsryunrbeuw8fxxjmv7jr79u8lc','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-03-17 09:31:08'),('a3xm2el48smcvnnl1a9pss3tmgk6532c','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-03-30 06:27:53'),('naeg3gbs69yg3p8eudkumtdjw5znz91p','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-04-05 15:29:09'),('np9gedwqa4f1xmtxxkqks80ocuysfflg','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-04-15 06:42:46'),('2potflbh2lgtrpvh66ekqo24mni3atw8','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-04-15 06:45:41'),('xxqco47duo5gm4m0vupy3x8ub5f70z2m','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-05-17 10:25:28'),('k2ujlbgzjh319oap62gr7nbd40v76v05','NWIyOTVjNzJlYjc5OGVlMWZkZjRiYmMzNmVlNThlNTEwNmMwZDA1ODp7ImlzX2xvZ2luIjp7InVzZXIiOiJhZG1pbiJ9fQ==','2017-07-26 05:52:12');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_manage_serverlist`
--

DROP TABLE IF EXISTS `server_manage_serverlist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_manage_serverlist` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `Address` varchar(50) NOT NULL,
  `CreateTime` datetime NOT NULL,
  `ServerId` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_manage_serverlist`
--

LOCK TABLES `server_manage_serverlist` WRITE;
/*!40000 ALTER TABLE `server_manage_serverlist` DISABLE KEYS */;
INSERT INTO `server_manage_serverlist` VALUES (1,'game01','192.168.1.2','2016-02-01 12:00:00','10001'),(2,'game02','192.168.1.3','2016-02-02 12:00:00','10002');
/*!40000 ALTER TABLE `server_manage_serverlist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_manage_user`
--

DROP TABLE IF EXISTS `server_manage_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_manage_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(6) NOT NULL,
  `password` varchar(15) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_manage_user`
--

LOCK TABLES `server_manage_user` WRITE;
/*!40000 ALTER TABLE `server_manage_user` DISABLE KEYS */;
INSERT INTO `server_manage_user` VALUES (2,'admin','admin');
/*!40000 ALTER TABLE `server_manage_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `server_view_serverview`
--

DROP TABLE IF EXISTS `server_view_serverview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `server_view_serverview` (
  `id` int(11) NOT NULL,
  `Address` varchar(50) NOT NULL,
  `Name` varchar(50) NOT NULL,
  `Date` date NOT NULL,
  `Disk` varchar(50) NOT NULL,
  `DiskUse` longtext NOT NULL,
  `Mem` varchar(50) NOT NULL,
  `MemUse` longtext NOT NULL,
  `RedisUse` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `server_view_serverview`
--

LOCK TABLES `server_view_serverview` WRITE;
/*!40000 ALTER TABLE `server_view_serverview` DISABLE KEYS */;
INSERT INTO `server_view_serverview` VALUES (1,'192.168.1.1','game01,game02,game03,game04,game05','2017-02-01','40','6.7,6.8,7.0,8.5,6.7,6.8,7.0,8.5,6.7,6.8,7.0,8.5','999','690.7,660.8,770.0,820.5,614.7,641.8,474.0,824.5,625.7,645.8,736.0,845.5','8.7,6.4,7.0,8.5,6.4,6.8,7.0,8.5,9.7,6.8,4.0,6.5'),(2,'192.168.1.2','game06,game07,game08,game09,game10','2017-02-01','20','2.7,6.8,7.0,5,6.7,6.8,9.0,8.5,6.7,6.8,7.0,8.5','299','234.7,634.842,732.0,557,645.743,653.8,936.0,843.5,667.7,636.8,735.0,826.5','6.2,6.8,4.0,8.5,6.7,4.8,7.0,7.5,6.7,9.8,7.0,5.5'),(3,'192.168.1.3','game11,game12,game13,game14,game15','2017-02-01','30','6.5,6.8,7.0,3.5,6.7,6.4,7.0,8.5,8.7,6.8,7.0,5.5','399','645.5,626.54,736.0,336.5,653.7,626.4,775.0,837.5,847.7,637.8,754.0,536.5','6.7,6.3,7.0,8.5,4.7,6.8,7.0,8.5,6.3,6.8,9.0,4.5'),(4,'192.168.1.4','game16,game17,game18,game19,game20','2017-02-01','40','6.3,6.8,2.0,8.5,6.7,6.8,5.0,8.2,6.7,4.8,7.0,3.5','499','623.3,646.8,274.0,836.5,636.7,653.8,553.0,825.2,664.7,436.8,736.0,543.5','6.7,6.3,7.0,8.5,4.7,6.8,7.0,4.5,6.3,6.8,9.0,5.7'),(5,'192.168.1.1','game21,game22,game23,game24,game25','2017-02-02','50','6.2,6.8,4.0,5.5,6.7,4.8,7.0,7.5,6.7,9.8,7.0,5.5','599','623.7,645.3,754.0,845.5,454.7,654.8,723.0,845.5,632.3,636.8,923.0,543.5','4.7,5.8,7.0,8.8,6.7,6.8,8.0,8.5,6.7,6.8,7.0,8.4'),(6,'192.168.1.2','game26,game27,game28,game29,game30','2017-02-02','60','6.4,6.8,4.0,8.6,6.7,8.8,7.0,8.5,5.7,6.8,4.0,8.5','699','634.2,623.8,443.0,825.5,654.7,435.8,734.0,764.5,665.7,934.8,763.0,553.35','2.7,6.8,7.0,5,6.7,6.8,9.0,8.5,6.7,6.8,7.0,8.5'),(7,'192.168.1.3','game31,game32,game33,game34,game35','2017-02-02','70','3.7,6.4,7.0,8.5,6.7,3.8,7.0,8.9,6.7,6.5,7.0,4.5','799','622.7,624.3,734.0,523,656.7,642.8,923.0,832.5,654.7,654.8,734.0,843.5','2.7,6.8,7.0,5,6.7,6.8,9.0,8.5,6.7,6.8,7.0,8.5'),(8,'192.168.1.4','game36,game37,game38,game39,game40','2017-02-02','80','6.7,6.3,7.0,8.2,4.7,6.8,7.0,8.5,6.3,6.8,9.0,5.5','899','643.2,623.8,443.0,854.5,635.7,462.8,724.0,754.5,632.7,953.8,754.0,554.5','4.7,5.8,7.0,8.8,6.7,6.8,8.0,6.5,6.7,6.8,7.0,8.6'),(9,'192.168.1.1','game41,game42,game43,game44,game45','2017-02-03','90','8.7,6.4,7.0,8.5,6.4,6.8,7.0,8.5,9.7,6.8,4.0,6.5','999','643.7,623.3,743.0,842.5,434.7,636.8,734.0,864.5,624.3,634.8,943.0,553.5','6.7,6.3,7.0,8.5,4.7,6.8,7.0,8.4,6.3,6.8,9.0,5.5'),(10,'192.168.1.2','game06,game07,game08,game09,game10','2017-02-03','40','4.7,5.8,7.0,8.3,6.7,6.8,8.0,8.5,6.7,6.8,7.0,8.8','999','425.7,563.8,736.0,834.8,634.7,665.8,876.0,856.5,685.7,654.8,734.0,834.8','8.7,6.4,7.0,8.5,6.4,6.8,7.0,8.5,9.7,6.8,4.0,6.5'),(11,'192.168.1.3','game11,game12,game13,game14,game15','2017-02-03','40','4.4,5.8,3.0,7.8,6.7,6.8,7.0,8.5,6.7,6.8,7.0,8.2','999','634.3,665.8,562.0,854.5,923.7,665.8,534.0,863.2,623.7,454.8,743.0,325.5','8.7,6.4,7.0,8.5,6.4,6.8,7.0,8.5,9.7,6.8,4.0,6.8'),(12,'192.168.1.4','game01,game02,game03,game04,game05','2017-02-03','20','2.7,5.8,8.0,5,6.7,6.8,7.0,8.5,6.7,4.8,7.0,8.6','299','643.3,746.8,462.0,832.5,663.7,674.8,536.0,834.2,643.7,465.8,735.0,323.5','8.7,6.4,7.0,8.5,6.4,6.8,7.0,8.5,9.7,6.8,4.0,6.5'),(13,'192.168.1.1','game41,game42,game43,game44,game45','2017-02-04','90','8.7,6.4,7.0,8.5,6.4,6.8,7.0,4.5,9.7,6.8,4.0,6.5','999','643.7,623.3,732.0,832.5,432.7,632.8,754.0,865.5,775.3,645.4,934.0,523.5','6.7,6.3,7.0,8.5,4.7,6.8,7.0,8.6,6.3,6.8,9.0,5.5'),(14,'192.168.1.2','game06,game07,game08,game09,game10','2017-02-04','40','4.7,5.8,7.0,6.8,6.7,6.8,8.0,8.5,6.7,6.8,7.0,8.8','999','454.7,523.8,743.0,865.8,654.7,612.8,543.0,812.5,623.7,665.6,754.0,832.8','2.7,5.5,8.0,5,6.7,6.5,7.0,8.5,6.7,4.8,7.0,8.6'),(15,'192.168.1.3','game11,game12,game13,game14,game15','2017-02-04','40','4.4,5.8,3.0,8.4,6.7,6.8,7.0,8.5,6.7,6.8,7.0,8.2','999','643.3,765.8,275.0,332.5,355.7,622.8,522.0,855.2,655.7,422.8,755.0,322.5','8.7,6.4,7.0,8.5,6.4,6.8,7.0,8.5,9.7,6.8,4.0,6.3'),(16,'192.168.1.4','game01,game02,game03,game04,game05','2017-02-04','20','2.7,5.8,8.0,5,6.7,6.8,7.0,8.5,6.7,4.8,7.0,8.6','299','634.3,676.8,452.0,866.5,623.7,653.8,734.0,854.2,635.7,443.8,755.0,323.5','2.7,5.8,8.0,5,6.7,6.8,6.0,8.5,6.4,4.8,7.0,8.6'),(17,'192.168.1.1','game41,game42,game43,game44,game45','2017-02-05','90','8.7,6.4,7.0,8.5,6.4,6.8,7.0,7.5,9.7,6.3,4.0,6.5','999','643.7,663.3,735.0,874.5,445.7,643.8,723.0,652.5,645.3,663.8,963.0,545.5','8.7,6.4,7.0,8.5,6.4,6.8,7.0,8.3,6.7,6.8,4.0,6.5'),(18,'192.168.1.2','game06,game07,game08,game09,game10','2017-02-05','40','4.7,5.8,7.0,8.5,6.7,6.8,8.0,8.5,6.7,6.8,7.0,8.8','999','465.7,554.8,734.0,836.8,463.7,663.7,824.0,834.5,654.7,654.86,754.0,834.8','6.7,6.3,7.0,8.5,4.7,6.8,7.0,8.5,6.3,6.8,5.0,5.9'),(19,'192.168.1.3','game11,game12,game13,game14,game15','2017-02-05','40','4.4,5.8,3.0,3.8,6.7,6.8,7.0,8.5,6.7,6.8,7.0,8.2','999','656.3,635.8,523.0,534.5,654.3,645.8,524.0,824.2,653.7,464.8,743.0,325.5','2.7,6.8,7.0,5,6.7,6.5,9.0,8.5,6.7,6.8,7.0,8.5'),(20,'192.168.1.4','game01,game02,game03,game04,game05','2017-02-05','20','2.7,5.8,8.0,5,6.4,6.8,7.0,5.5,6.7,4.8,9.0,8.6','299','627.6,626.8,256.0,338.5,655.7,635.8,525.0,845.2,665.7,425.8,735.0,623.5','6.7,6.8,7.0,8.5,6.7,6.8,7.0,8.5,6.4,6.8,7.0,4.5'),(21,'192.168.1.1','game41,game42,game43,game44,game45','2017-02-06','90','8.7,6.4,7.0,8.5,6.4,6.8,7.0,6.5,9.7,6.8,4.0,6.5','999','627.7,646.3,726.0,832.5,462.7,636.5,736.0,436.5,626.3,636.8,934.0,536.5','6.7,3.8,7.0,5.5,6.7,6.8,7.0,5.5,6.7,7.4,5.0,6.5'),(22,'192.168.1.2','game06,game07,game08,game09,game10','2017-02-06','40','4.7,5.8,7.0,8.8,8.7,6.8,8.0,8.5,6.7,6.8,7.0,8.8','999','446.7,536.8,726.0,864.8,646.7,663.3,842.0,836.5,646.7,626.8,736.0,836.8','4.7,5.8,7.0,8.7,6.7,6.8,8.0,8.5,5.7,6.8,7.0,8.8'),(23,'192.168.1.3','game11,game12,game13,game14,game15','2017-02-06','40','4.4,5.8,3.0,8.8,3.7,6.8,7.0,8.9,6.7,6.8,7.0,8.2','999','436.3,636.8,623.0,736.5,664.5,646.8,535.0,825.7,653.7,453.8,724.0,324.5','6.7,4.8,7.0,8.5,6.7,6.8,7.0,8.5,6.7,5.8,7.0,7.5'),(24,'192.168.1.4','game01,game02,game03,game04,game05','2017-02-06','20','2.7,5.8,8.0,5,6.7,6.4,7.0,8.5,6.7,4.8,7.0,8.6','299','623.3,624.8,225.0,825.5,663.7,624.8,563.0,824.2,624.7,454.8,752.0,324.5','6.7,6.8,7.0,8.5,6.7,6.8,7.0,8.5,6.7,6.8,7.0,8.5');
/*!40000 ALTER TABLE `server_view_serverview` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-07-12 17:10:28
