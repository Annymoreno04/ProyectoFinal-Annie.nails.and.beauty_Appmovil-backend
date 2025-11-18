-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 18-11-2025 a las 06:03:24
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `annienails`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias_servicios`
--

CREATE TABLE `categorias_servicios` (
  `id_categoria` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `categorias_servicios`
--

INSERT INTO `categorias_servicios` (`id_categoria`, `nombre`, `descripcion`) VALUES
(1, 'Uñas', 'Servicios de manicura, acrílicas, gel, etc y mas'),
(2, 'Cabello', 'Cortes, cepillado y tratamientos capilares.'),
(3, 'Facial y Corporal', 'Limpieza facial, spa y tratamientos relajantes.'),
(4, 'Estética', 'Maquillaje y cuidado facial.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `citas`
--

CREATE TABLE `citas` (
  `id_cita` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `id_empleado` int(11) DEFAULT NULL,
  `fecha_cita` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `estado` enum('pendiente','confirmada','completada','cancelada','no_realizada') DEFAULT 'pendiente'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `citas`
--

INSERT INTO `citas` (`id_cita`, `id_usuario`, `id_servicio`, `id_empleado`, `fecha_cita`, `hora_inicio`, `estado`) VALUES
(27, 7, 2, 3, '2025-11-18', '12:40:00', 'completada');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `especialidad` varchar(100) DEFAULT NULL,
  `anos_experiencia` int(11) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `hora_inicio_atencion` time DEFAULT '10:00:00',
  `hora_fin_atencion` time DEFAULT '17:00:00',
  `estado` enum('activo','inactivo') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `id_usuario`, `especialidad`, `anos_experiencia`, `descripcion`, `hora_inicio_atencion`, `hora_fin_atencion`, `estado`) VALUES
(1, 10, 'Manicurista', 5, 'Experta en manicura con una pasión por el arte y la precisión. Con 5 años de experiencia, especializada en manicuras que promueven la salud de las uñas.', '10:00:00', '17:00:00', 'activo'),
(2, 11, 'Manicurista', 4, 'Manicurista dedicada con habilidades expertas en cuidado de uñas. Con 4 años de trayectoria, combina técnicas modernas con atención meticulosa a los detalles.', '10:00:00', '17:00:00', 'activo'),
(3, 12, 'Manicurista', 2, 'Profesional enfocada en la belleza y el bienestar de las uñas. Con 2 años de experiencia, fusiona técnicas tradicionales con las últimas tendencias.', '10:00:00', '17:00:00', 'activo'),
(4, 13, 'Manicurista', 1, 'Especialista en crear diseños impresionantes. Con 1 año en la industria, se enfoca en manicuras artísticas y terapéuticas que cuidan la salud de las uñas.', '10:00:00', '17:00:00', 'activo'),
(5, 14, 'Manicurista', 4, 'Manicurista certificada con experiencia en técnicas avanzadas. Con 4 años, ofrece manicuras de alta calidad que combinan estética y bienestar.', '10:00:00', '17:00:00', 'activo'),
(6, 15, 'Manicurista', 2, 'Comprometida con la excelencia y la creatividad. Con 2 años de experiencia, domina técnicas de cuidado de uñas desde lo clásico hasta lo contemporáneo.', '10:00:00', '17:00:00', 'activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horarios`
--

CREATE TABLE `horarios` (
  `id` int(11) NOT NULL,
  `hora` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `horarios`
--

INSERT INTO `horarios` (`id`, `hora`) VALUES
(1, '10:10 AM'),
(2, '11:00 AM'),
(3, '11:50 AM'),
(4, '12:40 PM'),
(5, '1:30 PM'),
(6, '2:20 PM'),
(7, '3:10 PM'),
(8, '4:00 PM');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `roles`
--

CREATE TABLE `roles` (
  `id_rol` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `roles`
--

INSERT INTO `roles` (`id_rol`, `nombre`) VALUES
(1, 'Administrador'),
(2, 'Cliente'),
(3, 'Empleado');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id_servicio` int(11) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `descripcion` text DEFAULT NULL,
  `duracion_minutos` int(11) DEFAULT 45
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id_servicio`, `id_categoria`, `titulo`, `descripcion`, `duracion_minutos`) VALUES
(1, 1, 'Acrílicas\r\n', 'Uñas resistentes y estilizadas con acrílico.', 45),
(2, 1, 'Dipping', 'Técnica en polvo para un acabado natural y duradero.', 45),
(3, 1, 'Press On', 'Uñas removibles, prácticas y de larga duración.', 45),
(4, 1, 'Gel', 'Brillo intenso y duración prolongada en tus uñas.', 45),
(5, 1, 'Semi', 'Esmaltado semipermanente con acabado profesional..', 45),
(6, 1, 'Forrado Acrílico', 'Protección y refuerzo de la uña natural con acrílico.', 45),
(7, 1, 'Retoque de uñas', 'Dale una segunda vida a tus uñas.', 45),
(8, 2, 'Corte / cepillado', 'Corte moderno y cepillado profesional.', 45),
(9, 2, 'Hidratación capilar', 'Tratamiento para revitalizar y dar brillo al cabello.', 45),
(10, 2, 'Tintura o mechas', 'Coloración con productos de alta calidad.', 45),
(11, 2, 'Peinados para eventos', 'Peinados elegantes para ocasiones especiales.', 45),
(12, 3, 'Limpieza facial', 'Elimina impurezas y revitaliza tu piel.', 45),
(13, 3, 'Masaje relajante', 'Reduce el estrés y mejora tu bienestar.', 45),
(14, 3, 'Depilación facial / corporal', 'Piel suave y libre de vello.', 45),
(15, 4, 'Maquillaje profesional', 'Maquillaje para eventos o sesiones fotográficas.', 45),
(16, 4, 'Lifting o extensión de pestañas', 'Mirada impactante con efecto natural.', 45),
(17, 4, 'Diseño de cejas', 'Cejas definidas que enmarcan tu rostro.', 45);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `trabajos`
--

CREATE TABLE `trabajos` (
  `id` int(11) NOT NULL,
  `titulo` varchar(100) NOT NULL,
  `descripcion` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `trabajos`
--

INSERT INTO `trabajos` (`id`, `titulo`, `descripcion`) VALUES
(1, 'FORRADO DE ACRÍLICO', 'Diseño de frances fucsia y brillantina con decoración de corazones.'),
(2, 'DISEÑO DE CEJAS', 'Diseño de cejas con henna, permace días con un buen estilo de cejas.'),
(3, 'TRENZAS AFRICANAS', 'Diseño de trenzas para ocasiones especiales y para mantener un buen look.'),
(4, 'TÉCNICA DIPPING', 'Diseño de flores con color otoño y frances sencillo.'),
(5, 'MAQUILLAJE PROFESIONAL', 'Diseño de maquillaje profesional para eventos con diseño estilizado.'),
(6, 'TINTE DE CABELLO', 'Diseño de tinturación de cabello afro con color cobrizo.'),
(7, 'RETOQUE DE UÑAS', 'Retoque de uñas.'),
(8, 'UÑAS EN GEL', 'Diseño de mariposas con colores fucsia y amarillo, decoradas con frances fucsia con puntos blancos.');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tutoriales`
--

CREATE TABLE `tutoriales` (
  `id` int(11) NOT NULL,
  `id_categoria` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tutoriales`
--

INSERT INTO `tutoriales` (`id`, `id_categoria`, `titulo`, `descripcion`) VALUES
(1, 1, 'Uñas Acrílicas: Guía Completa', 'Aprende paso a paso cómo aplicar uñas acrílicas...'),
(2, 1, 'Manicura Francesa: Un Clásico que Nunca Falla', 'Descubre cómo lograr una manicura francesa perfecta...'),
(3, 1, 'Tendencias de Esmaltes para el 2025', 'Conoce los colores y estilos más populares...');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `id_rol` int(11) NOT NULL,
  `nombre_usuario` varchar(50) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(100) DEFAULT NULL,
  `clave` varchar(255) NOT NULL,
  `estado` enum('activo','inactivo') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `id_rol`, `nombre_usuario`, `nombre`, `telefono`, `correo`, `clave`, `estado`) VALUES
(7, 2, 'Angie04', 'Angela Romana c', '3152036651', 'angir12@gmail.com', '$2b$12$6zbW6.rUOTnbV6jWtbYSpuoPh7bhzCnma/S2i7TSHBK4zxCX.O7HO', 'activo'),
(8, 1, 'Anny04', 'Anny Moreno', '322566615', 'morempleudo@gmail.com', '$2b$12$pgOljW03l4W.UFNLOeRefehPkj7HbNqxgq7AqzL/ybF0o9WpP8iKi', 'activo'),
(9, 3, 'ann11', 'Anny Moreno L', '3015623589', 'morenoleudoaaa@gmail.com', '$2b$12$NaBYI1PWOgHaaKphaPBDgeptalWGkwtgsYfm4O7NMiYAsP3.hTPBS', 'activo'),
(10, 3, 'angie.mena', 'Angie Mena', '3001234567', 'angie.mena@salon.com', '$2b$12$Y59yFPE2D.G8SeG.FUUtZeg9.FVHSih/Zic/UCBLFcUF3OeWuZhb6', 'activo'),
(11, 3, 'caroline.perea', 'Caroline Perea', '3001234568', 'caroline.perea@salon.com', '$2b$12$zocpNyQiZjv4ypFBhJoGM.VMtWQJ8zWMQ4utQfiYOH32pJtrdyf7S', 'activo'),
(12, 3, 'stefhany.lemus', 'Stefhany Lemus', '3001234569', 'stefhany.lemus@salon.com', '$2b$12$hUpI6Y6AyumLlEKVPfJQZu1r7AWIgnBljmf0KGBeI8Xr1hnEJE3c2', 'activo'),
(13, 3, 'andrea.moreno', 'Andrea Moreno', '3001234570', 'andrea.moreno@salon.com', '$2b$12$.FKX7ZYVdws.z4t087B/1exUPnjgavam28UsVkRLQ5Eia7bmNtKz6', 'activo'),
(14, 3, 'tatiana.palacios', 'Tatiana Palacios', '3001234571', 'tatiana.palacios@salon.com', '$2b$12$fvPE7Pk/7gLgOFdLq5MoZe8QuCQc9EPk80tcg0KKKryFSBNY.l2Ge', 'activo'),
(15, 2, 'ashly.valderrama', 'Ashly Valderrama', '3001234572', 'ashly.valderrama@salon.com', '$2b$12$sS1zcTFk5kg3GB0U75o3tetEZvqnsdVGK8LcQqhcM2vAa8ihjZ4YK', 'activo');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias_servicios`
--
ALTER TABLE `categorias_servicios`
  ADD PRIMARY KEY (`id_categoria`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `citas`
--
ALTER TABLE `citas`
  ADD PRIMARY KEY (`id_cita`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_servicio` (`id_servicio`),
  ADD KEY `id_empleado` (`id_empleado`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`),
  ADD UNIQUE KEY `id_usuario` (`id_usuario`);

--
-- Indices de la tabla `horarios`
--
ALTER TABLE `horarios`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id_rol`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`id_servicio`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Indices de la tabla `trabajos`
--
ALTER TABLE `trabajos`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `tutoriales`
--
ALTER TABLE `tutoriales`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_categoria` (`id_categoria`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `nombre_usuario` (`nombre_usuario`),
  ADD UNIQUE KEY `correo` (`correo`),
  ADD KEY `id_rol` (`id_rol`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `categorias_servicios`
--
ALTER TABLE `categorias_servicios`
  MODIFY `id_categoria` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT de la tabla `citas`
--
ALTER TABLE `citas`
  MODIFY `id_cita` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `horarios`
--
ALTER TABLE `horarios`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT de la tabla `roles`
--
ALTER TABLE `roles`
  MODIFY `id_rol` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `id_servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT de la tabla `trabajos`
--
ALTER TABLE `trabajos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `tutoriales`
--
ALTER TABLE `tutoriales`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `citas`
--
ALTER TABLE `citas`
  ADD CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_servicio`),
  ADD CONSTRAINT `citas_ibfk_3` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`);

--
-- Filtros para la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD CONSTRAINT `empleados_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE;

--
-- Filtros para la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD CONSTRAINT `servicios_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias_servicios` (`id_categoria`);

--
-- Filtros para la tabla `tutoriales`
--
ALTER TABLE `tutoriales`
  ADD CONSTRAINT `tutoriales_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias_servicios` (`id_categoria`);

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `usuarios_ibfk_1` FOREIGN KEY (`id_rol`) REFERENCES `roles` (`id_rol`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
