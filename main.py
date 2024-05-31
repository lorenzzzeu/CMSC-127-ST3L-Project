from system import count, get_id, get_input, validate_id
from datetime import datetime
# from main import init
import os

import mariadb

# import functionalities for establishment
from establishment import establishment_menu
from food_item import food_item_menu
from review import review_menu


# Main Menu
def MainMenu():
    print("\n----------Main Menu----------")
    print("[1] Food Establishment")
    print("[2] Food Item")
    print("[3] Food Reviews")
    print("[0] Exit")

    choice = get_input("\nEnter your choice: ", "int", 0, 3, None, None)
    return choice


#################################

# Connect to MariaDB Platform
conn_bool = True
while conn_bool:
    mariadb_password = input("Enter password: ")

    try:
        conn = mariadb.connect(
            user = "root",
            password = mariadb_password,
            host = "localhost",
            autocommit = True
        )

        if(conn):
            conn_bool = False

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

# Get Cursor for DB functions
global cur 
cur = conn.cursor()

# Create database/tables on initial boot and use app database
cur.execute("CREATE DATABASE IF NOT EXISTS project127;")
cur.execute("USE project127;")
cur.execute('''
        CREATE TABLE IF NOT EXISTS USER (
            user_id INT (3) AUTO_INCREMENT,
            first_name VARCHAR(50) NOT NULL,
            middle_name VARCHAR(50),
            last_name VARCHAR(50),
            birthday DATE,
            age INT(2),
            email VARCHAR (50) NOT NULL,
            password VARCHAR(100),
            displayed_name VARCHAR(100),
            type_of_food_establishment_owned VARCHAR(100), 
            food_preference VARCHAR(50), 
            is_owner BOOLEAN,
            is_customer BOOLEAN,
            CONSTRAINT User_UserId_pk PRIMARY KEY (user_id)
        );
    ''')
cur.execute('''
      CREATE TABLE IF NOT EXISTS USER_ADDRESS (
          user_id INT(3),
          address VARCHAR(200),
          CONSTRAINT useraddress_address_pk PRIMARY KEY (address),
          CONSTRAINT useraddress_userid_fk FOREIGN KEY (user_id) REFERENCES USER (user_id)
      )
  ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS USER_CONTACT (
        user_id INT(3),
        contact_number VARCHAR(20),
        CONSTRAINT usercontact_contactnumber_pk PRIMARY KEY (contact_number),
        CONSTRAINT usercontact_userid_fk FOREIGN KEY (user_id) REFERENCES USER (user_id)
    )
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS FOOD_ESTABLISHMENT (
        establishment_id INT (3),
        establishment_name VARCHAR(100),
        date_established DATE,
        location VARCHAR(200),
        opening_hour TIME,
        user_id INT (3),
        CONSTRAINT FoodEstablishment_EstablishmentId_pk PRIMARY KEY(establishment_id),
        CONSTRAINT FoodEstablishment_UserId_fk FOREIGN KEY (User_id) REFERENCES USER(user_id)
    );
''')
cur.execute('''
      CREATE TABLE IF NOT EXISTS FOOD_ESTABLISHMENT_CONTACT (
          establishment_id INT(3),
          establishment_contact_number VARCHAR(20),
          CONSTRAINT FoodEstablishmentContact_EstablishmentContactNumber_pk PRIMARY KEY (establishment_contact_number),
          CONSTRAINT FoodEstablishmentContact_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id) ON DELETE CASCADE
      );
  ''')
cur.execute('''
      CREATE TABLE IF NOT EXISTS FOOD_ESTABLISHMENT_SOCIAL (
          establishment_id INT(3),
          social_media_link VARCHAR(250),
          CONSTRAINT FoodEstablishmentSocial_SocialMediaLink_pk PRIMARY KEY (social_media_link),
          CONSTRAINT FoodEstablishmentSocial_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id) ON DELETE CASCADE
      );
  ''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS FOOD_ITEM (
        food_id INT(3),
        food_name VARCHAR(100),
        price DECIMAL(10,2),
        type VARCHAR(100),
        user_id INT (3),
        establishment_id INT (3),
        CONSTRAINT FoodItem_FoodId_pk PRIMARY KEY (food_id),
        CONSTRAINT FoodItem_UserId_fk FOREIGN KEY (user_id) REFERENCES USER(user_id),
        CONSTRAINT FoodItem_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id) ON DELETE CASCADE
    );
''')
cur.execute('''
    CREATE TABLE IF NOT EXISTS REVIEW (
        review_id INT(5),
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
        user_id INT (3),
        establishment_id INT(3),
        food_id INT(3),
        CONSTRAINT Review_ReviewId_pk PRIMARY KEY (review_id),
        CONSTRAINT Review_UserId_fk FOREIGN KEY (user_id) REFERENCES USER (user_id),
        CONSTRAINT Review_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id) ON DELETE CASCADE,
        CONSTRAINT Review_FoodId_fk FOREIGN KEY (food_id) REFERENCES FOOD_ITEM(food_id) ON DELETE CASCADE
    );
''')

user_id = get_id("Enter user ID: ", "user", "fetch", None, None, cur)

while True:
    choice = MainMenu()
     
    if choice == 1:
        print("\n-> Food Establishment")
        #function for establishment
        establishment_menu(cur, user_id)
    elif choice == 2:
        print("\n-> Food Item")
        food_item_menu(cur, user_id)
    elif choice == 3:
        print("\n-> Reviews")
        review_menu(cur, user_id)
        
    elif choice == 0: 
        print("Goodbye!")
        break