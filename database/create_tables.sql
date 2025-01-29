CREATE DATABASE faq_assistant;

USE faq_assistant;

CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query TEXT NOT NULL,
    response TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE knowledge_base (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);