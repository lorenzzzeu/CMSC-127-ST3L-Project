# Food Reviews Information System
# CMSC 127 Final Project

## Description
This information system allows users to record, in electronic form, data on food reviews and food items from food establishments.

## Team Members
- Lorenz Gabriel
- Dan Victor Gapaz
- Gian Carlo Suarez
- Dirk Ablanque <br/>

<br/>**Section:** ST3L

## Features
- Add, update, and delete a food review (on a food establishment or a food item)
- Add, delete, search, and update a food establishment
- Add, delete, search, and update a food item

## Reports
- View all food establishments
- View all food reviews for an establishment or a food item
- View all food items from an establishment
- View all food items from an establishment that belong to a food type (meat, veg, etc.)
- View all reviews made within a month for an establishment or a food item
- View all establishments with a high average rating (rating >= 4) (ratings from 1-5; highest is 5)
- View all food items from an establishment arranged according to price
- Search food items from any establishment based on a given price range and/or food type

## Setup
1. Clone the repository to your local machine.
2. Open your MariaDB client and connect to your local MariaDB server.3. Input 'mysql -u root -p' in the terminal.
4. Input your MariaDB password.
5. Run or source the SQL script `project127.sql` that is in root folder of this app to create the necessary database and table (dummy values).
6. If you are using VS Code, you may simply run tha 'main.py' file.
7. If you want to run it in your terminal, you may input to your terminal 'python3 main.py'. Make sure you have the necessary files and python dependencies.

## Technologies Used
- MariaDB
- Python3
- Pip/Tk*