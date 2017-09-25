/*
MySQL Data Transfer
Source Host: localhost
Source Database: mydb
Target Host: localhost
Target Database: mydb
Date: 2012/10/31 10:54:35
*/

SET FOREIGN_KEY_CHECKS=0;
-- ----------------------------
-- Table structure for products
-- ----------------------------
CREATE TABLE `products` (
  `id` int(11) NOT NULL auto_increment,
  `parentId` int(11) default NULL,
  `name` varchar(50) default NULL,
  `quantity` int(11) default NULL,
  `price` decimal(10,2) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records 
-- ----------------------------
INSERT INTO `products` VALUES ('1', '0', 'Computers', null, null);
INSERT INTO `products` VALUES ('2', '0', 'Electronics', null, null);
INSERT INTO `products` VALUES ('3', '2', 'Digital Cameras', null, null);
INSERT INTO `products` VALUES ('4', '2', 'DVD', null, null);
INSERT INTO `products` VALUES ('5', '2', 'MP3 Players', null, null);
INSERT INTO `products` VALUES ('6', '2', 'Video Games', null, null);
INSERT INTO `products` VALUES ('7', '1', 'Printers', null, null);
INSERT INTO `products` VALUES ('8', '1', 'Firewall', null, null);
INSERT INTO `products` VALUES ('9', '1', 'Keyboard', null, null);
INSERT INTO `products` VALUES ('10', '3', 'Nikon COOLPIX L26 16.1 MP', '12', '74.97');
INSERT INTO `products` VALUES ('11', '3', 'Canon PowerShot A1300', '143', '109.99');
INSERT INTO `products` VALUES ('12', '3', 'Canon PowerShot A2300', '32', '91.52');
INSERT INTO `products` VALUES ('13', '4', 'Verbatim 95101 4.7 GB', '35', '11.81');
INSERT INTO `products` VALUES ('14', '4', 'Brave', '78', '14.99');
INSERT INTO `products` VALUES ('15', '4', 'Sony DVPSR510H DVD Player', '223', '43.23');
INSERT INTO `products` VALUES ('16', '5', 'SanDisk Sansa Clip Zip 4GB', '21', '30.74');
INSERT INTO `products` VALUES ('17', '5', 'BLUE MP3 Metal Mini Clip Player', '56', '2.99');
INSERT INTO `products` VALUES ('18', '6', 'Assassin\'s Creed III', '39', '58.65');
INSERT INTO `products` VALUES ('19', '6', 'Call of Duty: Modern Warfare 3', '76', '37.48');
INSERT INTO `products` VALUES ('20', '7', 'Epson WorkForce 845', '69', '121.29');
INSERT INTO `products` VALUES ('21', '7', 'Canon PIXMA MG5320', '12', '110.12');
INSERT INTO `products` VALUES ('22', '7', 'HP Deskjet 1000 Printer', '63', '33.95');
INSERT INTO `products` VALUES ('23', '8', 'Cisco RV110W-A-NA-K9', '103', '79.95');
INSERT INTO `products` VALUES ('24', '8', 'ZyXEL ZyWALL USG50', '34', '209.99');
INSERT INTO `products` VALUES ('25', '8', 'NETGEAR FVS318', '67', '89.99');
INSERT INTO `products` VALUES ('26', '9', 'Logitech Keyboard K120', '45', '9.93');
INSERT INTO `products` VALUES ('27', '9', 'Microsoft Natural Ergonomic Keyboard 4000', '89', '37.69');
INSERT INTO `products` VALUES ('28', '9', 'Logitech Wireless Touch Keyboard K400', '41', '34.99');
INSERT INTO `products` VALUES ('29', '9', 'Logitech Gaming Keyboard G110', '67', '59.99');
