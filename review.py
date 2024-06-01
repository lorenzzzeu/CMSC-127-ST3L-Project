from system import count, get_id, get_input, validate_id
from datetime import datetime

# Menu for reviews
def review_menu(cur, user_id): 
    print("\nFood Establishment and Food Review System")

    #check if user is an owner
    query = "SELECT is_owner FROM User WHERE user_id = %s"
    cur.execute(query, (user_id,))
    
    is_owner = cur.fetchone()[0]

    if (is_owner) == 1:
        while True:
            print(f"\n----------Reviews----------")
            print("[1] View Reviews for a Food Establishment or Item")
            print("[0] Back to Menu")
            print("-----------------------")
            choice = get_input("\nEnter your choice: ", "int", 0, 1, None, None)

            if choice == 1:
                print("\n-> Viewing reviews for a food establishment or item")
                view_review(cur)
            elif choice == 0: break

        return
    else:
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
                add_review(cur, user_id)
            elif choice == 3:
                print("\n-> Editing a review")
                update_review(cur, user_id)
            elif choice == 4:
                print("\n-> Deleting a review")
                delete_review(cur, user_id)
            elif choice == 0: break

        return

# REVIEWS --------------------------
def add_review(cur, user_id):
    choice = get_input("\nAre you providing a review for an Establishment or a Food Item? (Press 1 for Establishment; Press 2 for Food Item): ", "int", 1, 2, None, None)

    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day

    service = None
    ambience = None
    cleanliness = None
    plating = None
    taste = None
    texture = None
    establishment_id = None
    food_id = None
    classification = None

    cur.execute("SELECT MAX(review_id) FROM REVIEW")
    new_increment = cur.fetchone()[0]

    alter_query = "ALTER TABLE REVIEW AUTO_INCREMENT = %s"
    cur.execute(alter_query, (new_increment,))
    
    if choice == 1:
        cur.execute("SELECT establishment_id, establishment_name FROM FOOD_ESTABLISHMENT")
        food_items = cur.fetchall()

        if food_items:
            print("\nList of Food Establishments")
            for item in food_items:
                print(f"Establishment ID: {item[0]}")
                print(f"Establishment Name: {item[1]}\n")
        else:
            print("\nNo food establishments available.")

        establishment_id = get_id("Enter establishment ID: ", "establishment", "fetch", None, None, cur)
        comment = get_input("Enter comment: ", "string", 1, 250, None, None)
        content = get_input("Enter content: ", "string", 1, 1000, None, None)
        rating = int(get_input("Enter rating (1-5): ", "int", 1, 5, None, None))
        service = int(get_input("Enter service rating (1-5): ", "int", 1, 5, None, None))
        ambience = int(get_input("Enter ambience rating (1-5): ", "int", 1, 5, None, None))
        cleanliness = int(get_input("Enter cleanliness rating (1-5): ", "int", 1, 5, None, None))
        classification = "Food Establishment"

    elif choice == 2:
        cur.execute("SELECT food_id, food_name, establishment_name FROM FOOD_ITEM NATURAL JOIN FOOD_ESTABLISHMENT")
        food_items = cur.fetchall()

        if food_items:
            print("\nList of Food Items")
            for item in food_items:
                print(f"Food ID: {item[0]}")
                print(f"Food Name: {item[1]}")
                print(f"Establishment Name: {item[2]}\n")
        else:
            print("\nNo food items available.")

        food_id = get_id("Enter food ID: ", "food", "fetch", None, None, cur)
        comment = get_input("Enter comment: ", "string", 1, 250, None, None)
        content = get_input("Enter content: ", "string", 1, 1000, None, None)
        rating = int(get_input("Enter rating (1-5): ", "int", 1, 5, None, None))
        taste = int(get_input("Enter taste rating (1-5): ", "int", 1, 5, None, None))
        texture = int(get_input("Enter texture rating (1-5): ", "int", 1, 5, None, None))
        plating = int(get_input("Enter plating rating (1-5): ", "int", 1, 5, None, None))
        classification = "Food Item"
        
    query = "INSERT INTO REVIEW (comment, rating, content, year, month, day, service, ambience, cleanliness, taste, texture, plating, classification, user_id, establishment_id, food_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    values = (comment, rating, content, year, month, day, service, ambience, cleanliness, taste, texture, plating, classification, user_id, establishment_id, food_id)
    cur.execute(query, values)


def view_review(cur):
    while True:
        print("\n----------Display a Review----------")
        print("[1] View Reviews for a Food Establishment or Item")
        print("[2] View Reviews for a Food Establishment or Item within a month")
        print("[0] Back to Menu")
        choice = get_input("\nEnter your choice: ", "int", 0, 2, None, None)

        if choice == 1:
            review_choice = get_input("Enter '1' to view reviews for an establishment or '2' to view reviews for a food item (0 to exit): ", "int", 0, 2, None, None)
            if review_choice == 1:
                establishment_id = get_id("Enter the establishment ID: ", "establishment","fetch", None, None, cur)
                query = "SELECT * FROM REVIEW WHERE establishment_id = %s"
                cur.execute(query, (establishment_id,))
            elif review_choice == 2:
                food_id = get_id("Enter the food item ID: ", "food","fetch", None, None, cur)
                query = "SELECT * FROM REVIEW WHERE food_id = %s"
                cur.execute(query, (food_id,))
            elif review_choice == 0:
                return

            rows = cur.fetchall()
            if rows:
                for row in rows:
                    print("Review:")
                    print("Review ID:", row[0])
                    print("User ID:", row[15])
                    print("Comment:", row[1])
                    print("Rating:", row[2])
                    print("Content:", row[3])
                    print("Year:", row[4])
                    print("Day:", row[5])
                    print("Month:", row[6])
                    print("Classification:", row[14])
                    
                    # Print attributes based on classification
                    if row[14] == "Food Establishment":
                        print("Service Rating:", row[7])
                        print("Ambience Rating:", row[8])
                        print("Cleanliness Rating:", row[9])
                    elif row[14] == "Food Item":
                        print("Taste Rating:", row[10])
                        print("Texture Rating:", row[11])
                        print("Plating Rating:", row[12])
                        
                    # Print Establishment ID or Food ID if not None
                    if row[16] is not None:
                        print("Establishment ID:", row[16])
                    if row[17] is not None:
                        print("Food ID:", row[17])
            else:
                print("No reviews found")

        elif choice == 2:
            while True:
                month_review_choice = get_input("Enter 'e' to view reviews for an establishment or 'f' to view reviews for a food item: ", "string", 1, 1, None, None)
                if month_review_choice == 'e':
                    establishment_id = get_id("Enter the establishment ID: ", "establishment","fetch", None, None, cur)
                    query = "SELECT * FROM REVIEW WHERE establishment_id = %s AND month = %s"
                    values = (establishment_id, datetime.now().month)
                elif month_review_choice == 'f':
                    food_id = get_id("Enter the food item ID: ", "food","fetch", None, None, cur)
                    query = "SELECT * FROM REVIEW WHERE food_id = %s AND month = %s"
                    values = (food_id, datetime.now().month)
                else:
                    print("Invalid choice")
                    continue

                cur.execute(query, values)
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print("Review:")
                        print("Review ID:", row[0])
                        print("User ID:", row[15])
                        print("Comment:", row[1])
                        print("Rating:", row[2])
                        print("Content:", row[3])
                        print("Year:", row[4])
                        print("Day:", row[5])
                        print("Month:", row[6])
                        print("Classification:", row[14])
                        
                        # Print attributes based on classification
                        if row[14] == "Food Establishment":
                            print("Service Rating:", row[7])
                            print("Ambience Rating:", row[8])
                            print("Cleanliness Rating:", row[9])
                        elif row[14] == "Food Item":
                            print("Taste Rating:", row[10])
                            print("Texture Rating:", row[11])
                            print("Plating Rating:", row[12])
                            
                        # Print Establishment ID or Food ID if not None
                        if row[16] is not None:
                            print("Establishment ID:", row[16])
                        if row[17] is not None:
                            print("Food ID:", row[17])
                else:
                    print("No reviews found for this month")

                return
        elif choice == 0:
            return

def update_review(cur, user_id): # lagyan ng checker if yung user na yun yung may ari nung review
    while True:
        review_id = int(get_id("Enter review ID: ", "review", "fetch", None, None, cur))

        query = "SELECT user_id FROM REVIEW WHERE review_id = %s"
        cur.execute(query, (review_id,))

        owner_of_review = cur.fetchone()[0]
        
        if(user_id != owner_of_review):
            print("You can't edit this review added by another user.")
            continue

        query = "SELECT classification FROM REVIEW WHERE review_id = %s"
        cur.execute(query, (review_id,))
        classification = cur.fetchone()

        classification = classification[0]

        service = None
        ambience = None
        cleanliness = None
        plating = None
        taste = None
        texture = None

        if classification == "Food Establishment":
            comment = get_input("Enter new comment: ", "string", 1, 250, None, None)
            content = get_input("Enter new content: ", "string", 1, 1000, None, None)
            rating = int(get_input("Enter new rating (1-5): ", "int", 1, 5, None, None))
            service = int(get_input("Enter new service rating (1-5): ", "int", 1, 5, None, None))
            ambience = int(get_input("Enter new ambience rating (1-5): ", "int", 1, 5, None, None))
            cleanliness = int(get_input("Enter new cleanliness rating (1-5): ", "int", 1, 5, None, None))

        elif classification == "Food Item":
            comment = get_input("Enter new comment: ", "string", 1, 250, None, None)
            content = get_input("Enter new content: ", "string", 1, 1000, None, None)
            rating = int(get_input("Enter new rating (1-5): ", "int", 1, 5, None, None))
            taste = int(get_input("Enter new taste rating (1-5): ", "int", 1, 5, None, None))
            texture = int(get_input("Enter new texture rating (1-5): ", "int", 1, 5, None, None))
            plating = int(get_input("Enter new plating rating (1-5): ", "int", 1, 5, None, None))

        # user_id = int(get_id("Enter new user ID: ", "user", "fetch", None, None, cur)) #hindi ata to kailangan(?) since ung user na nag input lng non ung pwede magpalit. or dapat pala may validation dito to check if yung user na nag bigay ng revview ang maguupdate

        query = "UPDATE REVIEW SET rating = %s, comment = %s, content = %s, service = %s, ambience = %s, cleanliness = %s, taste = %s, texture = %s, plating = %s WHERE review_id = %s AND user_id = %s"
        values = (rating, comment, content, service, ambience, cleanliness, taste, texture, plating, review_id, user_id)
        cur.execute(query, values)

        break

    return

def delete_review(cur, user_id): # Need pa lagyan ng checker if yung user na yun yung may ari nung review
    while True:
        review_id = int(get_id("Enter review ID: ", "review", "fetch", None, None, cur))

        query = "SELECT user_id FROM REVIEW WHERE review_id = %s"
        cur.execute(query, (review_id,))

        owner_of_review = cur.fetchone()[0]
        
        if(user_id != owner_of_review):
            print("You can't delete this review added by another user.")
            continue

        query = "DELETE FROM REVIEW WHERE review_id = %s AND user_id = %s"
        cur.execute(query, (review_id, user_id))

        break
        
    return