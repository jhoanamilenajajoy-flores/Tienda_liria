/*
SQLyog Enterprise v13.1.1 (64 bit)
MySQL - 8.0.30 : Database - tienda_liria
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`tienda_liria` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `tienda_liria`;

/*Table structure for table `categorias_prod` */

DROP TABLE IF EXISTS `categorias_prod`;

CREATE TABLE `categorias_prod` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre_categoria` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `categorias_prod` */

insert  into `categorias_prod`(`id_categoria`,`nombre_categoria`) values 
(1,'aseo'),
(2,'bebidas'),
(3,'comida'),
(4,'otros');

/*Table structure for table `cliente` */

DROP TABLE IF EXISTS `cliente`;

CREATE TABLE `cliente` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre_cliente` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `celular_cliente` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `fecha_registro` date NOT NULL,
  `saldo_cliente` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `cliente` */

/*Table structure for table `cliente_venta` */

DROP TABLE IF EXISTS `cliente_venta`;

CREATE TABLE `cliente_venta` (
  `id_cliente_venta` int NOT NULL AUTO_INCREMENT,
  `id_cliente` int NOT NULL,
  `id_venta` int NOT NULL,
  PRIMARY KEY (`id_cliente_venta`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_venta` (`id_venta`),
  CONSTRAINT `cliente_venta_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`),
  CONSTRAINT `cliente_venta_ibfk_2` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id_venta`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `cliente_venta` */

/*Table structure for table `informe_venta` */

DROP TABLE IF EXISTS `informe_venta`;

CREATE TABLE `informe_venta` (
  `id_informe_venta` int NOT NULL AUTO_INCREMENT,
  `id_venta` int NOT NULL,
  `id_cliente` int NOT NULL,
  `tipo_periodo` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `dia` int DEFAULT NULL,
  `mes` int DEFAULT NULL,
  `año` int DEFAULT NULL,
  PRIMARY KEY (`id_informe_venta`),
  KEY `id_venta` (`id_venta`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `informe_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `venta` (`id_venta`),
  CONSTRAINT `informe_venta_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `informe_venta` */

/*Table structure for table `producto` */

DROP TABLE IF EXISTS `producto`;

CREATE TABLE `producto` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `id_categoria` int NOT NULL,
  `id_proveedor` int NOT NULL,
  `codigo` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `nombre` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `disponibilidad` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `id_categoria` (`id_categoria`),
  KEY `id_proveedor` (`id_proveedor`),
  CONSTRAINT `producto_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias_prod` (`id_categoria`),
  CONSTRAINT `producto_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `producto` */

insert  into `producto`(`id_producto`,`id_categoria`,`id_proveedor`,`codigo`,`nombre`,`precio`,`disponibilidad`) values 
(1,2,1,'01','cocacolamediana',3000.00,'si'),
(2,1,4,'02','limpido',1000.00,'si'),
(3,3,2,'03','frutiño',1500.00,'si');

/*Table structure for table `proveedores` */

DROP TABLE IF EXISTS `proveedores`;

CREATE TABLE `proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre_proveedor` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `celular_proveedor` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `direccion_proveedor` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id_proveedor`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `proveedores` */

insert  into `proveedores`(`id_proveedor`,`nombre_proveedor`,`celular_proveedor`,`direccion_proveedor`) values 
(1,'cocacola','3148089429','Mocoa'),
(2,'frutiño','3148089429','Mocoa'),
(3,'frutiben','3148079456','Pasto'),
(4,'limpialimpia','3148089456','cauca');

/*Table structure for table `venta` */

DROP TABLE IF EXISTS `venta`;

CREATE TABLE `venta` (
  `id_venta` int NOT NULL AUTO_INCREMENT,
  `id_producto` int NOT NULL,
  `cantidad_producto` int NOT NULL,
  `precio_unitario_producto` decimal(10,2) NOT NULL,
  `precio_iva_producto` decimal(10,2) NOT NULL,
  `precio_total_producto` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id_venta`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

/*Data for the table `venta` */

insert  into `venta`(`id_venta`,`id_producto`,`cantidad_producto`,`precio_unitario_producto`,`precio_iva_producto`,`precio_total_producto`) values 
(1,1,3,5000.00,5500.00,15.00);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
