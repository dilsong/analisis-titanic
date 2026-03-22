CREATE DATABASE rrhh_analytics;
use rrhh_analytics;

-- Tabla 1: Departamentos
CREATE TABLE departamentos (
    id_departamento INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla 2: Cargos
CREATE TABLE cargos (
    id_cargo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    nivel INT NOT NULL
);

-- Tabla 3: Empleados
CREATE TABLE empleados (
    id_empleado INT PRIMARY KEY,
    edad INT,
    genero VARCHAR(10),
    estado_civil VARCHAR(20),
    educacion INT,
    campo_educacion VARCHAR(50),
    id_departamento INT,
    id_cargo INT,
    salario_mensual DECIMAL(10,2),
    horas_extra VARCHAR(5),
    viaje_negocios VARCHAR(30),
    rotacion VARCHAR(5),
    FOREIGN KEY (id_departamento) REFERENCES departamentos(id_departamento),
    FOREIGN KEY (id_cargo) REFERENCES cargos(id_cargo)
);

-- Tabla 4: Satisfaccion
CREATE TABLE satisfaccion (
    id_empleado INT PRIMARY KEY,
    satisfaccion_trabajo INT,
    satisfaccion_ambiente INT,
    satisfaccion_relacion INT,
    balance_vida INT,
    involucramiento INT,
    calificacion_desempeño INT,
    FOREIGN KEY (id_empleado) REFERENCES empleados(id_empleado)
);



-- Verificar departamentos
SELECT * FROM departamentos;

-- Verificar top 5 empleados con su departamento y cargo
SELECT e.id_empleado, e.edad, e.genero, 
       d.nombre AS departamento,
       c.nombre AS cargo,
       e.salario_mensual,
       e.rotacion
FROM empleados e
JOIN departamentos d ON e.id_departamento = d.id_departamento
JOIN cargos c ON e.id_cargo = c.id_cargo
LIMIT 5;