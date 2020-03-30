-- Drop, create fresh studentdb
DROP DATABASE IF EXISTS
  studentdb;
CREATE DATABASE
  studentdb;

-- Create superuser
CREATE USER
  student
WITH
  SUPERUSER PASSWORD 'student';

-- Grant privileges
GRANT
  ALL PRIVILEGES
ON
  DATABASE studentdb
TO student;
