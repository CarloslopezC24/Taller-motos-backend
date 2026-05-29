SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS `registros`;
DROP TABLE IF EXISTS `usuarios`;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE `usuarios` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre_usuario` VARCHAR(100) NOT NULL,
  `password` VARCHAR(255) NOT NULL, 
  `tipo_plan` VARCHAR(50) DEFAULT 'Básico',
  `rol` VARCHAR(50) DEFAULT 'Usuario',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `registros` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(150) NOT NULL,
  `categoria` VARCHAR(100) NOT NULL,
  `descripcion` TEXT DEFAULT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `destacado` TINYINT(1) DEFAULT 0,
  `activo` TINYINT(1) DEFAULT 1,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


INSERT INTO `usuarios` (`id`, `nombre_usuario`, `password`, `tipo_plan`, `rol`) VALUES
(1, 'Carlos López', 'admin123', 'Premium', 'Administrador');

INSERT INTO `registros` (`nombre`, `categoria`, `descripcion`, `precio`, `destacado`, `activo`) VALUES
('Cambio de Aceite Sintético', 'Servicio Preventivo', 'Cambio de aceite de alta gama 10W40 o 15W50, incluye lavado de filtro de partículas y revisión de niveles.', 350.00, 1, 1),
('Ajuste y Lubricación de Cadena', 'Mantenimiento', 'Limpieza profunda de la transmisión final con desengrasante especial, ajuste de tensión exacta y lubricación con grasa de alta adherencia.', 150.00, 0, 1),
('Diagnóstico de Sistema Eléctrico', 'Servicio Correctivo', 'Revisión completa de batería, alternador, regulador de voltaje y arnés principal utilizando multímetro avanzado.', 450.00, 1, 1);