from system import count, get_id, get_input, validate_id
from datetime import datetime
# from main import init
import os

import mariadb

# import functionalities for establishment
from establishment import establishment_menu

# REVIEWS --------------------------
def add_review(cur):
    review_id = get_id("Enter review ID: ", "review", "add", None, None, cur)
    comment = get_input("Enter comment: ", "string", 1, 250, None, None)
    rating = int(get_input("Enter rating (1-5): ", "int", 1, 5, None, None))
    content = get_input("Enter content: ", "string", 1, 1000, None, None)
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    average_rating = rating
    service = int(get_input("Enter service rating (1-5): ", "int", 1, 5, None, None))
    ambience = int(get_input("Enter ambience rating (1-5): ", "int", 1, 5, None, None))
    cleanliness = int(get_input("Enter cleanliness rating (1-5): ", "int", 1, 5, None, None))
    taste = int(get_input("Enter taste rating (1-5): ", "int", 1, 5, None, None))
    texture = int(get_input("Enter texture rating (1-5): ", "int", 1, 5, None, None))
    plating = int(get_input("Enter plating rating (1-5): ", "int", 1, 5, None, None))
    classification = get_input("Enter classification: ", "string", 1, 100, None, None)
    user_id = int(get_id("Enter user ID: ", "user", "fetch", None, None, cur))
    establishment_id = get_id("Enter establishment ID (or 0 if reviewing a food item): ", "establishment", "fetch", None, None, cur)
    food_id = get_id("Enter food ID (or 0 if reviewing an establishment): ", "food", "fetch", None, None, cur)

    query = "INSERT INTO REVIEW (review_id, comment, rating, content, year, month, day, average_rating, service, ambience, cleanliness, taste, texture, plating, classification, user_id, establishment_id, food_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (review_id, comment, rating, content, year, month, day, average_rating, service, ambience, cleanliness, taste, texture, plating, classification, user_id, establishment_id, food_id)
    cur.execute(query, values)


def view_review(cur):
    choice = get_input("Enter '1' to view reviews for an establishment or '2' to view reviews for a food item (0 to exit): ", "int", 0, 2, None, None)
    if choice == 1:
        establishment_id = get_id("Enter the establishment ID: ", "establishment","fetch", None, None, cur)
        query = "SELECT * FROM REVIEW WHERE establishment_id = %s"
        cur.execute(query, (establishment_id,))
    elif choice == 2:
        food_id = get_id("Enter the food item ID: ", "food","fetch", None, None, cur)
        query = "SELECT * FROM REVIEW WHERE food_id = %s"
        cur.execute(query, (food_id,))
    elif choice == 0:
        return
    else:
        print("Invalid choice")
        return

    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No reviews found")

# NOT YET IMPLEMENTED
def view_reviews_within_month():
    choice = get_input("Enter 'e' to view reviews for an establishment or 'f' to view reviews for a food item: ")
    if choice == 'e':
        establishment_id = int(get_input("Enter establishment ID: "))
        query = "SELECT * FROM REVIEW WHERE establishment_id = %s AND month = %s"
        values = (establishment_id, datetime.now().month)
    elif choice == 'f':
        food_id = int(get_input("Enter food ID: "))
        query = "SELECT * FROM REVIEW WHERE food_id = %s AND month = %s"
        values = (food_id, datetime.now().month)
    else:
        print("Invalid choice")
        return

    cur.execute(query, values)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No reviews found for this month")

def update_review(cur):
    review_id = int(get_id("Enter review ID: ", "review", "fetch", None, None, cur))
    rating = int(get_input("Enter new rating (1-5): ", "int", 1, 5, None, None))
    comment = get_input("Enter new comment: ", "string", 1, 250, None, None)
    content = get_input("Enter new content: ", "string", 1, 1000, None, None)
    service = int(get_input("Enter new service rating (1-5): ", "int", 1, 5, None, None))
    ambience = int(get_input("Enter new ambience rating (1-5): ", "int", 1, 5, None, None))
    cleanliness = int(get_input("Enter new cleanliness rating (1-5): ", "int", 1, 5, None, None))
    taste = int(get_input("Enter new taste rating (1-5): ", "int", 1, 5, None, None))
    texture = int(get_input("Enter new texture rating (1-5): ", "int", 1, 5, None, None))
    plating = int(get_input("Enter new plating rating (1-5): ", "int", 1, 5, None, None))
    classification = get_input("Enter new classification: ", "string", 1, 100, None, None)
    user_id = int(get_id("Enter new user ID: ", "user", "fetch", None, None, cur)) #hindi ata to kailangan(?) since ung user na nag input lng non ung pwede magpalit. or dapat pala may validation dito to check if yung user na nag bigay ng revview ang maguupdate
    establishment_id = get_id("Enter new establishment ID (or 0 if reviewing a food item): ", "establishment", "fetch", None, None, cur)   
    food_id = int(get_id("Enter new food ID (or 0 if reviewing an establishment): ", "user","fetch", None, None, cur))

    query = "UPDATE REVIEW SET rating = %s, comment = %s, content = %s, service = %s, ambience = %s, cleanliness = %s, taste = %s, texture = %s, plating = %s, classification = %s, user_id = %s, establishment_id = %s, food_id = %s WHERE review_id = %s"
    values = (rating, comment, content, service, ambience, cleanliness, taste, texture, plating, classification, user_id, establishment_id, food_id, review_id)
    cur.execute(query, values)


def delete_review(cur):
    review_id = int(get_id("Enter review ID: ", "review", "fetch", None, None, cur))
    query = "DELETE FROM REVIEW WHERE review_id = %s"
    cur.execute(query, (review_id,))


def add_food_item():
    food_id = get_id("FOOD_ITEM")
    food_name = get_input("Enter food name: ")
    price = float(get_input("Enter price: "))
    food_type = get_input("Enter food type: ")
    user_id = int(get_input("Enter user ID: "))
    establishment_id = int(get_input("Enter establishment ID: "))
    query = "INSERT INTO FOOD_ITEM (food_id, food_name, price, type, user_id, establishment_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (food_id, food_name, price, food_type, user_id, establishment_id)
    cur.execute(query, values)

def delete_food_item():
    food_id = int(get_input("Enter food ID: "))
    query = "DELETE FROM FOOD_ITEM WHERE food_id = %s"
    cur.execute(query, (food_id,))

def search_food_item():
    search_term = get_input("Enter search term: ")
    query = "SELECT * FROM FOOD_ITEM WHERE food_name LIKE %s OR type LIKE %s"
    values = (f"%{search_term}%", f"%{search_term}%")
    cur.execute(query, values)
    for row in cur:
        print(row)

def update_food_item():
    food_id = int(get_input("Enter food ID: "))
    field = get_input("Enter field to update (food_name, price, type): ")
    new_value = get_input(f"Enter new value for {field}: ")
    query = f"UPDATE FOOD_ITEM SET {field} = %s WHERE food_id = %s"
    values = (new_value, food_id)
    cur.execute(query, values)

# Main Menu
def MainMenu():
    print("\n----------Main Menu----------")
    print("[1] Food Establishment")
    print("[2] Food Item")
    print("[3] Food Reviews")
    print("[0] Exit")

    choice = get_input("\nEnter your choice: ", "int", 0, 3, None, None)
    return choice


# Menu for reviews
def review_menu(cur): 
    print("\nFood Establishment and Food Review System")

    while True:
        print(f"\n----------Reviews----------")
        print("[1] View Reviews for a Food Establishment or Item")
        print("[2] Add a Review")
        print("[3] Edit a Review")
        print("[4] Delete a Review")
        print("[0] Back to Menu")
        print("-----------------------")
        choice = get_input("\nEnter your choice: ", "int", 0, 4, None, None)

        if choice == 1:
            print("\n-> Viewing reviews for a food establishment or item")
            view_review(cur)
        elif choice == 2:
            print("\n-> Adding a review")
            add_review(cur)
        elif choice == 3:
            print("\n-> Editing a review")
            update_review(cur)
        elif choice == 4:
            print("\n-> Deleting a review")
            delete_review(cur)
        elif choice == 0: break

    return



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


while True:
    choice = MainMenu()
     
    if choice == 1:
        print("\n-> Food Establishment")
        #function for establishment
        establishment_menu(cur)
    elif choice == 2:
        print("\n-> Food Item")
        #function for review
    elif choice == 3:
        print("\n-> Reviews")
        review_menu(cur)
        
    elif choice == 0: 
        print("Goodbye!")
        break