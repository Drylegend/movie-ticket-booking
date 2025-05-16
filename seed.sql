-- seed.sql
USE movie_booking;

INSERT INTO user (name, email, password) VALUES
  ('Alice', 'alice@example.com', 'passwordhash1'),
  ('Bob',   'bob@example.com',   'passwordhash2');

INSERT INTO movie (title, genre, duration, rating) VALUES
  ('Inception',       'Sci-Fi',    148, 'PG-13'),
  ('The Matrix',      'Sci-Fi',    136, 'R'),
  ('Avengers',        'Action',    143, 'PG-13'),
  ('Joker',           'Drama',     122, 'R'),
  ('Interstellar',    'Sci-Fi',    169, 'PG-13'),
  ('The Dark Knight', 'Action',    152, 'PG-13'),
  ('Parasite',        'Thriller',  132, 'R'),
  ('Toy Story',       'Animation',  81, 'G'),
  ('Titanic',         'Romance',   195, 'PG-13'),
  ('Shutter Island',  'Mystery',   138, 'R');

INSERT INTO theater (theater_name, location) VALUES
  ('Central Cinema', 'Downtown'),
  ('Grand Theater',  'Uptown'),
  ('Riverside Plex', 'Riverside');

INSERT INTO showtime (movie_id, theater_id, show_date, start_time, end_time) VALUES
  (1, 1, '2025-05-15', '14:00:00', '16:30:00'),
  (2, 1, '2025-05-15', '17:00:00', '19:15:00'),
  (3, 3, '2025-05-16', '18:00:00', '20:30:00'),
  (8, 1, '2025-05-18', '10:00:00', '11:45:00'),
  (8, 2, '2025-05-18', '14:00:00', '15:45:00'),
  (9, 1, '2025-05-19', '12:00:00', '15:15:00'),
  (9, 3, '2025-05-19', '18:00:00', '21:15:00'),
  (10,2, '2025-05-20', '13:00:00', '15:18:00'),
  (10,4, '2025-05-20', '17:00:00', '19:18:00');

INSERT INTO seat (show_id, seat_number) VALUES
  (1, 'A1'), (1, 'A2'), (1, 'B1'),
  (8, 'A1'), (8, 'A2'),
  (9, 'A1'), (9, 'A2'),
  (10,'A1'),(10,'A2');
