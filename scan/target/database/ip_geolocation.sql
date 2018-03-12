# Host: localhost  (Version 5.7.9-log)
# Date: 2017-09-12 20:37:50
# Generator: MySQL-Front 6.0  (Build 1.124)

create database ip_geolocation;
use ip_geolocation;

#
# Structure for table "aiwen_data"
#

DROP TABLE IF EXISTS `aiwen_data`;
CREATE TABLE `aiwen_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_from` int(10) unsigned NOT NULL,
  `ip_to` int(10) unsigned NOT NULL,
  `continent_name` varchar(16) DEFAULT NULL,
  `country_code` varchar(16) DEFAULT NULL,
  `country_name` varchar(50) DEFAULT NULL,
  `region_name` varchar(128) DEFAULT NULL,
  `city_name` varchar(128) DEFAULT NULL,
  `district_name` varchar(128) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `isp_name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ip_from_index` (`ip_from`),
  KEY `ip_to_index` (`ip_to`),
  KEY `ip_from_to_index` (`ip_from`,`ip_to`)
) ENGINE=InnoDB AUTO_INCREMENT=23448869 DEFAULT CHARSET=utf8;

#
# Structure for table "chunzhen_data"
#

DROP TABLE IF EXISTS `chunzhen_data`;
CREATE TABLE `chunzhen_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_from` int(10) unsigned NOT NULL,
  `ip_to` int(10) unsigned NOT NULL,
  `country_name` varchar(64) DEFAULT NULL,
  `region_name` varchar(128) DEFAULT NULL,
  `city_name` varchar(128) DEFAULT NULL,
  `district_name` varchar(128) DEFAULT NULL,
  `isp_name` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ip_from_index` (`ip_from`),
  KEY `ip_to_index` (`ip_to`),
  KEY `ip_from_to_index` (`ip_from`,`ip_to`)
) ENGINE=InnoDB AUTO_INCREMENT=447556 DEFAULT CHARSET=utf8;

#
# Structure for table "combine_data"
#

DROP TABLE IF EXISTS `combine_data`;
CREATE TABLE `combine_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_from` int(10) unsigned NOT NULL,
  `ip_to` int(10) unsigned NOT NULL,
  `country_code` varchar(4) DEFAULT NULL,
  `country_name` varchar(128) DEFAULT NULL,
  `region_name` varchar(256) DEFAULT NULL,
  `city_name` varchar(256) DEFAULT NULL,
  `district_name` varchar(256) DEFAULT NULL,
  `isp_name` varchar(256) DEFAULT NULL,
  `domain_name` varchar(128) DEFAULT NULL,
  `info_source` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ip_from_index` (`ip_from`),
  KEY `ip_to_index` (`ip_to`),
  KEY `ip_from_to_index` (`ip_from`,`ip_to`)
) ENGINE=InnoDB AUTO_INCREMENT=20001 DEFAULT CHARSET=utf8;

#
# Structure for table "db_md5sum"
#

DROP TABLE IF EXISTS `db_md5sum`;
CREATE TABLE `db_md5sum` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `db_name` varchar(128) DEFAULT NULL,
  `md5sum` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Structure for table "ip_dns"
#

DROP TABLE IF EXISTS `ip_dns`;
CREATE TABLE `ip_dns` (
  `ip` int(10) unsigned NOT NULL,
  `dns_name` varchar(256) DEFAULT NULL,
  UNIQUE KEY `ip_UNIQUE` (`ip`),
  KEY `ip_dns_index` (`ip`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Structure for table "ip2location_data"
#

DROP TABLE IF EXISTS `ip2location_data`;
CREATE TABLE `ip2location_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_from` int(10) unsigned NOT NULL,
  `ip_to` int(10) unsigned NOT NULL,
  `country_code` varchar(2) DEFAULT NULL,
  `country_name` varchar(64) DEFAULT NULL,
  `region_name` varchar(128) DEFAULT NULL,
  `city_name` varchar(128) DEFAULT NULL,
  `isp_name` varchar(256) DEFAULT NULL,
  `domain_name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ip_from_index` (`ip_from`),
  KEY `ip_to_index` (`ip_to`),
  KEY `ip_from_to_index` (`ip_from`,`ip_to`)
) ENGINE=InnoDB AUTO_INCREMENT=12551471 DEFAULT CHARSET=utf8;

#
# Structure for table "ip2locationlite_data"
#

DROP TABLE IF EXISTS `ip2locationlite_data`;
CREATE TABLE `ip2locationlite_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_from` int(10) unsigned NOT NULL,
  `ip_to` int(10) unsigned NOT NULL,
  `country_code` varchar(2) DEFAULT NULL,
  `country_name` varchar(64) DEFAULT NULL,
  `region_name` varchar(128) DEFAULT NULL,
  `city_name` varchar(128) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `postal_code` varchar(30) DEFAULT NULL,
  `time_zone` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_from_UNIQUE` (`ip_from`),
  UNIQUE KEY `ip_to_UNIQUE` (`ip_to`),
  KEY `ip_from_index` (`ip_from`),
  KEY `ip_to_index` (`ip_to`),
  KEY `ip_from_to_index` (`ip_from`,`ip_to`)
) ENGINE=InnoDB AUTO_INCREMENT=3495087 DEFAULT CHARSET=utf8;

#
# Structure for table "ipipnet_data"
#

DROP TABLE IF EXISTS `ipipnet_data`;
CREATE TABLE `ipipnet_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_from` int(10) unsigned NOT NULL,
  `ip_to` int(10) unsigned NOT NULL,
  `country_name` varchar(50) DEFAULT NULL,
  `region_name` varchar(128) DEFAULT NULL,
  `city_name` varchar(128) DEFAULT NULL,
  `district_name` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ip_from_index` (`ip_from`),
  KEY `ip_to_index` (`ip_to`),
  KEY `ip_from_to_index` (`ip_from`,`ip_to`)
) ENGINE=InnoDB AUTO_INCREMENT=1061446 DEFAULT CHARSET=utf8;

#
# Structure for table "ipmarker_data"
#

DROP TABLE IF EXISTS `ipmarker_data`;
CREATE TABLE `ipmarker_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_from` int(10) unsigned NOT NULL,
  `ip_to` int(10) unsigned NOT NULL,
  `country_name` varchar(64) DEFAULT NULL,
  `region_name` varchar(128) DEFAULT NULL,
  `city_name` varchar(128) DEFAULT NULL,
  `isp_name` varchar(128) DEFAULT NULL,
  `time_zone` varchar(128) DEFAULT NULL,
  `postal_code` varchar(30) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `ip_from_index` (`ip_from`),
  KEY `ip_to_index` (`ip_to`),
  KEY `ip_from_to_index` (`ip_from`,`ip_to`)
) ENGINE=InnoDB AUTO_INCREMENT=6383163 DEFAULT CHARSET=utf8;

#
# Structure for table "maxmind_data"
#

DROP TABLE IF EXISTS `maxmind_data`;
CREATE TABLE `maxmind_data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ip_from` int(10) unsigned NOT NULL,
  `ip_to` int(10) unsigned NOT NULL,
  `continent_code` varchar(2) DEFAULT NULL,
  `continent_name` varchar(32) DEFAULT NULL,
  `country_code` varchar(2) DEFAULT NULL,
  `country_name` varchar(64) DEFAULT NULL,
  `region_code` varchar(3) DEFAULT NULL,
  `region_name` varchar(128) DEFAULT NULL,
  `region_2_code` varchar(3) DEFAULT NULL,
  `region_2_name` varchar(128) DEFAULT NULL,
  `city_name` varchar(128) DEFAULT NULL,
  `time_zone` varchar(128) DEFAULT NULL,
  `postal_code` varchar(30) DEFAULT NULL,
  `latitude` double DEFAULT NULL,
  `longitude` double DEFAULT NULL,
  `accuracy_radius` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ip_from_UNIQUE` (`ip_from`),
  UNIQUE KEY `ip_to_UNIQUE` (`ip_to`),
  KEY `ip_from_index` (`ip_from`),
  KEY `ip_to_index` (`ip_to`),
  KEY `ip_from_to_index` (`ip_from`,`ip_to`)
) ENGINE=InnoDB AUTO_INCREMENT=2949311 DEFAULT CHARSET=utf8;

#
# Structure for table "translate"
#

DROP TABLE IF EXISTS `translate`;
CREATE TABLE `translate` (
  `zh` varchar(50) NOT NULL,
  `en` varchar(100) NOT NULL,
  `level` int(11) NOT NULL,
  UNIQUE KEY `ch_unique` (`zh`,`level`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
