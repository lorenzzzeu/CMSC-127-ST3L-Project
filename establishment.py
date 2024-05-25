#create a try catch or validation to check if the inputted establishment_id is already in the database

from system import count, get_id, get_input, validate_id

# Menu For Food Establishment
def establishment_menu(cur):
    print("\nFood Establishment and Food Review System")

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
            add_establishment(cur)
        elif choice == 2:
            print("\n-> Deleting an establishment")
            delete_establishment(cur)
        elif choice == 3:
            print("\n-> Searching for an establishment")
            search_establishment(cur)
        elif choice == 4:
            print("\n-> Updating an establishment")
            update_establishment(cur)
        elif choice == 5:
            print("\n-> Displaying all establishments")
            display_all_establishments(cur)
        elif choice == 0: break

    return


# Add an Establishment
def add_establishment(cur):
    print("\n----------Add Establishment----------")
    establishment_id = get_id("Enter Establishment ID: ", "establishment", "add", None, None, cur)
    establishment_name = get_input("Enter Establishment Name: ", "string", 1, 75, None, None)
    date_established = get_input("Enter Date Established (YYYY-MM-DD): ", "date", 1, 75, None, None)
    location = get_input("Enter Location: ", "string", 1, 75, None, None)
    opening_hour = get_input("Enter Opening Hour: ", "string", 1, 75, None, None)
    user_id = get_id("Enter User ID: ", "user", "fetch",None, None, cur)
    contact = get_input("Enter Contact Number: ", "string", 1, 75, None, None)
    social = get_input("Enter Social Media: ", "string", 1, 200, None, None)

    query = "INSERT INTO FOOD_ESTABLISHMENT (establishment_id, establishment_name, date_established, location, opening_hour,user_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (establishment_id, establishment_name, date_established, location, opening_hour, user_id)
    cur.execute(query, values)  

    query_for_contact = "INSERT INTO FOOD_ESTABLISHMENT_CONTACT (establishment_id, establishment_contact_number) VALUES (%s, %s)"
    values_for_contact = (establishment_id, contact)
    cur.execute(query_for_contact, values_for_contact)

    query_for_social = "INSERT INTO FOOD_ESTABLISHMENT_SOCIAL (establishment_id, social_media_link) VALUES (%s, %s)"   
    values_for_social = (establishment_id, social)
    cur.execute(query_for_social, values_for_social)

# Delete an Establishment
def delete_establishment(cur):
    print("\n----------Delete Establishment----------")
    establishment_id = int(get_id("Enter Establishment ID: ", "establishment", "fetch", None, None, cur))

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

# Search for an Establishment
def search_establishment(cur):
    print("\n----------Search Establishment----------")
    establishment_id = int(get_id("Enter Establishment ID: ", "establishment", "fetch", None, None, cur))

    query = "SELECT establishment_id, establishment_name, date_established, location, opening_hour, user_id FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
    cur.execute(query, (establishment_id,))
    result = cur.fetchone()

    query_contact = "SELECT establishment_contact_number FROM FOOD_ESTABLISHMENT_CONTACT WHERE establishment_id = %s"
    cur.execute(query_contact, (establishment_id,))
    contact = cur.fetchone()

    query_social = "SELECT social_media_link FROM FOOD_ESTABLISHMENT_SOCIAL WHERE establishment_id = %s"
    cur.execute(query_social, (establishment_id,))
    social = cur.fetchone()

    if result:
        print(f"\nEstablishment ID: {result[0]}")
        print(f"Establishment Name: {result[1]}")
        print(f"Date Established: {result[2]}")
        print(f"Location: {result[3]}")
        print(f"Opening Hour: {result[4]}")
        print(f"User ID: {result[5]}")
        print(f"Contact Number: {contact[0]}")
        print(f"Social Media: {social[0]}")
    else:
        print("Establishment does not exist.")

# Update an establishment
def update_establishment(cur):
    print("\n----------Update Establishment----------")
    establishment_id = int(get_id("Enter Establishment ID: ", "establishment", "fetch", None, None, cur))

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

        establishment_name = get_input("Enter Establishment Name: ", "string", 1, 75, None, None)
        date_established = get_input("Enter Date Established (YYYY-MM-DD): ", "date", 1, 75, None, None)
        location = get_input("Enter Location: ", "string", 1, 75, None, None)
        opening_hour = get_input("Enter Opening Hour: ", "string", 1, 75, None, None)
        user_id = get_id("Enter User ID: ", "user", "fetch", None, None, cur)
        contact = get_input("Enter Contact Number: ", "string", 1, 75, None, None)
        social = get_input("Enter Social Media: ", "string", 1, 200, None, None)

        query = "UPDATE FOOD_ESTABLISHMENT SET establishment_name = %s, date_established = %s, location = %s, opening_hour = %s, user_id = %s WHERE establishment_id = %s"
        values = (establishment_name, date_established, location, opening_hour, user_id, establishment_id)
        cur.execute(query, values)

        query_for_contact = "UPDATE FOOD_ESTABLISHMENT_CONTACT SET establishment_contact_number = %s WHERE establishment_id = %s"
        values_for_contact = (contact, establishment_id)
        cur.execute(query_for_contact, values_for_contact)

        query_for_social = "UPDATE FOOD_ESTABLISHMENT_SOCIAL SET social_media_link = %s WHERE establishment_id = %s"
        values_for_social = (social, establishment_id)
        cur.execute(query_for_social, values_for_social)
        
# View all establishments
def display_all_establishments(cur):
    print("\n----------Display All Establishments----------")

    query = "SELECT establishment_id, establishment_name, date_established, location, opening_hour, user_id FROM FOOD_ESTABLISHMENT"
    cur.execute(query)
    result = cur.fetchall()

    for establishment in result:
        print(f"\nEstablishment ID: {establishment[0]}")
        print(f"Establishment Name: {establishment[1]}")
        print(f"Date Established: {establishment[2]}")
        print(f"Location: {establishment[3]}")
        print(f"Opening Hour: {establishment[4]}")
        print(f"User ID: {establishment[5]}")