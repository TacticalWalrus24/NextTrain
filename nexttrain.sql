-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 15, 2021 at 01:07 PM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.5

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nexttrain`
--

-- --------------------------------------------------------

--
-- Table structure for table `linesegments`
--

CREATE TABLE `linesegments` (
  `RailID` int(11) NOT NULL,
  `LineID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `linesegments`
--

INSERT INTO `linesegments` (`RailID`, `LineID`) VALUES
(53124, 12345),
(13524, 12345),
(24135, 12345),
(24531, 12345),
(24531, 54321),
(24135, 54321),
(13524, 54321),
(53124, 54321);

-- --------------------------------------------------------

--
-- Table structure for table `platforms`
--

CREATE TABLE `platforms` (
  `PlatformNumber` int(11) NOT NULL,
  `Occupied` tinyint(1) DEFAULT 0,
  `StationID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `raillines`
--

CREATE TABLE `raillines` (
  `LineID` int(11) NOT NULL,
  `LineName` varchar(255) NOT NULL DEFAULT ' ',
  `PopUlarity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `raillines`
--

INSERT INTO `raillines` (`LineID`, `LineName`, `PopUlarity`) VALUES
(12345, 'TestLine', 3),
(54321, 'eniLtseT', 3);

-- --------------------------------------------------------

--
-- Table structure for table `rails`
--

CREATE TABLE `rails` (
  `RailID` int(11) NOT NULL,
  `Length` int(11) NOT NULL,
  `Width` int(11) DEFAULT 1,
  `StartStation` int(11) NOT NULL,
  `EndStation` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `rails`
--

INSERT INTO `rails` (`RailID`, `Length`, `Width`, `StartStation`, `EndStation`) VALUES
(13524, 10, 10, 12543, 21453),
(24135, 6, 8, 21453, 21543),
(24531, 4, 3, 21543, 21345),
(53124, 5, 4, 54123, 12543);

-- --------------------------------------------------------

--
-- Table structure for table `stationlines`
--

CREATE TABLE `stationlines` (
  `LineID` int(11) NOT NULL,
  `StationID` int(11) NOT NULL,
  `StopNumber` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stationlines`
--

INSERT INTO `stationlines` (`LineID`, `StationID`, `StopNumber`) VALUES
(12345, 54123, 1),
(12345, 12543, 2),
(12345, 21453, 3),
(12345, 21543, 4),
(12345, 21345, 5),
(54321, 21345, 1),
(54321, 21543, 2),
(54321, 21453, 3),
(54321, 12543, 4),
(54321, 54123, 5);

-- --------------------------------------------------------

--
-- Table structure for table `stations`
--

CREATE TABLE `stations` (
  `StationID` int(11) NOT NULL,
  `StationName` varchar(255) NOT NULL DEFAULT ' ',
  `Poularity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stations`
--

INSERT INTO `stations` (`StationID`, `StationName`, `Poularity`) VALUES
(12543, 'Station2', 3),
(21345, 'Station5', 3),
(21453, 'Station3', 3),
(21543, 'Station4', 3),
(54123, 'Station1', 3);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `linesegments`
--
ALTER TABLE `linesegments`
  ADD KEY `RailID` (`RailID`),
  ADD KEY `LineID` (`LineID`);

--
-- Indexes for table `platforms`
--
ALTER TABLE `platforms`
  ADD PRIMARY KEY (`PlatformNumber`),
  ADD KEY `StationID` (`StationID`);

--
-- Indexes for table `raillines`
--
ALTER TABLE `raillines`
  ADD PRIMARY KEY (`LineID`);

--
-- Indexes for table `rails`
--
ALTER TABLE `rails`
  ADD PRIMARY KEY (`RailID`),
  ADD KEY `StartStation` (`StartStation`),
  ADD KEY `EndStation` (`EndStation`);

--
-- Indexes for table `stationlines`
--
ALTER TABLE `stationlines`
  ADD KEY `LineID` (`LineID`),
  ADD KEY `StationID` (`StationID`);

--
-- Indexes for table `stations`
--
ALTER TABLE `stations`
  ADD PRIMARY KEY (`StationID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `linesegments`
--
ALTER TABLE `linesegments`
  ADD CONSTRAINT `linesegments_ibfk_1` FOREIGN KEY (`RailID`) REFERENCES `rails` (`RailID`),
  ADD CONSTRAINT `linesegments_ibfk_2` FOREIGN KEY (`LineID`) REFERENCES `raillines` (`LineID`);

--
-- Constraints for table `platforms`
--
ALTER TABLE `platforms`
  ADD CONSTRAINT `platforms_ibfk_1` FOREIGN KEY (`StationID`) REFERENCES `stations` (`StationID`);

--
-- Constraints for table `rails`
--
ALTER TABLE `rails`
  ADD CONSTRAINT `rails_ibfk_1` FOREIGN KEY (`StartStation`) REFERENCES `stations` (`StationID`),
  ADD CONSTRAINT `rails_ibfk_2` FOREIGN KEY (`EndStation`) REFERENCES `stations` (`StationID`);

--
-- Constraints for table `stationlines`
--
ALTER TABLE `stationlines`
  ADD CONSTRAINT `stationlines_ibfk_1` FOREIGN KEY (`LineID`) REFERENCES `raillines` (`LineID`),
  ADD CONSTRAINT `stationlines_ibfk_2` FOREIGN KEY (`StationID`) REFERENCES `stations` (`StationID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
