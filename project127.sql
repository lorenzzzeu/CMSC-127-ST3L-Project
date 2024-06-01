DROP DATABASE IF EXISTS project127;
CREATE DATABASE IF NOT EXISTS project127;
USE project127;

-- User Table
CREATE TABLE IF NOT EXISTS USER (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    middle_name VARCHAR(50),
    last_name VARCHAR(50),
    birthday DATE,
    age INT(2),
    email VARCHAR(50) NOT NULL,
    password VARCHAR(100),
    displayed_name VARCHAR(100),
    type_of_food_establishment_owned VARCHAR(100), 
    food_preference VARCHAR(50), 
    is_owner BOOLEAN,
    is_customer BOOLEAN
);

CREATE TABLE IF NOT EXISTS USER_ADDRESS (
    address_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    address VARCHAR(200),
    CONSTRAINT useraddress_userid_fk FOREIGN KEY (user_id) REFERENCES USER (user_id)
);

CREATE TABLE IF NOT EXISTS USER_CONTACT (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    contact_number VARCHAR(20),
    CONSTRAINT usercontact_userid_fk FOREIGN KEY (user_id) REFERENCES USER (user_id)
);

CREATE TABLE IF NOT EXISTS FOOD_ESTABLISHMENT (
    establishment_id INT AUTO_INCREMENT PRIMARY KEY,
    establishment_name VARCHAR(100),
    date_established DATE,
    location VARCHAR(200),
    opening_hour TIME,
    user_id INT,
    CONSTRAINT FoodEstablishment_UserId_fk FOREIGN KEY (user_id) REFERENCES USER(user_id)
);

CREATE TABLE IF NOT EXISTS FOOD_ESTABLISHMENT_CONTACT (
    establishment_contact_id INT AUTO_INCREMENT PRIMARY KEY,
    establishment_id INT,
    establishment_contact_number VARCHAR(20),
    CONSTRAINT FoodEstablishmentContact_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS FOOD_ESTABLISHMENT_SOCIAL (
    establishment_social_id INT AUTO_INCREMENT PRIMARY KEY,
    establishment_id INT,
    social_media_link VARCHAR(250),
    CONSTRAINT FoodEstablishmentSocial_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS FOOD_ITEM (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    food_name VARCHAR(100),
    price DECIMAL(10,2),
    type VARCHAR(100),
    user_id INT,
    establishment_id INT,
    CONSTRAINT FoodItem_UserId_fk FOREIGN KEY (user_id) REFERENCES USER(user_id),
    CONSTRAINT FoodItem_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS REVIEW (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    comment VARCHAR (250),
    rating INT (2), 
    content TEXT,
    year YEAR,
    day INT (2),
    month INT (2),
    service INT (1),
    ambience  INT (1),
    cleanliness  INT (1),
    taste  INT (1),
    texture  INT (1),
    plating  INT (1),
    classification VARCHAR(100),
    user_id INT,
    establishment_id INT,
    food_id INT,
    CONSTRAINT Review_UserId_fk FOREIGN KEY (user_id) REFERENCES USER (user_id),
    CONSTRAINT Review_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id) ON DELETE CASCADE,
    CONSTRAINT Review_FoodId_fk FOREIGN KEY (food_id) REFERENCES FOOD_ITEM(food_id) ON DELETE CASCADE
);

-- Inserting dummy data
INSERT INTO USER (first_name, middle_name, last_name, birthday, age, email, password, displayed_name, type_of_food_establishment_owned, food_preference, is_owner, is_customer) 
VALUES 
('Juan', 'Dela Cruz', 'Santos', '1990-05-15', 31, 'juan@example.com', PASSWORD('password123'), 'JuanDC', 'Restaurant', NULL, 1, 0),
('Maria', 'Luna', 'Reyes', '1985-09-20', 36, 'maria@example.com', PASSWORD('password456'), 'MariaL', 'Restaurant', NULL, 1, 0),
('Antonio', 'Garcia', 'Ramos', '1982-07-10', 39, 'antonio@example.com', PASSWORD('password789'), 'Tony', NULL, 'Italian cuisine', 0, 1),
('Elena', 'Cruz', 'Lopez', '1995-03-25', 26, 'elena@example.com', PASSWORD('passwordabc'), 'Ellie', NULL, 'Korean cuisine', 0, 1),
('Pedro', NULL, 'Gonzales', '1998-11-08', 23, 'pedro@example.com', PASSWORD('passworddef'), 'Pedring', NULL, 'Chinese cuisine', 0, 1),
('Lorenz', 'Gomez', 'Gabriel', '2004-02-14', 20, 'lorenz@example.com', PASSWORD('passwordlg'), 'Lorenz', 'Restaurant', NULL, 1, 0),
('Dan Victor', NULL, 'Gapaz', '2003-04-20', 21, 'dan@example.com', PASSWORD('passworddg'), 'Dan', 'Fastfood', NULL, 1, 0),
('Gian Carlo', NULL, 'Suarez', '2003-06-11', 20, 'gian@example.com', PASSWORD('passwordgs'), 'Gian', NULL, 'Korean cuisine', 0, 1),
('Dirk', NULL, 'Ablanque', '2003-01-01', 21, 'dirk@example.com', PASSWORD('passwordda'), 'Dirk', NULL, 'Japanese cuisine', 0, 1),
('Iska', 'Oble', 'Komsay', '2000-11-15', 23, 'iska@example.com', PASSWORD('passwordik'), 'IskaK', NULL, 'Filipino cuisine', 0, 1);

INSERT INTO USER_ADDRESS (user_id, address)
VALUES 
(1, '123 Main Street, Makati City'),
(2, '456 Maple Avenue, Quezon City'),
(3, '789 Oak Street, Taguig City'),
(4, '101 Pine Road, Pasig City'),
(5, '202 Elm Lane, Manila'),
(6, '15 Faculty, Taguig City'),
(7, '42 Los Baños, Laguna'),
(8, '69 Tuktukan, Taguig City'),
(9, '101 Los Baños, Laguna'),
(10, '612 Intramuros, Manila');

INSERT INTO USER_CONTACT (user_id, contact_number)
VALUES
-- Inserting dummy data into USER_CONTACT table
(1, '1234567890'),
(2, '0987654321'),
(3, '1112223333'),
(4, '4445556666'),
(5, '7778889999'),
(6, '0214021402'),
(7, '0425876514'),
(8, '0611061106'),
(9, '0258464485'),
(10, '1122334455');

-- Inserting dummy data into FOOD_ESTABLISHMENT table
INSERT INTO FOOD_ESTABLISHMENT (establishment_name, date_established, location, opening_hour, user_id)
VALUES 
('Juan''s Grill', '2020-01-10', 'Makati City', '08:00:00', 1),
('Tokyo Ramen House', '2018-05-20', 'Quezon City', '11:00:00', 2),
('Sitio''s Bakery', '2015-11-03', 'Taguig City', '06:30:00', 2),
('Maria''s Cafe', '2019-09-15', 'Pasig City', '07:00:00', 2),
('Juan''s Burger Joint', '2022-03-01', 'Manila', '10:30:00', 1),
('Lorenz''s KayEfSi', '2022-02-14', 'Taguig City', '09:00:00', 6),
('Gabbo InSide Restaurant', '2018-09-10', 'Makati City', '12:00:00', 6),
('Donut Dunkin & Bakery', '2019-12-08', 'Taguig City', '06:00:00', 6),
('Tatang Dan''s Foodhouse', '2020-10-25', 'Laguna', '08:00:00', 7),
('Jabee', '2024-05-08', 'Laguna', '6:00:00', 7);

-- Inserting dummy data into FOOD_ESTABLISHMENT_CONTACT table
INSERT INTO FOOD_ESTABLISHMENT_CONTACT (establishment_id, establishment_contact_number)
VALUES 
(1, '1111111111'),
(2, '2222222222'),
(3, '3333333333'),
(4, '4444444444'),
(5, '5555555555'),
(6, '6666666666'),
(7, '7777777777'),
(8, '8888888888'),
(9, '9999999999'),
(10, '1010101010');

-- Inserting dummy data into FOOD_ESTABLISHMENT_SOCIAL table
INSERT INTO FOOD_ESTABLISHMENT_SOCIAL (establishment_id, social_media_link)
VALUES 
(1, 'https://www.facebook.com/juansgrill'),
(2, 'https://www.instagram.com/tokyoramenshop'),
(3, 'https://www.facebook.com/tonysbakery'),
(4, 'https://www.instagram.com/elliescafe'),
(5, 'https://www.facebook.com/pedringsburgers'),
(6, 'https://www.facebook.com/KayEfSi'),
(7, 'https://www.instagram.com/insideres'),
(8, 'https://www.facebook.com/sitiobakery'),
(9, 'https://www.instagram.com/tatangdan'),
(10, 'https://www.facebook.com/jabee');

-- Inserting dummy data into FOOD_ITEM table
INSERT INTO FOOD_ITEM (food_name, price, type, user_id, establishment_id)
VALUES 
('Adobo', 200.00, 'Main Dish', 1, 1),
('Tonkotsu Ramen', 300.00, 'Noodles', 2, 2),
('Pandesal', 5.00, 'Bread', 2, 3),
('Cappuccino', 120.00, 'Beverage', 2, 4),
('Cheeseburger', 150.00, 'Burger', 1, 5),
('Ultimate Steak KayEfSi Special', 180.00, 'Main Dish', 6, 6),
('Special Jjampong', 150.00, 'Noodles', 6, 7),
('Croissant', 50.00, 'Bread', 6, 8),
('Spaghetti', 30.00, 'Pasta', 7, 9),
('ChickenSaya', 99.00, 'Chicken', 7, 10);

-- Inserting dummy data into REVIEW table
INSERT INTO REVIEW (comment, rating, content, year, day, month, service, ambience, cleanliness, taste, texture, plating, classification, user_id, establishment_id, food_id)
VALUES 
('Great food and service!', 5, 'The restaurant ambiance is cozy and inviting. Their dishes are delicious and well-prepared.', 2024, 25, 5, 5, 4, 5, NULL, NULL, NULL, 'Food Establishment', 3, 1, NULL),
('Average food', 3, 'The food was decent, noodles are a bit soggy.', 2024, 18, 5, NULL, NULL, NULL, 3, 4, 3, 'Food Item', 4, NULL, 2),
('Great place!', 4, 'The food was decent, but the service is great. The place was clean.', 2024, 10, 5, 5, 5, 5, NULL, NULL, NULL, 'Food Establishment', 5, 3, NULL),
('Disappointing experience', 2, 'The food was not up to expectations. Food is almost raw.', 2024, 5, 5, NULL, NULL, NULL, 1, 2, 2, 'Food Item', 4, NULL, 4),
('Fast and convenient', 4, 'Quick service and tasty food. Perfect for a lovingly meal.', 2024, 2, 5, 4, 3, 4, NULL, NULL, NULL, 'Food Establishment', 5, 5, NULL);
