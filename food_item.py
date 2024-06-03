from system import count, get_id, get_input, validate_id
import customtkinter as ctk
from tkinter import messagebox

# Menu for Food Item
def food_item_menu(cur, user_id, parent):
    #ask muna kung sino yung user para malaman kung owner ba siya. Owner lang ang pwede mag add
    food_item_menu_window = ctk.CTkToplevel(parent)
    food_item_menu_window.title("establishment menu ")
    food_item_menu_window.geometry("300x600")

    def back_to_main_menu():
        food_item_menu_window.destroy()

    ctk.CTkLabel(food_item_menu_window, text="Food Item Menu").pack(pady=10)
    
    #check if user is an owner
    query = "SELECT is_owner, is_customer FROM User WHERE user_id = %s"
    cur.execute(query, (user_id,))
    
    userType = cur.fetchone()

    if ((userType[0] == 1 and userType[1] == 1) or userType[0] == 1):
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
                update_food_item(cur, user_id)
            elif choice == 4:
                print("\n-> Deleting a food item")
                delete_food_item(cur, user_id)
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
    while True:
        #Ask for food estabs, to check if may access siya mag add doon sa food establishment
        establishment_id = get_id("Enter establishment ID: ", "establishment", "fetch", None, None, cur)
        query = "SELECT user_id FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
        cur.execute(query, (establishment_id,))

        owner_of_food_estab = cur.fetchone()[0]
        if(user_id != owner_of_food_estab):
            print("You do not have access to this food establishment. You can only add food items to your own food establishment.")
            continue

        cur.execute("SELECT MAX(food_id) FROM FOOD_ITEM")
        new_increment = cur.fetchone()[0]

        alter_query = "ALTER TABLE FOOD_ITEM AUTO_INCREMENT = %s"
        cur.execute(alter_query, (new_increment,))

        #ask for food details !!tinanggal ko na si food_id since auto increment naman, hayaan na siguro na mag generate yung program para di hassle sa admin
        food_name = get_input("Enter food name: ", "string", 1, 100, None, None)
        price = float(get_input("Enter price: ", "int", 1, 9999, None, None))
        food_type = get_input("Enter food type: ", "string", 1, 100, None, None)
        query = "INSERT INTO FOOD_ITEM ( food_name, price, type, user_id, establishment_id) VALUES ( %s, %s, %s, %s, %s)"
        values = (food_name, price, food_type, user_id, establishment_id)
        cur.execute(query, values)

        break
    return

# Delete a Food Item
def delete_food_item(cur, user_id): # lagyan ng checker if yung user na yun yung may ari nung review
    while True:

        food_id = int(get_id("Enter food ID: ", "food", "fetch", None, None, cur))
        query = "SELECT user_id FROM FOOD_ITEM WHERE food_id = %s"
        cur.execute(query, (food_id,))

        owner_of_food_item = cur.fetchone()[0]
        
        if(user_id != owner_of_food_item):
            print("You can't delete this food item added by another user.")
            continue

        query = "DELETE FROM FOOD_ITEM WHERE food_id = %s"
        cur.execute(query, (food_id,))    

        break

    return   

def search_food_item(cur):
    # Search food item based on the name and food type
    search_term = get_input("Enter search term: ", "string", 1, 100, None, None)

    query = "SELECT * FROM FOOD_ITEM WHERE food_name LIKE %s OR type LIKE %s"
    values = (f"%{search_term}%", f"%{search_term}%")

    cur.execute(query, values)
    
    result = cur.fetchall()
    if result:
        for food_item in result:
            print(f"\nFood ID: {food_item[0]}")
            print(f"Food Name: {food_item[1]}")
            print(f"Price: {food_item[2]}")
            print(f"Food Type: {food_item[3]}")
    else:
        print("\nThere is no food item with this type")
       
def update_food_item(cur, user_id): # Need pa lagyan ng checker if yung user na yun yung may ari nung review
    while True:

        food_id = int(get_id("Enter food ID: ", "food", "fetch", None, None, cur))
        query = "SELECT user_id FROM FOOD_ITEM WHERE food_id = %s"
        cur.execute(query, (food_id,))

        owner_of_food_item = cur.fetchone()[0]
        
        if(user_id != owner_of_food_item):
            print("\nYou can't update this food item added by another user.")
            return

        food_name = get_input("Enter new food name: ", "string", 1, 100, None, None)
        price = float(get_input("Enter new price: ", "int", 1, 999, None, None))
        food_type = get_input("Enter new food type: ", "string", 1, 100, None, None)
        query = "UPDATE FOOD_ITEM SET food_name = %s, price = %s, type = %s WHERE food_id = %s AND user_id = %s"
        values = (food_name, price, food_type, food_id, user_id)
        cur.execute(query, values)

        break

    return

# Display food items according to different choices
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
            establishment_id = get_id("Enter establishment ID: ", "establishment", "fetch", None, None, cur)
            establishment_name_query = "SELECT establishment_name FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
            cur.execute(establishment_name_query, (establishment_id,))
            establishment_name = cur.fetchone()[0]
            

            query = "SELECT * FROM FOOD_ITEM WHERE establishment_id = %s"
            cur.execute(query, (establishment_id,))

            result = cur.fetchall()

            # Check if there are no results and print a message
            if not result:
                print("No food items found for the given criteria.")
            else:
                print(f"\nEstablishment ID: {establishment_id}")
                print(f"Establishment Name: {establishment_name}")
                for food_item in result:
                    print(f"\nFood ID: {food_item[0]}")
                    print(f"Food Name: {food_item[1]}")
                    print(f"Price: {food_item[2]}")
                    print(f"Food Type: {food_item[3]}")
                    print(f"User ID: {food_item[4]}")

        elif choice == 2:
            establishment_id = get_id("Enter establishment ID: ", "establishment", "fetch", None, None, cur)
            food_type = get_input("Enter food type: ", "string", 1, 100, None, None)

            establishment_name_query = "SELECT establishment_name FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
            cur.execute(establishment_name_query, (establishment_id,))
            establishment_name = cur.fetchone()[0]
            

            query = "SELECT * FROM FOOD_ITEM WHERE establishment_id = %s AND type = %s"
            cur.execute(query, (establishment_id, food_type))

            result = cur.fetchall()

             # Check if there are no results and print a message
            if not result:
                print("No food items found for the given criteria.")
            else:
                print(f"\nEstablishment ID: {establishment_id}")
                print(f"Establishment Name: {establishment_name}")
                print(f"Food Type: {food_type}")
                for food_item in result:
                    print(f"\nFood ID: {food_item[0]}")
                    print(f"Food Name: {food_item[1]}")
                    print(f"Price: {food_item[2]}")
                    print(f"User ID: {food_item[4]}")

        elif choice == 3:
            sort = get_input("\nSort By Price (Descending or Ascending): ", "string", 1, 100, None, None)
            establishment_id = get_id("Enter establishment ID: ", "establishment", "fetch", None, None, cur)

            establishment_name_query = "SELECT establishment_name FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
            cur.execute(establishment_name_query, (establishment_id,))
            establishment_name = cur.fetchone()[0]
            

            if sort.lower() == "ascending":
                query = "SELECT * FROM FOOD_ITEM WHERE establishment_id = %s ORDER BY price ASC"
            elif sort.lower() == "descending":
                query = "SELECT * FROM FOOD_ITEM WHERE establishment_id = %s ORDER BY price DESC"
            cur.execute(query, (establishment_id,))

            result = cur.fetchall()

             # Check if there are no results and print a message
            if not result:
                print("No food items found for the given criteria.")
            else:
                print(f"\nEstablishment ID: {establishment_id}")
                print(f"Establishment Name: {establishment_name}")
                print(f"Sort Type: {sort}")
                for food_item in result:
                    print(f"\nFood ID: {food_item[0]}")
                    print(f"Food Name: {food_item[1]}")
                    print(f"Price: {food_item[2]}")
                    print(f"Food Type: {food_item[3]}")
                    print(f"User ID: {food_item[4]}")

        elif choice == 4:
            food_type = get_input("Enter food type: ", "string", 1, 100, None, None)

            establishment_query = "SELECT establishment_id, establishment_name FROM FOOD_ESTABLISHMENT"
            cur.execute(establishment_query)
            establishments = {row[0]: row[1] for row in cur.fetchall()}


            query = "SELECT * FROM FOOD_ITEM WHERE type = %s ORDER BY establishment_id"
            cur.execute(query, (food_type,))
            result = cur.fetchall()
            current_establishment_id = None
            

            if not result:
                print("No food items found for the given criteria.")
            else:
                print(f"\nFood Type: {food_type}")

                for food_item in result:

                    if food_item[5] != current_establishment_id:
                        current_establishment_id = food_item[5]
                        print('-'*50)
                        print(f"\nEstablishment ID: {current_establishment_id}")
                        print(f"Establishment Name: {establishments[current_establishment_id]}")

                    
                    print(f"\nFood ID: {food_item[0]}")
                    print(f"Food Name: {food_item[1]}")
                    print(f"Price: {food_item[2]}")
                    print(f"User ID: {food_item[4]}")


        elif choice == 5:
            establishment_id = get_id("Enter establishment ID: ", "establishment", "fetch", None, None, cur)
            establishment_name_query = "SELECT establishment_name FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
            cur.execute(establishment_name_query, (establishment_id,))
            establishment_name = cur.fetchone()[0]

            search_price_min = float(get_input("Enter minimum food item price: ", "int", 1, 999999, None, None))
            search_price_max = float(get_input("Enter maximum food item price: ", "int", 1, 999999, None, None))

            query_price = "SELECT * FROM FOOD_ITEM WHERE price BETWEEN %s AND %s ORDER BY price ASC"
            price_values = (search_price_min, search_price_max)
            cur.execute(query_price, price_values)

            result = cur.fetchall()

            # Check if there are no results and print a message
            if not result:
                print("No food items found for the given criteria.")
            else:
                for food_item in result:
                    print(f"\nFood ID: {food_item[0]}")
                    print(f"Food Name: {food_item[1]}")
                    print(f"Price: {food_item[2]}")
                    print(f"Food Type: {food_item[3]}")
                    print(f"User ID: {food_item[4]}")
                    print(f"Establishment ID: {food_item[5]}")
                    print(f"Establishment Name: {establishment_name}")

        elif choice == 6:
            establishment_id = get_id("Enter establishment ID: ", "establishment", "fetch", None, None, cur)
            establishment_name_query = "SELECT establishment_name FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
            cur.execute(establishment_name_query, (establishment_id,))
            establishment_name = cur.fetchone()[0]
            
            food_type = get_input("Enter food type: ", "string", 1, 100, None, None)
            search_price_min = float(get_input("Enter minimum food item price: ", "int", 1, 999999, None, None))
            search_price_max = float(get_input("Enter maximum food item price: ", "int", 1, 999999, None, None))

            query = """
                SELECT * FROM FOOD_ITEM 
                WHERE price BETWEEN %s AND %s AND type = %s 
                ORDER BY price ASC
            """
            values = (search_price_min, search_price_max, food_type)
            cur.execute(query, values)

            result = cur.fetchall()

            # Check if there are no results and print a message
            if not result:
                print("No food items found for the given criteria.")
            else:
                for food_item in result:
                    print(f"\nFood ID: {food_item[0]}")
                    print(f"Food Name: {food_item[1]}")
                    print(f"Price: {food_item[2]}")
                    print(f"Food Type: {food_item[3]}")
                    print(f"User ID: {food_item[4]}")
                    print(f"Establishment ID: {food_item[5]}")
                    print(f"Establishment Name: {establishment_name}")

        elif choice == 0:
            return
        


        