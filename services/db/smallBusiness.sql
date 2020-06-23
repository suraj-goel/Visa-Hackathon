# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: SG-visahackathon-2575-master.servers.mongodirector.com (MySQL 5.7.25-log)
# Database: smallBusiness
# Generation Time: 2020-06-23 13:22:03 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table Cart
# ------------------------------------------------------------

CREATE TABLE `Cart` (
  `CartID` varchar(256) NOT NULL,
  `Total` varchar(256) NOT NULL,
  `Status` varchar(256) NOT NULL,
  `MerchantID` varchar(256) NOT NULL,
  PRIMARY KEY (`CartID`),
  KEY `MerchantID` (`MerchantID`),
  CONSTRAINT `fk_cart_mid` FOREIGN KEY (`MerchantID`) REFERENCES `Merchant` (`MerchantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table Location
# ------------------------------------------------------------

CREATE TABLE `Location` (
  `LocationID` varchar(256) NOT NULL,
  `Latitude` varchar(256) NOT NULL,
  `Longitude` varchar(256) NOT NULL,
  `MerchantID` varchar(256) NOT NULL,
  PRIMARY KEY (`LocationID`),
  KEY `MerchantID` (`MerchantID`),
  CONSTRAINT `fk_merchantid_location` FOREIGN KEY (`MerchantID`) REFERENCES `Merchant` (`MerchantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table Merchant
# ------------------------------------------------------------

CREATE TABLE `Merchant` (
  `MerchantID` varchar(100) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `RegisteredName` varchar(100) NOT NULL,
  `EmailID` varchar(100) NOT NULL,
  `ContactNumber` varchar(100) NOT NULL,
  `Address` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  PRIMARY KEY (`EmailID`),
  UNIQUE KEY `MerchantID` (`MerchantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table Negotiation
# ------------------------------------------------------------

CREATE TABLE `Negotiation` (
  `NegotiationID` varchar(256) NOT NULL,
  `Status` varchar(256) NOT NULL,
  `CartID` varchar(256) NOT NULL,
  `Price` varchar(256) NOT NULL,
  PRIMARY KEY (`NegotiationID`),
  KEY `CartID` (`CartID`),
  CONSTRAINT `Negotiation_ibfk_1` FOREIGN KEY (`CartID`) REFERENCES `Cart` (`CartID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table Offer
# ------------------------------------------------------------

CREATE TABLE `Offer` (
  `offerID` varchar(256) NOT NULL,
  `Information` varchar(256) NOT NULL,
  `DiscountPercentage` varchar(256) NOT NULL,
  `ValidTill` date NOT NULL,
  `QuantityRequired` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`offerID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table OfferOnProduct
# ------------------------------------------------------------

CREATE TABLE `OfferOnProduct` (
  `OfferProductID` varchar(256) NOT NULL,
  `OfferID` varchar(256) NOT NULL,
  `ProductID` varchar(256) NOT NULL,
  PRIMARY KEY (`OfferProductID`),
  KEY `ProductID` (`ProductID`),
  KEY `OfferID` (`OfferID`),
  CONSTRAINT `fk_offerid_offerassociated` FOREIGN KEY (`OfferID`) REFERENCES `Offer` (`offerID`),
  CONSTRAINT `fk_productid_offerassociated` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table Orders
# ------------------------------------------------------------

CREATE TABLE `Orders` (
  `OrderID` varchar(256) NOT NULL,
  `Status` varchar(256) NOT NULL,
  `CartID` varchar(256) NOT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `CartID` (`CartID`),
  CONSTRAINT `fk_cartid_orders` FOREIGN KEY (`CartID`) REFERENCES `ProductCart` (`CartID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table Product
# ------------------------------------------------------------

CREATE TABLE `Product` (
  `ProductID` varchar(256) NOT NULL,
  `Name` varchar(256) NOT NULL,
  `Description` varchar(256) NOT NULL,
  `Price` varchar(256) NOT NULL,
  `Quantity` varchar(256) NOT NULL,
  `Category` varchar(256) NOT NULL,
  `MerchantID` varchar(256) NOT NULL,
  PRIMARY KEY (`ProductID`),
  UNIQUE KEY `ProductID` (`ProductID`),
  KEY `MerchantID` (`MerchantID`),
  CONSTRAINT `fk` FOREIGN KEY (`MerchantID`) REFERENCES `Merchant` (`MerchantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table ProductCart
# ------------------------------------------------------------

CREATE TABLE `ProductCart` (
  `CartID` varchar(256) NOT NULL,
  `ProductID` varchar(256) NOT NULL,
  `Quantity` varchar(256) NOT NULL,
  PRIMARY KEY (`CartID`,`ProductID`),
  KEY `ProductID` (`ProductID`),
  KEY `CartID` (`CartID`),
  CONSTRAINT `ProductCart_ibfk_1` FOREIGN KEY (`ProductID`) REFERENCES `Product` (`ProductID`),
  CONSTRAINT `fk_product_cart_cartID` FOREIGN KEY (`CartID`) REFERENCES `Cart` (`CartID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table Requirement
# ------------------------------------------------------------

CREATE TABLE `Requirement` (
  `RequirementID` varchar(256) NOT NULL,
  `Title` varchar(256) NOT NULL,
  `Description` varchar(256) NOT NULL,
  `Status` varchar(256) NOT NULL,
  `CartId` varchar(256) DEFAULT NULL,
  `MerchantID` varchar(256) NOT NULL,
  PRIMARY KEY (`RequirementID`),
  KEY `CartId` (`CartId`),
  KEY `MerchantID` (`MerchantID`),
  CONSTRAINT `fk_cart_req` FOREIGN KEY (`CartId`) REFERENCES `ProductCart` (`CartID`),
  CONSTRAINT `fk_merchant` FOREIGN KEY (`MerchantID`) REFERENCES `Merchant` (`MerchantID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
