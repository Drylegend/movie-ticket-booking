-- schema.sql
CREATE DATABASE IF NOT EXISTS movie_booking;
USE movie_booking;

CREATE TABLE user (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  email VARCHAR(100) UNIQUE,
  password VARCHAR(255)
);

CREATE TABLE movie (
  movie_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200),
  genre VARCHAR(50),
  duration INT,
  rating VARCHAR(10)
);

CREATE TABLE theater (
  theater_id INT AUTO_INCREMENT PRIMARY KEY,
  theater_name VARCHAR(100),
  location VARCHAR(200)
);

CREATE TABLE showtime (
  show_id INT AUTO_INCREMENT PRIMARY KEY,
  movie_id INT,
  theater_id INT,
  show_date DATE,
  start_time TIME,
  end_time TIME,
  FOREIGN KEY (movie_id) REFERENCES movie(movie_id),
  FOREIGN KEY (theater_id) REFERENCES theater(theater_id)
);

CREATE TABLE seat (
  seat_id INT AUTO_INCREMENT PRIMARY KEY,
  show_id INT,
  seat_number VARCHAR(10),
  is_booked BOOLEAN DEFAULT FALSE,
  FOREIGN KEY (show_id) REFERENCES showtime(show_id)
);

CREATE TABLE booking (
  booking_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT,
  show_id INT,
  seat_id INT,
  booking_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES user(user_id),
  FOREIGN KEY (show_id) REFERENCES showtime(show_id),
  FOREIGN KEY (seat_id) REFERENCES seat(seat_id)
);

CREATE TABLE payment (
  payment_id INT AUTO_INCREMENT PRIMARY KEY,
  booking_id INT,
  amount DECIMAL(10,2),
  payment_method VARCHAR(50),
  payment_status VARCHAR(20) DEFAULT 'Pending',
  payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (booking_id) REFERENCES booking(booking_id)
);
