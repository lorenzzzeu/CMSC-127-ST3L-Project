from datetime import datetime

# Check if entity exists
# - Parameters:
#   1. cursor (cursor): mariaDB cursor
#   2. t (string): entity type (user, establishment, item, review)
#   3. id (int): entity id
# - Returns 1 if entity exists, otherwise 0
def validate_id (cur, t, id):
  if t == "user":
    cur.execute("SELECT user_id FROM user WHERE user_id = ?", (id,))
    for user_id in cur:
      if id == user_id[0]: return 1  

  elif t == "establishment":
    cur.execute("SELECT establishment_id FROM food_establishment WHERE establishment_id = ?", (id,))
    for establishment_id in cur:
      if id == establishment_id[0]: return 1 

  elif t == "food": 
    cur.execute("SELECT food_id FROM food_item WHERE food_id = ?", (id,))
    for food_id in cur:
      if id == food_id[0]: return 1

  elif t == "review": 
    cur.execute("SELECT review_id FROM review WHERE review_id = ?", (id,))
    for review_id in cur:
      if id == review_id[0]: return 1

  return 0

# Get total number of given entity
# - Parameters:
#   1. cursor (cursor): mariaDB cursor
#   2. t (string): entity type (user, establishment, item, review)
#   3. prompt (bool): if count() should print "no {t}s" prompt
# - Returns total count of entities in DB
def count (cur, t, prompt):
  if (t == "user"):
    cur.execute(f"SELECT COUNT(*) count FROM user")
  else:
    cur.execute(f"SELECT COUNT(*) count FROM food_{t}")
    
  for count in cur:
    if count[0] == 0 and prompt:
      print(f"There are currently no {t}s.")
      
    return count[0]

# Get user input and check if it's valid
# Just saw this online....
# - Parameters:
#   1. msg (string): message prompt for input
#   2. type (string): input type (int, string, date)
#   3. min (int): minimum value
#   4. max (int): maximum value
#   5. optional_msg (string): message prompt for optional attributes ('y/n' prompts)
#   6. optional_rev (bool): 
#       - False if an 'n' (no) input should return None 
#       -- (will not continue to ask for user input for given type), 
#       - True if 'y' (yes) should return None
def get_input (msg, type, min, max, optional_msg, optional_rev):
  # For optional attributes
  if optional_msg:
    prompt = True 
    while prompt:
      user_input = input(optional_msg)
      if user_input in ("y", "n"):
        prompt = False
      else:
        print("Invalid input!")

    if (optional_rev and user_input == "y") or (not optional_rev and user_input == "n"):
      return None
  
  while True:
    if type == "string":
      string_input = input(msg)
      if (len(string_input) <= max) :
        return string_input
      else:
        print("Invalid input!")
    
    elif type == "date":
      date = input(msg)
      try:
        valid_date = datetime.strptime(date, "%Y-%m-%d").date()
        return valid_date
      except ValueError:
        print("Invalid date!")

    elif type == "contact":
      contact = input(msg)
      if (contact.startswith("09") and len(contact) == 11 and contact.isdigit()):
        return contact
      else:
        print("Invalid contact number")

    elif type == "hour":
      string_input = input(msg)
      try:
        valid_format = datetime.strptime(string_input, "%H:%M:%S").time()
        return valid_format
      except ValueError:
        print("Invalid format!")
    
    elif type == "int":
      try:
        int_input = int(input(msg))
        if (int_input >= min and int_input <= max):
          return int_input
        else:
          print("Invalid input!")

      except (ValueError, TypeError):
        print("Invalid input!")

    elif type == "bool":
      try:
        bool_input = input(msg)
        if (bool_input == "y" and not optional_rev) or (bool_input == "n" and optional_rev):
          return True
        elif (bool_input == "y" and optional_rev) or (bool_input == "n" and not optional_rev):
          return False
        else:
          print("Invalid input!")

      except (ValueError, TypeError):
        print("Invalid input!")
        
# Get entity id from user input
# - Parameters:
#   1. msg (string): message prompt for input
#   2. type (string): entity type (establishment, id, review)
#   3. mode (string): fetch or add mode for establishment
#   4. optional_msg (string): message prompt for optional attributes ('y/n' prompts)
#   5. optional_rev (bool): False = return NULL if an 'n' input should disregard optional attribute, otherwise True if 'y'   
def get_id(msg, type, mode, optional_msg, optional_rev, cur):
  # For optional attributes
  if optional_msg:
    prompt = True
    while prompt:
      user_input = input(optional_msg)
      if user_input in ("y", "n"):
        prompt = False
      else:
        print("Invalid input!")

    if (optional_rev and user_input == "y") or (not optional_rev and user_input == "n"):
      return None

  while True:
    if type == "user":
      if mode == "fetch":
        try:
          user_input = int(input(msg))
          if validate_id(cur, "user", user_input) == 1:
            return user_input
          else:
            print("User doesn't exist.")

        except (ValueError, TypeError):
          print("Invalid input!")

      elif mode == "add":
        try:
          user_input = int(input(msg))
          if validate_id(cur, "user", user_input) == 0:
            return user_input
          else:
            print("User ID is in the system already.")
        except (ValueError, TypeError):
          print("Invalid input!")

    elif type == "establishment":
      if mode == "fetch":
        try:
          establishment_input = int(input(msg))
          if validate_id(cur, "establishment", establishment_input) == 1:
            return establishment_input
          else:
            print("Establishment does not exist.")

        except (ValueError, TypeError):
          print("Invalid input!")

      elif mode == "add":
        try:
          establishment_input = int(input(msg))
          print(establishment_input)
          if validate_id(cur, "establishment", establishment_input) == 0:
            return establishment_input
          else:
            print("Establishment ID is in the system already.")
        except (ValueError, TypeError):
          print("Invalid input!")

    elif type == "food":
      if mode == "fetch":
        try:
          food_input = int(input(msg))
          if validate_id(cur, "food", food_input) == 1:
            return food_input
          else:
            print("Food item does not exist.")

        except (ValueError, TypeError):
          print("Invalid input!")

      elif mode == "add":
        try:
          food_input = int(input(msg))
          if validate_id(cur, "food", food_input) == 0:
            return food_input
          else:
            print("Food item ID is in the system already.")
        except (ValueError, TypeError):
          print("Invalid input!")


    elif type == "review":
      if mode == "fetch":
        try:
          review_input = int(input(msg))
          if validate_id(cur, "review", review_input) == 1:
            return review_input
          else:
            print("Review doesn't exist.")

        except (ValueError, TypeError):
          print("Invalid input!")

      elif mode == "add":
        try:
          review_input = int(input(msg))
          if validate_id(cur, "review", review_input) == 0:
            return review_input
          else:
            print("Review ID is in the system already.")
        except (ValueError, TypeError):
          print("Invalid input!")