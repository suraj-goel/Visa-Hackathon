-- phpMyAdmin SQL Dump
-- version 4.9.5deb2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jun 22, 2020 at 05:54 PM
-- Server version: 8.0.20-0ubuntu0.20.04.1
-- PHP Version: 7.4.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `small_business`
--

-- --------------------------------------------------------

--
-- Table structure for table `Location`
--

CREATE TABLE `Location` (
  `LocationID` varchar(256) NOT NULL,
  `Latitude` varchar(256) NOT NULL,
  `Longitude` varchar(256) NOT NULL,
  `MerchantID` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Merchant`
--

CREATE TABLE `Merchant` (
  `MerchantID` varchar(100) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `RegisteredName` varchar(100) NOT NULL,
  `EmailID` varchar(100) NOT NULL,
  `ContactNumber` varchar(100) NOT NULL,
  `Address` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Merchant`
--

INSERT INTO `Merchant` (`MerchantID`, `Name`, `RegisteredName`, `EmailID`, `ContactNumber`, `Address`, `Password`) VALUES
('1', 'suraj', 'myshop', 'surajgoel@mnnit.ac.in', '8901435825', 'india', 'abc');

-- --------------------------------------------------------

--
-- Table structure for table `Negotiation`
--

CREATE TABLE `Negotiation` (
  `NegotiationID` varchar(256) NOT NULL,
  `Status` varchar(256) NOT NULL,
  `CartID` varchar(256) NOT NULL,
  `Price` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Offer`
--

CREATE TABLE `Offer` (
  `offerID` varchar(256) NOT NULL,
  `Information` varchar(256) NOT NULL,
  `DiscountPercentage` varchar(256) NOT NULL,
  `ValidTill` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `OfferOnProduct`
--

CREATE TABLE `OfferOnProduct` (
  `OfferProductID` varchar(256) NOT NULL,
  `OfferID` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `ProductID` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Orders`
--

CREATE TABLE `Orders` (
  `OrderID` varchar(256) NOT NULL,
  `Status` varchar(256) NOT NULL,
  `CartID` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Product`
--

CREATE TABLE `Product` (
  `ProductID` varchar(256) NOT NULL,
  `Name` varchar(256) NOT NULL,
  `Description` varchar(256) NOT NULL,
  `Price` varchar(256) NOT NULL,
  `Quantity` varchar(256) NOT NULL,
  `Category` varchar(256) NOT NULL,
  `MerchantID` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `Product`
--

INSERT INTO `Product` (`ProductID`, `Name`, `Description`, `Price`, `Quantity`, `Category`, `MerchantID`) VALUES
('1', 'Biscuit', 'This is biscuit', '30', '20', 'Food', '1');

-- --------------------------------------------------------

--
-- Table structure for table `ProductCart`
--

CREATE TABLE `ProductCart` (
  `CartID` varchar(256) NOT NULL,
  `MerchantID` varchar(256) NOT NULL,
  `ProductID` varchar(256) NOT NULL,
  `Status` varchar(256) NOT NULL,
  `Price` varchar(256) NOT NULL,
  `Information` varchar(512) DEFAULT NULL,
  `Quantity` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `ProductCart`
--

INSERT INTO `ProductCart` (`CartID`, `MerchantID`, `ProductID`, `Status`, `Price`, `Information`, `Quantity`) VALUES
('1', '1', '1', 'pending', '200', 'Test Data', '2');

-- --------------------------------------------------------

--
-- Table structure for table `Requirement`
--

CREATE TABLE `Requirement` (
  `RequirementID` varchar(256) NOT NULL,
  `Title` varchar(256) NOT NULL,
  `Description` varchar(256) NOT NULL,
  `Status` varchar(256) NOT NULL,
  `CartId` varchar(256) DEFAULT NULL,
  `MerchantID` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Location`
--
ALTER TABLE `Location`
  ADD PRIMARY KEY (`LocationID`),
  ADD KEY `MerchantID` (`MerchantID`);

--
-- Indexes for table `Merchant`
--
ALTER TABLE `Merchant`
  ADD PRIMARY KEY (`EmailID`),
  ADD UNIQUE KEY `MerchantID` (`MerchantID`);

--
-- Indexes for table `Negotiation`
--
ALTER TABLE `Negotiation`
  ADD PRIMARY KEY (`NegotiationID`),
  ADD KEY `CartID` (`CartID`);

--
-- Indexes for table `Offer`
--
ALTER TABLE `Offer`
  ADD PRIMARY KEY (`offerID`);

--
-- Indexes for table `OfferOnProduct`
--
ALTER TABLE `OfferOnProduct`
  ADD PRIMARY KEY (`OfferProductID`),
  ADD KEY `ProductID` (`ProductID`),
  ADD KEY `OfferID` (`OfferID`);

--
-- Indexes for table `Orders`
--
ALTER TABLE `Orders`
  ADD PRIMARY KEY (`OrderID`),
  ADD KEY `CartID` (`CartID`);

--
-- Indexes for table `Product`
--
ALTER TABLE `Product`
  ADD PRIMARY KEY (`ProductID`),
  ADD UNIQUE KEY `ProductID` (`ProductID`),
  ADD KEY `MerchantID` (`MerchantID`);

--
-- Indexes for table `ProductCart`
--
ALTER TABLE `ProductCart`
  ADD PRIMARY KEY (`CartID`,`ProductID`),
  ADD KEY `MerchantID` (`MerchantID`),
  ADD KEY `ProductID` (`ProductID`);

--
-- Indexes for table `Requirement`
--
ALTER TABLE `Requirement`
  ADD PRIMARY KEY (`RequirementID`),
  ADD KEY `CartId` (`CartId`),
  ADD KEY `MerchantID` (`MerchantID`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Location`
--
ALTER TABLE `Location`
  ADD CONSTRAINT `fk_merchantid_location` FOREIGN KEY (`MerchantID`) REFERENCES `Merchant` (`MerchantID`);

--
-- Constraints for table `Negotiation`
--
ALTER TABLE `Negotiation`
  ADD CONSTRAINT `fk_cartid_nego` FOREIGN KEY (`CartID`) REFERENCES `ProductCart` (`CartID`);

--
-- Constraints for table `OfferOnProduct`
--
ALTER TABLE `OfferOnProduct`
  ADD CONSTRAINT `fk_offerid_offerassociated` FOREIGN KEY (`OfferID`) REFERENCES `Offer` (`offerID`),
  ADD CONSTRAINT `fk_productid_offerassociated` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`);

--
-- Constraints for table `Orders`
--
ALTER TABLE `Orders`
  ADD CONSTRAINT `fk_cartid_orders` FOREIGN KEY (`CartID`) REFERENCES `ProductCart` (`CartID`);

--
-- Constraints for table `Product`
--
ALTER TABLE `Product`
  ADD CONSTRAINT `fk` FOREIGN KEY (`MerchantID`) REFERENCES `Merchant` (`MerchantID`);

--
-- Constraints for table `ProductCart`
--
ALTER TABLE `ProductCart`
  ADD CONSTRAINT `fk_merchant_cart` FOREIGN KEY (`MerchantID`) REFERENCES `Merchant` (`MerchantID`),
  ADD CONSTRAINT `fk_product_cart` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`);

--
-- Constraints for table `Requirement`
--
ALTER TABLE `Requirement`
  ADD CONSTRAINT `fk_cart_req` FOREIGN KEY (`CartId`) REFERENCES `ProductCart` (`CartID`),
  ADD CONSTRAINT `fk_merchant` FOREIGN KEY (`MerchantID`) REFERENCES `Merchant` (`MerchantID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
