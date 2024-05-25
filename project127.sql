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
    average_rating INT (1),
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
('Juan', 'Dela Cruz', 'Santos', '1990-05-15', 31, 'juan@example.com', 'password123', 'JuanDC', NULL, 'Filipino cuisine', 1, 1),
('Maria', 'Luna', 'Reyes', '1985-09-20', 36, 'maria@example.com', 'password456', 'MariaL', NULL, 'Japanese cuisine', 1, 1),
('Antonio', 'Garcia', 'Ramos', '1982-07-10', 39, 'antonio@example.com', 'password789', 'Tony', 'Bakery', 'Italian cuisine', 1, 1),
('Elena', 'Cruz', 'Lopez', '1995-03-25', 26, 'elena@example.com', 'passwordabc', 'Ellie', 'Coffee shop', 'Korean cuisine', 1, 1),
('Pedro', NULL, 'Gonzales', '1998-11-08', 23, 'pedro@example.com', 'passworddef', 'Pedring', 'Fast food', 'Chinese cuisine', 1, 1);

INSERT INTO USER_ADDRESS (user_id, address)
VALUES 
(1, '123 Main Street, Makati City'),
(2, '456 Maple Avenue, Quezon City'),
(3, '789 Oak Street, Taguig City'),
(4, '101 Pine Road, Pasig City'),
(5, '202 Elm Lane, Manila');

INSERT INTO USER_CONTACT (user_id, contact_number)
VALUES
-- Inserting dummy data into USER_CONTACT table
(1, '1234567890'),
(2, '0987654321'),
(3, '1112223333'),
(4, '4445556666'),
(5, '7778889999');

-- Inserting dummy data into FOOD_ESTABLISHMENT table
INSERT INTO FOOD_ESTABLISHMENT (establishment_name, date_established, location, opening_hour, user_id)
VALUES 
('Juan''s Grill', '2020-01-10', 'Makati City', '08:00:00', 1),
('Tokyo Ramen House', '2018-05-20', 'Quezon City', '11:00:00', 2),
('Tony''s Bakery', '2015-11-03', 'Taguig City', '06:30:00', 3),
('Ellie''s Cafe', '2019-09-15', 'Pasig City', '07:00:00', 4),
('Pedring''s Burger Joint', '2022-03-01', 'Manila', '10:30:00', 5);

-- Inserting dummy data into FOOD_ESTABLISHMENT_CONTACT table
INSERT INTO FOOD_ESTABLISHMENT_CONTACT (establishment_id, establishment_contact_number)
VALUES 
(1, '1111111111'),
(2, '2222222222'),
(3, '3333333333'),
(4, '4444444444'),
(5, '5555555555');

-- Inserting dummy data into FOOD_ESTABLISHMENT_SOCIAL table
INSERT INTO FOOD_ESTABLISHMENT_SOCIAL (establishment_id, social_media_link)
VALUES 
(1, 'https://www.facebook.com/juansgrill'),
(2, 'https://www.instagram.com/tokyoramenshop'),
(3, 'https://www.facebook.com/tonysbakery'),
(4, 'https://www.instagram.com/elliescafe'),
(5, 'https://www.facebook.com/pedringsburgers');

-- Inserting dummy data into FOOD_ITEM table
INSERT INTO FOOD_ITEM (food_name, price, type, user_id, establishment_id)
VALUES 
('Adobo', 200.00, 'Main Dish', 1, 1),
('Tonkotsu Ramen', 300.00, 'Noodles', 2, 2),
('Pandesal', 5.00, 'Bread', 3, 3),
('Cappuccino', 120.00, 'Beverage', 4, 4),
('Cheeseburger', 150.00, 'Burger', 5, 5);

-- Inserting dummy data into REVIEW table
INSERT INTO REVIEW (comment, rating, content, year, day, month, average_rating, service, ambience, cleanliness, taste, texture, plating, classification, user_id, establishment_id, food_id)
VALUES 
('Great food and service!', 5, 'The restaurant ambiance is cozy and inviting. Their dishes are delicious and well-prepared.', 2024, 25, 5, 5, 5, 4, 5, 5, 5, 5, 'Positive', 1, 1, 1),
('Average experience', 3, 'The food was decent, but the service could be improved. The place was clean.', 2024, 18, 5, 3, 3, 4, 4, 3, 4, 3, 'Neutral', 2, 2, 2),
('Delicious food!', 4, 'The food was amazing! I loved the flavors and presentation.', 2024, 10, 5, 4, 5, 5, 5, 5, 5, 5, 'Positive', 3, 3, 3),
('Disappointing experience', 2, 'The food was not up to expectations. Service was slow and the place was messy.', 2024, 5, 5, 2, 2, 2, 2, 3, 2, 2, 'Negative', 4, 4, 4),
('Fast and convenient', 4, 'Quick service and tasty food. Perfect for a quick meal.', 2024, 2, 5, 4, 4, 3, 4, 4, 4, 4, 'Positive', 5, 5, 5);
