create database Salas_Conferencia;
use  Salas_Conferencia;

create table user(
    id int auto_increment primary key,
    name varchar(100),
    email varchar(100) unique,
    password varchar(255),
    role enum('user', 'admin') default 'user'
);

CREATE TABLE room (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    capacity INT,
    location VARCHAR(200),
    availability BOOLEAN DEFAULT TRUE
);

CREATE TABLE reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    room_id INT,
    start_time DATETIME,
    end_time DATETIME,
    status ENUM('active', 'cancelled') DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);

-- Creación de datos de usuarios
INSERT INTO user (id, name, email, role)
VALUES 
(4, 'Alice', 'alice@example.com', 'user'),
(5, 'Bob', 'bob@example.com', 'admin'),
(6, 'Charlie', 'charlie@example.com', 'user'),
(7, 'Diana', 'diana@example.com', 'user');

-- Creación de datos de salas
INSERT INTO room (id, name, capacity, location)
VALUES
(2, 'Sala A', 20, 'Edificio 1, Piso 2'),
(6, 'Sala B', 15, 'Edificio 1, Piso 1'),
(7, 'Sala C', 25, 'Edificio 2, Piso 3'),
(8, 'Sala D', 10, 'Edificio 3, Piso 1');


INSERT INTO reservation (user_id, room_id, start_time, end_time, status)
VALUES
(1, 1, '2024-11-27 09:00:00', '2024-11-27 11:00:00', 'active'),
(2, 2, '2024-11-27 14:00:00', '2024-11-27 16:00:00', 'active'),
(3, 3, '2024-11-28 10:00:00', '2024-11-28 12:00:00', 'cancelled'),
(4, 1, '2024-11-29 08:00:00', '2024-11-29 10:00:00', 'active'),
(1, 2, '2024-11-30 15:00:00', '2024-11-30 17:00:00', 'active');


select * from user;
select * from room;
select * from reservation;
SELECT * FROM room WHERE availability = TRUE; 