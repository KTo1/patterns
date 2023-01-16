PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS students;
CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name VARCHAR (32)
);

DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    name TEXT
);

DROP TABLE IF EXISTS courses;
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
    id_category INTEGER,
    name TEXT,
    FOREIGN KEY (id_category) REFERENCES categories(id)
);

DROP TABLE IF EXISTS students_courses;
CREATE TABLE students_courses (
    id_student INTEGER,
    id_course INTEGER,
    FOREIGN KEY (id_student) REFERENCES students(id),
    FOREIGN KEY (id_course) REFERENCES courses(id)
);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
