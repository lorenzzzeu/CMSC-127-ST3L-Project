import mariadb

# Initialize database/connection
def init():
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
            CONSTRAINT FoodEstablishmentContact_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id)
        );
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS FOOD_ESTABLISHMENT_SOCIAL (
            establishment_id INT(3),
            social_media_link VARCHAR(250),
            CONSTRAINT FoodEstablishmentSocial_SocialMediaLink_pk PRIMARY KEY (social_media_link),
            CONSTRAINT FoodEstablishmentSocial_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id)
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
            CONSTRAINT FoodItem_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id)
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
            CONSTRAINT Review_EstablishmentId_fk FOREIGN KEY (establishment_id) REFERENCES FOOD_ESTABLISHMENT(establishment_id),
            CONSTRAINT Review_FoodId_fk FOREIGN KEY (food_id) REFERENCES FOOD_ITEM(food_id)
        );
    ''')

########################################################

print("\nFood Establishment and Food Review System")
init()