-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Oct 09, 2024 at 11:17 AM
-- Server version: 5.6.12-log
-- PHP Version: 5.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `ocrdb`
--
CREATE DATABASE IF NOT EXISTS `ocrdb` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `ocrdb`;

-- --------------------------------------------------------

--
-- Table structure for table `answerupload`
--

CREATE TABLE IF NOT EXISTS `answerupload` (
  `auid` int(11) NOT NULL,
  `sname` varchar(50) DEFAULT NULL,
  `emailid` varchar(50) DEFAULT NULL,
  `dname` varchar(50) DEFAULT NULL,
  `cyear` varchar(50) DEFAULT NULL,
  `subname` varchar(200) DEFAULT NULL,
  `safile` varchar(200) DEFAULT NULL,
  `audate` date DEFAULT NULL,
  PRIMARY KEY (`auid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `questable`
--

CREATE TABLE IF NOT EXISTS `questable` (
  `fid` int(11) NOT NULL,
  `dname` varchar(50) DEFAULT NULL,
  `cyear` varchar(50) DEFAULT NULL,
  `subname` varchar(200) DEFAULT NULL,
  `qfile` varchar(200) DEFAULT NULL,
  `afile` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`fid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `resulttable`
--

CREATE TABLE IF NOT EXISTS `resulttable` (
  `auid` int(11) DEFAULT NULL,
  `sname` varchar(50) DEFAULT NULL,
  `emailid` varchar(50) DEFAULT NULL,
  `dname` varchar(50) DEFAULT NULL,
  `cyear` varchar(50) DEFAULT NULL,
  `subname` varchar(50) DEFAULT NULL,
  `per` float DEFAULT NULL,
  `grade` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `studtable`
--

CREATE TABLE IF NOT EXISTS `studtable` (
  `sname` varchar(50) DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `cname` varchar(50) DEFAULT NULL,
  `dname` varchar(50) DEFAULT NULL,
  `cyear` varchar(50) DEFAULT NULL,
  `emailid` varchar(50) NOT NULL,
  `mno` varchar(10) DEFAULT NULL,
  `pword` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`emailid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
