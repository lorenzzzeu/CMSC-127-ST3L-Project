from system import count, get_id, get_input, validate_id

def food_item_menu(cur):
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
            add_food_item(cur)
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
        
def add_food_item(cur):
    food_id = get_id("Enter food item id: ", "food", "add", None, None, cur)
    food_name = get_input("Enter food name: ", "string", 1, 100, None, None)
    price = float(get_input("Enter price: ", "int", 1, 10, None, None))
    food_type = get_input("Enter food type: ", "string", 1, 100, None, None)
    user_id = get_id("Enter user ID: ", "food", "fetch", None, None, cur)
    establishment_id = get_id("Enter establishment ID: ", "food", "fetch", None, None, cur)
    query = "INSERT INTO FOOD_ITEM (food_id, food_name, price, type, user_id, establishment_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (food_id, food_name, price, food_type, user_id, establishment_id)
    cur.execute(query, values)
    
def delete_food_item(cur):
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
       
def update_food_item(cur):
    food_id = int(get_id("Enter food ID: ", "food", "fetch", None, None, cur))
    food_name = get_input("Enter new food name: ", "string", 1, 100, None, None)
    price = float(get_input("Enter new price: ", "int", 1, 10, None, None))
    food_type = get_input("Enter new food type: ", "string", 1, 100, None, None)
    query = "UPDATE FOOD_ITEM SET food_name = %s, price = %s, type = %s WHERE food_id = %s"
    values = (food_name, price, food_type, food_id)
    cur.execute(query, values)

# Display food items according to different choices
def display_all_food_items(cur):
    print("\n----------Display All Food Items----------")

    print("[1] View all food items from an establishment")
    print("[2] View all food items from an establishment that belong to a food type")
    print("[3] View all food items from an establishment arranged according to price")
    print("[4] View all food items with the same type")
    print("[5] View all food items based on a price range")
    print("[6] View all food items based on a price range that belong to the same food type")
    choice = get_input("\nEnter your choice: ", "int", 1, 6, None, None)

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

    result = cur.fetchall()

    for food_item in result:
        print(f"\nFood ID: {food_item[0]}")
        print(f"Food Name: {food_item[1]}")
        print(f"Price: {food_item[2]}")
        print(f"Food Type: {food_item[3]}")
        print(f"User ID: {food_item[4]}")
        print(f"Establishment ID: {food_item[5]}")    