-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 07, 2023 at 03:43 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `futsal`
--

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `ID` int(11) NOT NULL,
  `Name` varchar(200) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Address` varchar(200) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Type_court` varchar(50) NOT NULL,
  `Check_In_Date` varchar(10) NOT NULL,
  `Hour` varchar(10) NOT NULL,
  `Ball` int(1) NOT NULL,
  `Drink` int(1) NOT NULL,
  `Total_Amount` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`ID`, `Name`, `Phone`, `Address`, `Email`, `Type_court`, `Check_In_Date`, `Hour`, `Ball`, `Drink`, `Total_Amount`) VALUES
(9, 'Nazreen', '019-74300321', 'Taman Pauh\n', 'naz@gmail.com', 'Court A', '30/11/2023', '1 Hour', 1, 0, 100),
(10, 'Ainul', '011-23456779', 'Taman Dua\n', 'ainul@gmail.com', 'Court B', '02/12/2023', '2 Hour', 1, 1, 175);

-- --------------------------------------------------------

--
-- Table structure for table `user_account`
--

CREATE TABLE `user_account` (
  `ID` int(11) NOT NULL,
  `username` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_account`
--

INSERT INTO `user_account` (`ID`, `username`, `email`, `password`) VALUES
(1, 'Nazreen', 'naz@gmail.com', '123Nazreen'),
(2, 'Nazreen', 'naz17@gmail.com', '123Nazreen'),
(3, 'Ainull', 'ainul@gmail.com', 'Ainull123'),
(4, 'Alif_haikal', 'alif@gmail.com', 'Aliff123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `user_account`
--
ALTER TABLE `user_account`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `user_account`
--
ALTER TABLE `user_account`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
