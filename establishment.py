#create a try catch or validation to check if the inputted establishment_id is already in the database

from system import count, get_id, get_input, validate_id

# Menu For Food Establishment
def establishment_menu(cur, user_id):
    print("\nFood Establishment and Food Review System")

    #check if user is an owner
    query = "SELECT is_owner, is_customer FROM User WHERE user_id = %s"
    cur.execute(query, (user_id,))
    
    userType = cur.fetchone()

    if ((userType[0] == 1 and userType[1] == 1) or userType[0] == 1):
        while True:
            print(f"\n----------Establishment----------")
            print("[1] Add an Establishment")
            print("[2] Delete an Establishment")
            print("[3] Search for an Establishment")
            print("[4] Update an Establishment")
            print("[5] Display all Establishments")
            print("[0] Back to Menu")
            print("-----------------------")
            choice = get_input("\nEnter your choice: ", "int", 0, 5, None, None)

            if choice == 1:
                print("\n-> Adding an establishment")
                add_establishment(cur, user_id)
            elif choice == 2:
                print("\n-> Deleting an establishment")
                delete_establishment(cur, user_id)
            elif choice == 3:
                print("\n-> Searching for an establishment")
                search_establishment(cur)
            elif choice == 4:
                print("\n-> Updating an establishment")
                update_establishment(cur, user_id)
            elif choice == 5:
                print("\n-> Displaying all establishments")
                display_all_establishments(cur)
            elif choice == 0: break

        return

    else:
        while True:
            print(f"\n----------Establishment----------")
            print("[1] Search for an Establishment")
            print("[2] Display all Establishments")
            print("[0] Back to Menu")
            print("-----------------------")
            choice = get_input("\nEnter your choice: ", "int", 0, 2, None, None)

            if choice == 1:
                print("\n-> Searching for an establishment")
                search_establishment(cur)
            elif choice == 2:
                print("\n-> Displaying all establishments")
                display_all_establishments(cur)
            elif choice == 0: break

        return
    

# Add an Establishment
def add_establishment(cur, user_id):
    print("\n----------Add Establishment----------")

    establishment_name = get_input("Enter Establishment Name: ", "string", 1, 75, None, None)
    date_established = get_input("Enter Date Established (YYYY-MM-DD): ", "date", 1, 75, None, None)
    location = get_input("Enter Location: ", "string", 1, 75, None, None)
    opening_hour = get_input("Enter Opening Hour (HH:MM:SS): ", "hour", 1, 8, None, None)

    contact = None
    social = None

    cur.execute("SELECT MAX(establishment_id) FROM FOOD_ESTABLISHMENT")
    new_increment = cur.fetchone()[0]

    alter_query = "ALTER TABLE FOOD_ESTABLISHMENT AUTO_INCREMENT = %s"
    cur.execute(alter_query, (new_increment,))

    # Insert into FOOD_ESTABLISHMENT table
    query = "INSERT INTO FOOD_ESTABLISHMENT (establishment_name, date_established, location, opening_hour, user_id) VALUES (%s, %s, %s, %s, %s)"
    values = (establishment_name, date_established, location, opening_hour, user_id)
    cur.execute(query, values)
    establishment_id = cur.lastrowid

    # For Contact Numbers
    contact_choice = get_input("Do you want to add your contact number? (Yes [1], No [2]): ", "int", 1, 2, None, None)

    if (contact_choice == 1):
        while True:
            contact = get_input("Enter Contact Number (09XXXXXXXXX): ", "contact", 1, 75, None, None)

            cur.execute("SELECT MAX(establishment_contact_id) FROM FOOD_ESTABLISHMENT_CONTACT")
            new_contact_increment = cur.fetchone()[0]

            alter_query = "ALTER TABLE FOOD_ESTABLISHMENT_CONTACT AUTO_INCREMENT = %s"
            cur.execute(alter_query, (new_contact_increment,))

            query_for_contact = "INSERT INTO FOOD_ESTABLISHMENT_CONTACT (establishment_id, establishment_contact_number) VALUES (%s, %s)"
            values_for_contact = (establishment_id, contact)
            cur.execute(query_for_contact, values_for_contact)

            another_choice = get_input("Do you want to add another contact number? (Yes [1], No [2]): ", "int", 1, 2, None, None)

            if (another_choice == 2): break

    # For Social Media Links
    social_choice = get_input("Do you want to add your social media link? (Yes [1], No [2]): ", "int", 1, 2, None, None)

    if (social_choice == 1):
        while True:
            social = get_input("Enter Social Media Link: ", "string", 1, 200, None, None)

            cur.execute("SELECT MAX(establishment_social_id) FROM FOOD_ESTABLISHMENT_SOCIAL")
            new_social_increment = cur.fetchone()[0]

            alter_query = "ALTER TABLE FOOD_ESTABLISHMENT_SOCIAL AUTO_INCREMENT = %s"
            cur.execute(alter_query, (new_social_increment,))

            query_for_social = "INSERT INTO FOOD_ESTABLISHMENT_SOCIAL (establishment_id, social_media_link) VALUES (%s, %s)"
            values_for_social = (establishment_id, social)
            cur.execute(query_for_social, values_for_social)

            another_choice = get_input("Do you want to add another social media link? (Yes [1], No [2]): ", "int", 1, 2, None, None)

            if (another_choice == 2): break


    print("\nEstablishment added successfully.")

# Delete an Establishment
def delete_establishment(cur, user_id):
    print("\n----------Delete Establishment----------")
    while True:

        establishment_id = int(get_id("Enter Establishment ID: ", "establishment", "fetch", None, None, cur))

        query = "SELECT user_id FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
        cur.execute(query, (establishment_id,))

        owner_of_food_establishment = cur.fetchone()[0]
        
        if(user_id != owner_of_food_establishment):
            print("You can't delete this food establishment added by another user.")
            continue

        #delete contact from food_establishment_contact
        query_contact_delete = "DELETE FROM FOOD_ESTABLISHMENT_CONTACT WHERE establishment_id = %s"
        cur.execute(query_contact_delete, (establishment_id,))

        #delete social from food_establishment_social
        query_social_delete = "DELETE FROM FOOD_ESTABLISHMENT_SOCIAL WHERE establishment_id = %s"
        cur.execute(query_social_delete, (establishment_id,))

        #delete establishment from food_establishment
        query = "DELETE FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
        values = (establishment_id,)
        cur.execute(query, values)

        print("Successfully deleted food establishment")
        break

    return

# Search for an Establishment
def search_establishment(cur):
    print("\n----------Search Establishment----------")
    search_option = get_input("Search by [1] Establishment ID or [2] Establishment Name: ", "int", 1, 2, None, None)

    if search_option == 1:
        establishment_id = int(get_id("Enter Establishment ID: ", "establishment", "fetch", None, None, cur))

        query = """
            SELECT fe.establishment_id, fe.establishment_name, fe.date_established, fe.location, fe.opening_hour, fe.user_id, 
                cn.establishment_contact_number, sm.social_media_link, AVG(rv.rating) as avg_rating
            FROM FOOD_ESTABLISHMENT fe
            LEFT JOIN FOOD_ESTABLISHMENT_CONTACT cn ON fe.establishment_id = cn.establishment_id
            LEFT JOIN FOOD_ESTABLISHMENT_SOCIAL sm ON fe.establishment_id = sm.establishment_id
            LEFT JOIN REVIEW rv ON fe.establishment_id = rv.establishment_id
            where fe.establishment_id = %s
            GROUP BY fe.establishment_id, cn.establishment_contact_number, sm.social_media_link
            ORDER BY fe.establishment_id
            """

        # query = "SELECT establishment_id, establishment_name, date_established, location, opening_hour, user_id,  (select establishment_contact_number from food_establishment_contact where establishment_id=fe.establishment_id) as contact_number  FROM FOOD_ESTABLISHMENT fe WHERE establishment_id = %s"
        cur.execute(query, (establishment_id,))
        result = cur.fetchall()

    elif search_option == 2:
        establishment_name = get_input("Enter partial or full Establishment Name: ", "string", 1, 75, None, None)
        
        query = """
            SELECT fe.establishment_id, fe.establishment_name, fe.date_established, fe.location, fe.opening_hour, fe.user_id, 
                cn.establishment_contact_number, sm.social_media_link, AVG(rv.rating) as avg_rating
            FROM FOOD_ESTABLISHMENT fe
            LEFT JOIN FOOD_ESTABLISHMENT_CONTACT cn ON fe.establishment_id = cn.establishment_id
            LEFT JOIN FOOD_ESTABLISHMENT_SOCIAL sm ON fe.establishment_id = sm.establishment_id
            LEFT JOIN REVIEW rv ON fe.establishment_id = rv.establishment_id
            where fe.establishment_name LIKE %s
            GROUP BY fe.establishment_id, cn.establishment_contact_number, sm.social_media_link
            ORDER BY fe.establishment_id
            """
        
        # query = "SELECT establishment_id, establishment_name, date_established, location, opening_hour, user_id,  (select establishment_contact_number from food_establishment_contact where establishment_id=%s) as contact_number FROM FOOD_ESTABLISHMENT WHERE establishment_name LIKE %s"
        cur.execute(query, (f'%{establishment_name}%',))
        result = cur.fetchall() #fetchall() is used because there can be multiple establishments with the same name in the table for contact and social media ilnks

    if result:
        if search_option == 1:
            establishments = {}
            for establishment in result:
                est_id = establishment[0]
                if est_id not in establishments:
                    establishments[est_id] = {
                        "name": establishment[1],
                        "date_established": establishment[2],
                        "location": establishment[3],
                        "opening_hour": establishment[4],
                        "user_id": establishment[5],
                        "establishment_contact_number": set(),
                        "social_media_links": set(),
                        "avg_rating": establishment[8]
                    }
                if establishment[6]:  # Check if contact number is not None
                    establishments[est_id]["establishment_contact_number"].add(establishment[6])
                if establishment[7]:  # Check if social media link is not None
                    establishments[est_id]["social_media_links"].add(establishment[7])
            for est_id, details in establishments.items():
                print(f"\nEstablishment ID: {est_id}")
                print(f"Establishment Name: {details['name']}")
                print(f"Date Established: {details['date_established']}")
                print(f"Location: {details['location']}")
                print(f"Opening Hour: {details['opening_hour']}")
                avg_rating = details['avg_rating']
                if avg_rating is not None:
                    print(f"Average Rating: {avg_rating:.2f}")
                else:
                    print("Average Rating: No reviews yet")
                print("Contact Numbers:")
                if not details['establishment_contact_number']:
                    print(" No contact numbers available")
                for index, number in enumerate(details['establishment_contact_number'], start=1):
                    print(f" {index}. {number}")
                print("Social Media Links:")
                if not details['social_media_links']:
                    print(" No social media links available")
                for index, link in enumerate(details['social_media_links'], start=1):
                    print(f" {index}. {link}")
                print(f"User ID: {details['user_id']}")

        elif search_option == 2:
            establishments = {}
            for establishment in result:
                est_id = establishment[0]
                if est_id not in establishments:
                    establishments[est_id] = {
                        "name": establishment[1],
                        "date_established": establishment[2],
                        "location": establishment[3],
                        "opening_hour": establishment[4],
                        "user_id": establishment[5],
                        "establishment_contact_number": set(),
                        "social_media_links": set(),
                        "avg_rating": establishment[8]
                    }
                if establishment[6]:  # Check if contact number is not None
                    establishments[est_id]["establishment_contact_number"].add(establishment[6])
                if establishment[7]:  # Check if social media link is not None
                    establishments[est_id]["social_media_links"].add(establishment[7])
            for est_id, details in establishments.items():
                print(f"\nEstablishment ID: {est_id}")
                print(f"Establishment Name: {details['name']}")
                print(f"Date Established: {details['date_established']}")
                print(f"Location: {details['location']}")
                print(f"Opening Hour: {details['opening_hour']}")
                avg_rating = details['avg_rating']
                if avg_rating is not None:
                    print(f"Average Rating: {avg_rating:.2f}")
                else:
                    print("Average Rating: No reviews yet")
                print("Contact Numbers:")
                if not details['establishment_contact_number']:
                    print(" No contact numbers available")
                for index, number in enumerate(details['establishment_contact_number'], start=1):
                    print(f" {index}. {number}")
                print("Social Media Links:")
                if not details['social_media_links']:
                    print(" No social media links available")
                for index, link in enumerate(details['social_media_links'], start=1):
                    print(f" {index}. {link}")
                print(f"User ID: {details['user_id']}")
           
    else:
        print("No establishment found matching the search criteria.")

# Update an establishment
def update_establishment(cur, user_id):
    print("\n----------Update Establishment----------")
    while True:

        establishment_id = int(get_id("Enter Establishment ID: ", "establishment", "fetch", None, None, cur))
        
        query = "SELECT user_id FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
        cur.execute(query, (establishment_id,))

        owner_of_food_establishment = cur.fetchone()[0]
        

        if(user_id != owner_of_food_establishment):
            print("You can't edit this food establishment added by another user.")
            continue

        query = "SELECT establishment_id, establishment_name, date_established, location, opening_hour, user_id FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
        cur.execute(query, (establishment_id,))
        result = cur.fetchone()

        if result:
            print(f"\nEstablishment ID: {result[0]}")
            print(f"Establishment Name: {result[1]}")
            print(f"Date Established: {result[2]}")
            print(f"Location: {result[3]}")
            print(f"Opening Hour: {result[4]}")
            print(f"User ID: {result[5]}")

            establishment_name = get_input("Enter new Establishment Name: ", "string", 1, 75, None, None)
            date_established = get_input("Enter new Date Established (YYYY-MM-DD): ", "date", 1, 75, None, None)
            location = get_input("Enter new Location: ", "string", 1, 75, None, None)
            opening_hour = get_input("Enter new Opening Hour (HH:MM:SS): ", "hour", 1, 75, None, None)
            
            query = "SELECT establishment_contact_number FROM FOOD_ESTABLISHMENT_CONTACT WHERE establishment_id = %s"
            cur.execute(query, (establishment_id,))
            result = cur.fetchone()[0]
            
            if result:
                print(f"\nYour current contact number is/are : ")
                for number in result:
                    print(f" {number}")
                contact_choice = get_input("Do you want to update your contact number? (Yes [1], No [2]): ", "int", 1, 2, None, None)
            else:
                print("\nYou currently don't have a contact number")
                contact_choice = get_input("Do you want to add your contact number? (Yes [1], No [2]): ", "int", 1, 2, None, None)

            if (contact_choice == 1):
                contact = get_input("Enter Contact Number: (09XXXXXXXXX)", "contact", 1, 75, None, None)

                query_for_contact = "UPDATE FOOD_ESTABLISHMENT_CONTACT SET establishment_contact_number = %s WHERE establishment_id = %s"
                values_for_contact = (contact, establishment_id)
                cur.execute(query_for_contact, values_for_contact)

            query = "SELECT social_media_link FROM FOOD_ESTABLISHMENT_SOCIAL WHERE establishment_id = %s"
            cur.execute(query, (establishment_id,))
            result = cur.fetchone()[0]
            
            if result:
                print(f"\nYour current social media link is : {result}")
                social_choice = get_input("Do you want to update your social media link? (Yes [1], No [2]): ", "int", 1, 2, None, None)
            else:
                print("\nYou currently don't have a social media link")
                social_choice = get_input("Do you want to add your social media link? (Yes [1], No [2]): ", "int", 1, 2, None, None)
            
            if (social_choice == 1):
                social = get_input("Enter Social Media: ", "string", 1, 200, None, None)

                query_for_social = "UPDATE FOOD_ESTABLISHMENT_SOCIAL SET social_media_link = %s WHERE establishment_id = %s"
                values_for_social = (social, establishment_id)
                cur.execute(query_for_social, values_for_social)

            query = "UPDATE FOOD_ESTABLISHMENT SET establishment_name = %s, date_established = %s, location = %s, opening_hour = %s, user_id = %s WHERE establishment_id = %s"
            values = (establishment_name, date_established, location, opening_hour, user_id, establishment_id)
            cur.execute(query, values)

            break
    return
        

# View all establishments
def display_all_establishments(cur):
    while True:
        print("\n----------Display All Establishments----------")
        print("[1] View all establishments")
        print("[2] View all establishments with a high average rating (rating >= 4)")
        print("[0] Back to Menu")
        choice = get_input("\nEnter your choice: ", "int", 0, 2, None, None)

        if choice == 1:
            query = """
            SELECT fe.establishment_id, fe.establishment_name, fe.date_established, fe.location, fe.opening_hour, fe.user_id, 
                cn.establishment_contact_number, sm.social_media_link, AVG(rv.rating) as avg_rating
            FROM FOOD_ESTABLISHMENT fe
            LEFT JOIN FOOD_ESTABLISHMENT_CONTACT cn ON fe.establishment_id = cn.establishment_id
            LEFT JOIN FOOD_ESTABLISHMENT_SOCIAL sm ON fe.establishment_id = sm.establishment_id
            LEFT JOIN REVIEW rv ON fe.establishment_id = rv.establishment_id
            GROUP BY fe.establishment_id, cn.establishment_contact_number, sm.social_media_link
            ORDER BY fe.establishment_id
            """
            cur.execute(query)

        elif choice == 2:
            query = """
            SELECT fe.establishment_id, fe.establishment_name, fe.date_established, fe.location, fe.opening_hour, fe.user_id, 
                cn.establishment_contact_number, sm.social_media_link, AVG(rv.rating) as avg_rating
            FROM FOOD_ESTABLISHMENT fe
            LEFT JOIN FOOD_ESTABLISHMENT_CONTACT cn ON fe.establishment_id = cn.establishment_id
            LEFT JOIN FOOD_ESTABLISHMENT_SOCIAL sm ON fe.establishment_id = sm.establishment_id
            LEFT JOIN REVIEW rv ON fe.establishment_id = rv.establishment_id
            GROUP BY fe.establishment_id, cn.establishment_contact_number, sm.social_media_link
            HAVING avg_rating >= 4
            ORDER BY fe.establishment_id
            """
            cur.execute(query)
        
        elif choice == 0: return

        result = cur.fetchall()

        if not result:
            print("No food establishments found for the given criteria.")
        else:
            establishments = {}
            for establishment in result:
                est_id = establishment[0]
                if est_id not in establishments:
                    establishments[est_id] = {
                        "name": establishment[1],
                        "date_established": establishment[2],
                        "location": establishment[3],
                        "opening_hour": establishment[4],
                        "user_id": establishment[5],
                        "establishment_contact_number": set(),
                        "social_media_links": set(),
                        "avg_rating": establishment[8]
                    }
                if establishment[6]:  # Check if contact number is not None
                    establishments[est_id]["establishment_contact_number"].add(establishment[6])
                if establishment[7]:  # Check if social media link is not None
                    establishments[est_id]["social_media_links"].add(establishment[7])

            for est_id, details in establishments.items():
                print(f"\nEstablishment ID: {est_id}")
                print(f"Establishment Name: {details['name']}")
                print(f"Date Established: {details['date_established']}")
                print(f"Location: {details['location']}")
                print(f"Opening Hour: {details['opening_hour']}")
                avg_rating = details['avg_rating']
                if avg_rating is not None:
                    print(f"Average Rating: {avg_rating:.2f}")
                else:
                    print("Average Rating: No reviews yet")
                print("Contact Numbers:")
                if not details['establishment_contact_number']:
                    print(" No contact numbers available")
                for index, number in enumerate(details['establishment_contact_number'], start=1):
                    print(f" {index}. {number}")
                print("Social Media Links:")
                if not details['social_media_links']:
                    print(" No social media links available")
                for index, link in enumerate(details['social_media_links'], start=1):
                    print(f" {index}. {link}")
                print(f"User ID: {details['user_id']}")