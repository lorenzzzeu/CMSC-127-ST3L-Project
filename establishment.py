#create a try catch or validation to check if the inputted establishment_id is already in the database

from system import count, get_id, get_input, validate_id
import customtkinter as ctk
from tkinter import messagebox
#from main import open_main_menu

# Menu For Food Establishment
def establishment_menu(cur, user_id, parent):
    establishment_menu_window = ctk.CTkToplevel(parent)
    establishment_menu_window.title("establishment menu ")
    establishment_menu_window.geometry("300x600")

    def back_to_main_menu():
        establishment_menu_window.destroy()

    ctk.CTkLabel(establishment_menu_window, text="Establishment Menu").pack(pady=10)

    #check if user is an owner
    query = "SELECT is_owner, is_customer FROM User WHERE user_id = %s"
    cur.execute(query, (user_id,))
    
    userType = cur.fetchone()

    if ((userType[0] == 1 and userType[1] == 1) or userType[0] == 1):
        print(f"\n----------Establishment----------")
        print("[1] Add an Establishment")
        print("[2] Delete an Establishment")
        print("[3] Search for an Establishment")
        print("[4] Update an Establishment")
        print("[5] Display all Establishments")
        print("[0] Back to Menu")
        print("-----------------------")
        add_establishment = ctk.CTkButton(establishment_menu_window, text="[1] Add an Establishment", command=lambda: handle_menu_establishment(cur, user_id, 1))
        add_establishment.pack(pady=10)
        delete_establishment = ctk.CTkButton(establishment_menu_window, text="[2] Delete an Establishment", command=lambda: handle_menu_establishment(cur, user_id, 2))
        delete_establishment.pack(pady=10)
        search_establishment = ctk.CTkButton(establishment_menu_window, text="[3] Search for an Establishment", command=lambda: handle_menu_establishment(cur, user_id, 3))
        search_establishment.pack(pady=10)
        update_establishment = ctk.CTkButton(establishment_menu_window, text="[4] Update an Establishment", command=lambda: handle_menu_establishment(cur, user_id, 4))
        update_establishment.pack(pady=10)
        display_all_establishment = ctk.CTkButton(establishment_menu_window, text="[5] Display all Establishments", command=lambda: handle_menu_establishment(cur, user_id, 5))
        display_all_establishment.pack(pady=10)
        ctk.CTkButton(establishment_menu_window, text="Back to Main Menu", command=back_to_main_menu).pack(pady=5)

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


def handle_menu_establishment(cur, user_id, choice):
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
    #elif choice == 0: 


# Add an Establishment
def add_establishment(cur, user_id):
    add_establishment_window = ctk.CTkToplevel()
    add_establishment_window.title("add establishment window")
    add_establishment_window.geometry("300x200")
    print("\n----------Add Establishment----------")

    add_establishment_window = ctk.CTkToplevel()
    add_establishment_window.title("Add Establishment Window")
    add_establishment_window.geometry("400x600")

    scrollable_frame = ctk.CTkScrollableFrame(add_establishment_window, width=380, height=580)
    scrollable_frame.pack(pady=10, padx=10, fill="both", expand=True)

    establishment_name_label = ctk.CTkLabel(scrollable_frame, text="Enter Establishment Name:")
    establishment_name_label.pack(pady=5)
    establishment_name_entry = ctk.CTkEntry(scrollable_frame)
    establishment_name_entry.pack(pady=5)

    date_established_label = ctk.CTkLabel(scrollable_frame, text="Enter Date Established (YYYY-MM-DD):")
    date_established_label.pack(pady=5)
    date_established_entry = ctk.CTkEntry(scrollable_frame)
    date_established_entry.pack(pady=5)

    location_label = ctk.CTkLabel(scrollable_frame, text="Enter Location:")
    location_label.pack(pady=5)
    location_entry = ctk.CTkEntry(scrollable_frame)
    location_entry.pack(pady=5)

    opening_hour_label = ctk.CTkLabel(scrollable_frame, text="Enter Opening Hour (HH:MM:SS):")
    opening_hour_label.pack(pady=5)
    opening_hour_entry = ctk.CTkEntry(scrollable_frame)
    opening_hour_entry.pack(pady=5)

    contact_choice_label = ctk.CTkLabel(scrollable_frame, text="Do you want to add your contact number? (Yes [1], No [2]):")
    contact_choice_label.pack(pady=5)
    contact_choice_entry = ctk.CTkEntry(scrollable_frame)
    contact_choice_entry.pack(pady=5)

    contact_label = ctk.CTkLabel(scrollable_frame, text="Enter Contact Number (09XXXXXXXXX):")
    contact_label.pack(pady=5)
    contact_entry = ctk.CTkEntry(scrollable_frame)
    contact_entry.pack(pady=5)

    another_contact_choice_label = ctk.CTkLabel(scrollable_frame, text="Do you want to add another contact number? (Yes [1], No [2]):")
    another_contact_choice_label.pack(pady=5)
    another_contact_choice_entry = ctk.CTkEntry(scrollable_frame)
    another_contact_choice_entry.pack(pady=5)

    social_choice_label = ctk.CTkLabel(scrollable_frame, text="Do you want to add your social media link? (Yes [1], No [2]):")
    social_choice_label.pack(pady=5)
    social_choice_entry = ctk.CTkEntry(scrollable_frame)
    social_choice_entry.pack(pady=5)

    social_label = ctk.CTkLabel(scrollable_frame, text="Enter Social Media Link:")
    social_label.pack(pady=5)
    social_entry = ctk.CTkEntry(scrollable_frame)
    social_entry.pack(pady=5)

    another_social_choice_label = ctk.CTkLabel(scrollable_frame, text="Do you want to add another social media link? (Yes [1], No [2]):")
    another_social_choice_label.pack(pady=5)
    another_social_choice_entry = ctk.CTkEntry(scrollable_frame)
    another_social_choice_entry.pack(pady=5)

    def submit_establishment():
        establishment_name = get_input("Enter Establishment Name: ", "string", 1, 75, None, None)
        date_established = get_input("Enter Date Established (YYYY-MM-DD): ", "date", 1, 75, None, None)
        location = get_input("Enter Location: ", "string", 1, 75, None, None)
        opening_hour = get_input("Enter Opening Hour (HH:MM:SS): ", "hour", 1, 8, None, None)

        contact = None
        social = None

        cur.execute("SELECT MAX(establishment_id) FROM FOOD_ESTABLISHMENT")
        new_increment = cur.fetchone()[0] or 0

        alter_query = "ALTER TABLE FOOD_ESTABLISHMENT AUTO_INCREMENT = %s"
        cur.execute(alter_query, (new_increment,))

        query = "INSERT INTO FOOD_ESTABLISHMENT (establishment_name, date_established, location, opening_hour, user_id) VALUES (%s, %s, %s, %s, %s)"
        values = (establishment_name, date_established, location, opening_hour, user_id)
        cur.execute(query, values)
        establishment_id = cur.lastrowid

        add_contact_window(establishment_id)
        add_social_window(establishment_id)

        messagebox.showinfo("Success", "Establishment added successfully.")

    def add_contact_window(establishment_id):
        contact_window = ctk.CTkToplevel(add_establishment_window)
        contact_window.title("Add Contact Number")
        contact_window.geometry("400x300")

        contact_choice_label = ctk.CTkLabel(contact_window, text="Do you want to add your contact number? (Yes [1], No [2]):")
        contact_choice_label.pack(pady=5)
        contact_choice_entry = ctk.CTkEntry(contact_window)
        contact_choice_entry.pack(pady=5)

        contact_label = ctk.CTkLabel(contact_window, text="Enter Contact Number (09XXXXXXXXX):")
        contact_label.pack(pady=5)
        contact_entry = ctk.CTkEntry(contact_window)
        contact_entry.pack(pady=5)

        another_contact_choice_label = ctk.CTkLabel(contact_window, text="Do you want to add another contact number? (Yes [1], No [2]):")
        another_contact_choice_label.pack(pady=5)
        another_contact_choice_entry = ctk.CTkEntry(contact_window)
        another_contact_choice_entry.pack(pady=5)

        def submit_contact():
            contact_choice = get_input(contact_choice_entry, "int")
            if contact_choice == 1:
                while True:
                    contact = get_input(contact_entry, "contact")

                    cur.execute("SELECT MAX(establishment_contact_id) FROM FOOD_ESTABLISHMENT_CONTACT")
                    new_contact_increment = cur.fetchone()[0] or 0

                    alter_query = "ALTER TABLE FOOD_ESTABLISHMENT_CONTACT AUTO_INCREMENT = %s"
                    cur.execute(alter_query, (new_contact_increment,))

                    query_for_contact = "INSERT INTO FOOD_ESTABLISHMENT_CONTACT (establishment_id, establishment_contact_number) VALUES (%s, %s)"
                    values_for_contact = (establishment_id, contact)
                    cur.execute(query_for_contact, values_for_contact)

                    another_choice = get_input(another_contact_choice_entry, "int")
                    if another_choice == 2:
                        break

            contact_window.destroy()

        submit_button = ctk.CTkButton(contact_window, text="Submit Contact", command=submit_contact)
        submit_button.pack(pady=20)

    def add_social_window(establishment_id):
        social_window = ctk.CTkToplevel(add_establishment_window)
        social_window.title("Add Social Media Link")
        social_window.geometry("400x300")

        social_choice_label = ctk.CTkLabel(social_window, text="Do you want to add your social media link? (Yes [1], No [2]):")
        social_choice_label.pack(pady=5)
        social_choice_entry = ctk.CTkEntry(social_window)
        social_choice_entry.pack(pady=5)

        social_label = ctk.CTkLabel(social_window, text="Enter Social Media Link:")
        social_label.pack(pady=5)
        social_entry = ctk.CTkEntry(social_window)
        social_entry.pack(pady=5)

        another_social_choice_label = ctk.CTkLabel(social_window, text="Do you want to add another social media link? (Yes [1], No [2]):")
        another_social_choice_label.pack(pady=5)
        another_social_choice_entry = ctk.CTkEntry(social_window)
        another_social_choice_entry.pack(pady=5)

        def submit_social():
            social_choice = get_input(social_choice_entry, "int")
            if social_choice == 1:
                while True:
                    social = get_input(social_entry, "string")

                    cur.execute("SELECT MAX(establishment_social_id) FROM FOOD_ESTABLISHMENT_SOCIAL")
                    new_social_increment = cur.fetchone()[0] or 0

                    alter_query = "ALTER TABLE FOOD_ESTABLISHMENT_SOCIAL AUTO_INCREMENT = %s"
                    cur.execute(alter_query, (new_social_increment,))

                    query_for_social = "INSERT INTO FOOD_ESTABLISHMENT_SOCIAL (establishment_id, social_media_link) VALUES (%s, %s)"
                    values_for_social = (establishment_id, social)
                    cur.execute(query_for_social, values_for_social)

                    another_choice = get_input(another_social_choice_entry, "int")
                    if another_choice == 2:
                        break

            social_window.destroy()

        submit_button = ctk.CTkButton(social_window, text="Submit Social Media Link", command=submit_social)
        submit_button.pack(pady=20)

    submit_button = ctk.CTkButton(scrollable_frame, text="Submit Establishment", command=submit_establishment)
    submit_button.pack(pady=20)

'''
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

        cur.execute("SELECT MAX(establishment_contact_id) FROM FOOD_ESTABLISHMENT_CONTACT")
        new_contact_increment = cur.fetchone()[0]

        alter_query = "ALTER TABLE FOOD_ESTABLISHMENT_CONTACT AUTO_INCREMENT = %s"
        cur.execute(alter_query, (new_contact_increment,))

        # query_for_contact = "INSERT INTO FOOD_ESTABLISHMENT_CONTACT (establishment_id, establishment_contact_number) VALUES (%s, %s)"
        # values_for_contact = (establishment_id, contact)
        # cur.execute(query_for_contact, values_for_contact)

        cur.execute("SELECT MAX(establishment_social_id) FROM FOOD_ESTABLISHMENT_SOCIAL")
        new_social_increment = cur.fetchone()[0]

        alter_query = "ALTER TABLE FOOD_ESTABLISHMENT_SOCIAL AUTO_INCREMENT = %s"
        cur.execute(alter_query, (new_social_increment,))

        # query_for_social = "INSERT INTO FOOD_ESTABLISHMENT_SOCIAL (establishment_id, social_media_link) VALUES (%s, %s)"
        # values_for_social = (establishment_id, social)
        # cur.execute(query_for_social, values_for_social)


        print("\nEstablishment added successfully.")
    '''

def delete_establishment(cur, user_id):
    def get_id(entry):
        value = entry.get()
        return int(value) if value.isdigit() else None

    delete_establishment_window = ctk.CTkToplevel()
    delete_establishment_window.title("Delete Establishment")
    delete_establishment_window.geometry("400x300")

    establishment_id_label = ctk.CTkLabel(delete_establishment_window, text="Enter Establishment ID:")
    establishment_id_label.pack(pady=5)
    establishment_id_entry = ctk.CTkEntry(delete_establishment_window)
    establishment_id_entry.pack(pady=5)

    def submit_delete():
        establishment_id = get_id(establishment_id_entry)
        if establishment_id is None:
            messagebox.showerror("Invalid ID", "Please enter a valid establishment ID.")
            return

        query = "SELECT user_id FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
        cur.execute(query, (establishment_id,))

        owner_of_food_establishment = cur.fetchone()
        if owner_of_food_establishment is None:
            messagebox.showerror("Invalid ID", "No establishment found with this ID.")
            return

        owner_of_food_establishment = owner_of_food_establishment[0]
        
        if user_id != owner_of_food_establishment:
            messagebox.showerror("Permission Denied", "You can't delete this food establishment added by another user.")
            return

        # Delete contact from food_establishment_contact
        query_contact_delete = "DELETE FROM FOOD_ESTABLISHMENT_CONTACT WHERE establishment_id = %s"
        cur.execute(query_contact_delete, (establishment_id,))

        # Delete social from food_establishment_social
        query_social_delete = "DELETE FROM FOOD_ESTABLISHMENT_SOCIAL WHERE establishment_id = %s"
        cur.execute(query_social_delete, (establishment_id,))

        # Delete establishment from food_establishment
        query = "DELETE FROM FOOD_ESTABLISHMENT WHERE establishment_id = %s"
        cur.execute(query, (establishment_id,))

        messagebox.showinfo("Success", "Successfully deleted food establishment")
        delete_establishment_window.destroy()

    submit_button = ctk.CTkButton(delete_establishment_window, text="Delete Establishment", command=submit_delete)
    submit_button.pack(pady=20)

'''
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
'''

def search_establishment(cur):
    def get_input(entry, data_type):
        value = entry.get()
        if data_type == "string":
            return value
        elif data_type == "int":
            return int(value) if value.isdigit() else None

    def display_results(result, search_option):
        for widget in results_frame.winfo_children():
            widget.destroy()

        if result:
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
                result_label = ctk.CTkLabel(results_frame, text=f"Establishment ID: {est_id}\n"
                                                                f"Establishment Name: {details['name']}\n"
                                                                f"Date Established: {details['date_established']}\n"
                                                                f"Location: {details['location']}\n"
                                                                f"Opening Hour: {details['opening_hour']}\n"
                                                                f"User ID: {details['user_id']}\n"
                                                                f"Average Rating: {details['avg_rating']:.2f if details['avg_rating'] else 'No reviews yet'}\n"
                                                                f"Contact Numbers: {', '.join(details['establishment_contact_number']) if details['establishment_contact_number'] else 'No contact numbers available'}\n"
                                                                f"Social Media Links: {', '.join(details['social_media_links']) if details['social_media_links'] else 'No social media links available'}",
                                           justify='left')
                result_label.pack(pady=5)
        else:
            no_results_label = ctk.CTkLabel(results_frame, text="No establishment found matching the search criteria.")
            no_results_label.pack(pady=5)

    def submit_search():
        search_option = get_input(search_option_entry, "int")
        if search_option == 1:
            establishment_id_label.pack(pady=5)
            establishment_id_entry.pack(pady=5)
            search_by_id_button.pack(pady=5)
            establishment_name_label.pack_forget()
            establishment_name_entry.pack_forget()
            search_by_name_button.pack_forget()
        elif search_option == 2:
            establishment_name_label.pack(pady=5)
            establishment_name_entry.pack(pady=5)
            search_by_name_button.pack(pady=5)
            establishment_id_label.pack_forget()
            establishment_id_entry.pack_forget()
            search_by_id_button.pack_forget()
        else:
            messagebox.showerror("Invalid Option", "Please select a valid search option.")

    def search_by_id():
        establishment_id = get_input(establishment_id_entry, "int")
        if establishment_id is None:
            messagebox.showerror("Invalid ID", "Please enter a valid establishment ID.")
            return

        query = """
            SELECT fe.establishment_id, fe.establishment_name, fe.date_established, fe.location, fe.opening_hour, fe.user_id, 
                cn.establishment_contact_number, sm.social_media_link, AVG(rv.rating) as avg_rating
            FROM FOOD_ESTABLISHMENT fe
            LEFT JOIN FOOD_ESTABLISHMENT_CONTACT cn ON fe.establishment_id = cn.establishment_id
            LEFT JOIN FOOD_ESTABLISHMENT_SOCIAL sm ON fe.establishment_id = sm.establishment_id
            LEFT JOIN REVIEW rv ON fe.establishment_id = rv.establishment_id
            WHERE fe.establishment_id = %s
            GROUP BY fe.establishment_id, cn.establishment_contact_number, sm.social_media_link
            ORDER BY fe.establishment_id
        """
        cur.execute(query, (establishment_id,))
        result = cur.fetchall()
        display_results(result, 1)

    def search_by_name():
        establishment_name = get_input(establishment_name_entry, "string")
        if not establishment_name:
            messagebox.showerror("Invalid Name", "Please enter a valid establishment name.")
            return

        query = """
            SELECT fe.establishment_id, fe.establishment_name, fe.date_established, fe.location, fe.opening_hour, fe.user_id, 
                cn.establishment_contact_number, sm.social_media_link, AVG(rv.rating) as avg_rating
            FROM FOOD_ESTABLISHMENT fe
            LEFT JOIN FOOD_ESTABLISHMENT_CONTACT cn ON fe.establishment_id = cn.establishment_id
            LEFT JOIN FOOD_ESTABLISHMENT_SOCIAL sm ON fe.establishment_id = sm.establishment_id
            LEFT JOIN REVIEW rv ON fe.establishment_id = rv.establishment_id
            WHERE fe.establishment_name LIKE %s
            GROUP BY fe.establishment_id, cn.establishment_contact_number, sm.social_media_link
            ORDER BY fe.establishment_id
        """
        cur.execute(query, (f'%{establishment_name}%',))
        result = cur.fetchall()
        display_results(result, 2)

    search_establishment_window = ctk.CTkToplevel()
    search_establishment_window.title("Search Establishment")
    search_establishment_window.geometry("600x600")

    search_option_label = ctk.CTkLabel(search_establishment_window, text="Search by [1] Establishment ID or [2] Establishment Name:")
    search_option_label.pack(pady=5)
    search_option_entry = ctk.CTkEntry(search_establishment_window)
    search_option_entry.pack(pady=5)

    submit_button = ctk.CTkButton(search_establishment_window, text="Submit Search Option", command=submit_search)
    submit_button.pack(pady=20)

    establishment_id_label = ctk.CTkLabel(search_establishment_window, text="Enter Establishment ID:")
    establishment_id_entry = ctk.CTkEntry(search_establishment_window)
    search_by_id_button = ctk.CTkButton(search_establishment_window, text="Search by ID", command=search_by_id)

    establishment_name_label = ctk.CTkLabel(search_establishment_window, text="Enter partial or full Establishment Name:")
    establishment_name_entry = ctk.CTkEntry(search_establishment_window)
    search_by_name_button = ctk.CTkButton(search_establishment_window, text="Search by Name", command=search_by_name)

    results_frame = ctk.CTkScrollableFrame(search_establishment_window, width=580, height=350)
    results_frame.pack(pady=10, padx=10, fill="both", expand=True)

'''
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
'''



'''
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
            

            #Update Contact Numbers
            query = "SELECT establishment_contact_number FROM FOOD_ESTABLISHMENT_CONTACT WHERE establishment_id = %s"
            cur.execute(query, (establishment_id,))
            result = cur.fetchall()
            
            if result:
                contact_number = set()
                for row in result:
                    contact_number.add(row[0])
                print(f"\nYour current contact number is/are : ")
                for number in enumerate(contact_number, start=1):
                    print(f" {number[0]}. {number[1]}")
                contact_choice = get_input("Do you want to update your contact number? (Yes [1], No [2]): ", "int", 1, 2, None, None)
            else:
                print("\nYou currently don't have a contact number")
                contact_choice = get_input("Do you want to add your contact number? (Yes [1], No [2]): ", "int", 1, 2, None, None)

                #Get multiple inputs of contact numbers
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


            


            if (contact_choice == 1):
                add_or_update_number = get_input("Do you want to add a new contact number or update an existing one? (Add [1], Update [2]): ", "int", 1, 2, None, None)
                
                #Add Contact Number
                if (add_or_update_number == 1):
                    #allow for multiple entries of contact number
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

                #update Contact Number
                elif (add_or_update_number == 2):
                    #count the number of contact numbers to update
                    for number in contact_number:
                        contact = get_input("Enter Contact Number: (09XXXXXXXXX)", "contact", 1, 75, None, None)


                        #get the the id of the contact number to update
                        query_for_contact_id = "SELECT establishment_contact_id FROM FOOD_ESTABLISHMENT_CONTACT WHERE establishment_contact_number = %s"
                        values_for_contact_id = (number,)  
                        cur.execute(query_for_contact_id, values_for_contact_id)
                        contact_id = cur.fetchone()[0]

                        query_for_contact = "UPDATE FOOD_ESTABLISHMENT_CONTACT SET establishment_contact_number = %s WHERE establishment_contact_id = %s"
                        values_for_contact = (contact, contact_id)
                        cur.execute(query_for_contact, values_for_contact)



            #Update Social Media Links
            query = "SELECT social_media_link FROM FOOD_ESTABLISHMENT_SOCIAL WHERE establishment_id = %s"
            cur.execute(query, (establishment_id,))
            result = cur.fetchall()
            
            if result:
                links = set()
                for row in result:
                    links.add(row[0])

                print(f"\nYour current social media link is/are : ")
                for link in enumerate(links, start=1):
                    print(f" {link[0]}. {link[1]}")
                social_choice = get_input("Do you want to update your social media link? (Yes [1], No [2]): ", "int", 1, 2, None, None)
            else:
                print("\nYou currently don't have a social media link")
                social_choice = get_input("Do you want to add your social media link? (Yes [1], No [2]): ", "int", 1, 2, None, None)

                #Getting multiple inputs of social media links
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

            if (social_choice == 1):
                add_or_update_link = get_input("Do you want to add a new social media link or update an existing one? (Add [1], Update [2]): ", "int", 1, 2, None, None)
            
                if (add_or_update_link == 1):
                    #Getting multiple inputs of social media links
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

                elif (add_or_update_link == 2):
                    for link in links:
                        social_link = get_input("Enter Social Media Link: ", "string", 1, 75, None, None)

                        # get the id of the contact number to update
                        query_for_social_id = "SELECT establishment_social_id FROM FOOD_ESTABLISHMENT_SOCIAL WHERE social_media_link = %s"
                        values_for_social_id = (link,)
                        cur.execute(query_for_social_id, values_for_social_id)
                        link_id = cur.fetchone()[0]

                        query_for_social = "UPDATE FOOD_ESTABLISHMENT_SOCIAL SET social_media_link = %s WHERE establishment_social_id = %s"
                        values_for_social = (social_link, link_id)
                        cur.execute(query_for_social, values_for_social)

            query = "UPDATE FOOD_ESTABLISHMENT SET establishment_name = %s, date_established = %s, location = %s, opening_hour = %s, user_id = %s WHERE establishment_id = %s"
            values = (establishment_name, date_established, location, opening_hour, user_id, establishment_id)
            cur.execute(query, values)

            break
    return
'''        

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