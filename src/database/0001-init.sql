CREATE DATABASE cryptography_chat;

USE cryptography_chat;

CREATE TABLE chats (
    id INT PRIMARY KEY AUTO_INCREMENT,
    source_port INT NOT NULL,
    destination_port INT NOT NULL,
    method VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);