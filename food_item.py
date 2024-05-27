from system import count, get_id, get_input, validate_id

# Menu for Food Item
def food_item_menu(cur):
    #ask muna kung sino yung user para malaman kung owner ba siya. Owner lang ang pwede mag add
    user_id = get_id("Enter user ID: ", "user", "fetch", None, None, cur)
    #check if user is an owner
    query = "SELECT is_owner FROM User WHERE user_id = %s"
    cur.execute(query, (user_id,))
    
    is_owner = cur.fetchone()[0]
    print(is_owner)

    if (is_owner) == 1:
        while True:
            print(f"\n----------Food Item----------")
            print("[1] Search Food Item")
            print("[2] Add a Food Item")
            print("[3] Edit a Food Item")
            print("[4] Delete a Food Item")
            print("[5] Display all Food Items")
            print("[0] Back to Menu")
            print("-----------------------")
            choice = get_input("\nEnter your choice: ", "int", 0, 5, None, None)

            if choice == 1:
                print("\n-> Viewing a food item")
                search_food_item(cur)
            elif choice == 2:
                print("\n-> Adding a food item")
                add_food_item(cur, user_id)
            elif choice == 3:
                print("\n-> Editing a food item")
                update_food_item(cur)
            elif choice == 4:
                print("\n-> Deleting a food item")
                delete_food_item(cur)
            elif choice == 5:
                print("\n-> Viewing all food item")
                display_all_food_items(cur)   
            elif choice == 0: break

        return
    else:
        while True:
            print(f"\n----------Food Item----------")
            print("[1] Search Food Item")
            print("[2] Display all Food Items")
            print("[0] Back to Menu")
            print("-----------------------")
            choice = get_input("\nEnter your choice: ", "int", 0, 2, None, None)

            if choice == 1:
                print("\n-> Viewing a food item")
                search_food_item(cur)
            elif choice == 2:
                print("\n-> Viewing all food item")
                display_all_food_items(cur)   
            elif choice == 0: break

        return

# Add a Food Item      
def add_food_item(cur, user_id):
    #Ask for food estabs, to check if may access siya mag add doon sa food establishment
    establishment_id = get_id("Enter establishment ID: ", "food", "fetch", None, None, cur)
    query = "SELECT user_id FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
    cur.execute(query, (establishment_id,))

    owner_of_food_estab = cur.fetchone()[0]
    if(user_id != owner_of_food_estab):
        print("You do not have access to this food establishment. You can only add food items to your own food establishment.")
        return

    #ask for food details !!tinanggal ko na si food_id since auto increment naman, hayaan na siguro na mag generate yung program para di hassle sa admin
    food_name = get_input("Enter food name: ", "string", 1, 100, None, None)
    price = float(get_input("Enter price: ", "int", 1, 9999, None, None))
    food_type = get_input("Enter food type: ", "string", 1, 100, None, None)
    query = "INSERT INTO FOOD_ITEM ( food_name, price, type, user_id, establishment_id) VALUES ( %s, %s, %s, %s, %s)"
    values = ( food_name, price, food_type, user_id, establishment_id)
    cur.execute(query, values)

# Delete a Food Item
def delete_food_item(cur): # Need pa lagyan ng checker if yung user na yun yung may ari nung review
    food_id = int(get_id("Enter food ID: ", "food", "fetch", None, None, cur))
    query = "DELETE FROM FOOD_ITEM WHERE food_id = %s"
    cur.execute(query, (food_id,))       

def search_food_item(cur):
    # Search food item based on the name and food type
    search_term = get_input("Enter search term: ", "string", 1, 100, None, None)

    query = "SELECT * FROM FOOD_ITEM WHERE food_name LIKE %s OR type LIKE %s"
    values = (f"%{search_term}%", f"%{search_term}%")

    cur.execute(query, values)
    for row in cur:
        print(row) 
       
def update_food_item(cur): # Need pa lagyan ng checker if yung user na yun yung may ari nung review
    food_id = int(get_id("Enter food ID: ", "food", "fetch", None, None, cur))
    food_name = get_input("Enter new food name: ", "string", 1, 100, None, None)
    price = float(get_input("Enter new price: ", "int", 1, 10, None, None))
    food_type = get_input("Enter new food type: ", "string", 1, 100, None, None)
    query = "UPDATE FOOD_ITEM SET food_name = %s, price = %s, type = %s WHERE food_id = %s"
    values = (food_name, price, food_type, food_id)
    cur.execute(query, values)

# Display food items according to different choices
def display_all_food_items(cur):
    while True:
        print("\n----------Display All Food Items----------")

        print("[1] View all food items from an establishment")
        print("[2] View all food items from an establishment that belong to a food type")
        print("[3] View all food items from an establishment arranged according to price")
        print("[4] View all food items with the same type")
        print("[5] View all food items based on a price range")
        print("[6] View all food items based on a price range that belong to the same food type")
        print("[0] Back to Menu")
        choice = get_input("\nEnter your choice: ", "int", 0, 6, None, None)

        if choice == 1:
            establishment_id = get_id("Enter establishment ID: ", "food", "fetch", None, None, cur)
            query = f"SELECT * FROM FOOD_ITEM WHERE establishment_id = {establishment_id}"
            cur.execute(query)

        elif choice == 2:
            establishment_id = get_id("Enter establishment ID: ", "food", "fetch", None, None, cur)
            food_type = get_input("Enter food type: ", "string", 1, 100, None, None)
            query = "SELECT * FROM FOOD_ITEM WHERE establishment_id = %s AND type = %s"
            values = (establishment_id, food_type)
            cur.execute(query, values)

        elif choice == 3:
            sort = get_input("\nSort By Price (Descending or Ascending): ", "string", 1, 100, None, None)
            if sort.lower() == "ascending":
                query = "SELECT * FROM FOOD_ITEM ORDER BY price ASC"
            else:
                query = "SELECT * FROM FOOD_ITEM ORDER BY price DESC"
            cur.execute(query)

        elif choice == 4:
            food_type = get_input("Enter food type: ", "string", 1, 100, None, None)
            query = "SELECT * FROM FOOD_ITEM WHERE type = %s"
            cur.execute(query, (food_type,))

        elif choice == 5:
            search_price_min = float(get_input("Enter minimum food item price: ", "int", 1, 10, None, None))
            search_price_max = float(get_input("Enter maximum food item price: ", "int", 1, 10, None, None))

            query_price = "SELECT * FROM FOOD_ITEM WHERE price BETWEEN %s AND %s"
            price_values = (search_price_min, search_price_max)
            
            cur.execute(query_price, price_values)

        elif choice == 6:
            search_price_min = float(get_input("Enter minimum food item price: ", "int", 1, 10, None, None))
            search_price_max = float(get_input("Enter maximum food item price: ", "int", 1, 10, None, None))
            food_type = get_input("Enter food type: ", "string", 1, 100, None, None)
            query = "SELECT * FROM FOOD_ITEM WHERE price BETWEEN %s AND %s AND type = %s"
            values = (search_price_min, search_price_max, food_type)
            cur.execute(query, values)

        elif choice == 0:
            return

        result = cur.fetchall()

        for food_item in result:
            print(f"\nFood ID: {food_item[0]}")
            print(f"Food Name: {food_item[1]}")
            print(f"Price: {food_item[2]}")
            print(f"Food Type: {food_item[3]}")
            print(f"User ID: {food_item[4]}")
            print(f"Establishment ID: {food_item[5]}")    