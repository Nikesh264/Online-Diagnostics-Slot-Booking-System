import csv
import os

# File paths for storing data
SLOT_FILE = "slots.csv"
USER_FILE = "users.csv"

# Load data from CSV files
def load_slots():
    slots = []
    if os.path.exists(SLOT_FILE):
        with open(SLOT_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                slot = {
                    'date': row['date'],
                    'time': row['time'],
                    'booked': row['booked'] == 'True',
                    'user': row['user'] if row['user'] != 'None' else None
                }
                slots.append(slot)
    return slots

def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row['username']] = {
                    'password': row['password'],
                    'bookings': [int(x) for x in row['bookings'].split(';') if x]
                }
    return users

# Save data to CSV files
def save_slots(slots):
    with open(SLOT_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['date', 'time', 'booked', 'user'])
        writer.writeheader()
        for slot in slots:
            writer.writerow({
                'date': slot['date'],
                'time': slot['time'],
                'booked': slot['booked'],
                'user': slot['user'] if slot['user'] else 'None'
            })

def save_users(users):
    with open(USER_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['username', 'password', 'bookings'])
        writer.writeheader()
        for username, data in users.items():
            writer.writerow({
                'username': username,
                'password': data['password'],
                'bookings': ';'.join(map(str, data['bookings']))
            })

# Function to create a slot
def create_slot(date, time, slots):
    slot = {
        'date': date,
        'time': time,
        'booked': False,
        'user': None
    }
    slots.append(slot)

# Function to view all slots
def view_slots(slots):
    if not slots:
        print("No slots available.")
        return
    for i, slot in enumerate(slots):
        status = "Booked" if slot['booked'] else "Available"
        print(f"Slot {i+1}: Date: {slot['date']}, Time: {slot['time']}, Status: {status}")

# Function to book a slot
def book_slot(username, slot_index, slots, users):
    if slot_index < 1 or slot_index > len(slots):
        print("Invalid slot index.")
        return
    
    slot = slots[slot_index - 1]
    
    if slot['booked']:
        print(f"Slot {slot_index} is already booked.")
    else:
        slot['booked'] = True
        slot['user'] = username
        users[username]['bookings'].append(slot_index)
        print(f"Slot {slot_index} booked successfully by {username}.")
        save_slots(slots)
        save_users(users)

# Function to cancel a booking
def cancel_booking(username, slot_index, slots, users):
    if slot_index < 1 or slot_index > len(slots):
        print("Invalid slot index.")
        return
    
    slot = slots[slot_index - 1]
    
    if not slot['booked']:
        print(f"Slot {slot_index} is not booked.")
    elif slot['user'] != username:
        print(f"Slot {slot_index} was not booked by {username}.")
    else:
        slot['booked'] = False
        slot['user'] = None
        users[username]['bookings'].remove(slot_index)
        print(f"Slot {slot_index} booking canceled by {username}.")
        save_slots(slots)
        save_users(users)

# Admin Functions
def admin_add_slot(date, time, slots):
    create_slot(date, time, slots)
    print(f"Slot added: Date: {date}, Time: {time}")
    save_slots(slots)

def admin_remove_slot(slot_index, slots):
    if slot_index < 1 or slot_index > len(slots):
        print("Invalid slot index.")
        return
    
    slots.pop(slot_index - 1)
    print(f"Slot {slot_index} removed successfully.")
    save_slots(slots)

def admin_view_slots(slots):
    view_slots(slots)

def admin_manage_users(users):
    print("\nRegistered Users:")
    for user in users:
        print(f"Username: {user}, Bookings: {users[user]['bookings']}")

# User Functions
def register_user(username, password, users):
    if username in users:
        print("Username already exists.")
        return False
    users[username] = {'password': password, 'bookings': []}
    save_users(users)
    print(f"User {username} registered successfully.")
    return True

def login_user(username, password, users):
    if username not in users:
        print("Username not found.")
        return False
    if users[username]['password'] != password:
        print("Incorrect password.")
        return False
    print(f"User {username} logged in successfully.")
    return True

def user_view_bookings(username, slots, users):
    if not users[username]['bookings']:
        print(f"{username} has no bookings.")
        return
    print(f"{username}'s Bookings:")
    for slot_index in users[username]['bookings']:
        slot = slots[slot_index - 1]
        print(f"Slot {slot_index}: Date: {slot['date']}, Time: {slot['time']}")

# Example Usage
def main():
    slots = load_slots()
    users = load_users()

    while True:
        print("\n1. Register\n2. Login\n3. Admin\n4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password, users)
        
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if login_user(username, password, users):
                while True:
                    print("\n1. View Slots\n2. Book Slot\n3. Cancel Booking\n4. View My Bookings\n5. Logout")
                    user_choice = input("Choose an option: ")
                    
                    if user_choice == '1':
                        view_slots(slots)
                    elif user_choice == '2':
                        slot_index = int(input("Enter slot index to book: "))
                        book_slot(username, slot_index, slots, users)
                    elif user_choice == '3':
                        slot_index = int(input("Enter slot index to cancel: "))
                        cancel_booking(username, slot_index, slots, users)
                    elif user_choice == '4':
                        user_view_bookings(username, slots, users)
                    elif user_choice == '5':
                        break
                    else:
                        print("Invalid option.")
        
        elif choice == '3':
            admin_password = input("Enter admin password: ")
            if admin_password == "admin":
                while True:
                    print("\n1. Add Slot\n2. Remove Slot\n3. View Slots\n4. Manage Users\n5. Logout")
                    admin_choice = input("Choose an option: ")
                    
                    if admin_choice == '1':
                        date = input("Enter slot date (YYYY-MM-DD): ")
                        time = input("Enter slot time (HH:MM AM/PM): ")
                        admin_add_slot(date, time, slots)
                    elif admin_choice == '2':
                        slot_index = int(input("Enter slot index to remove: "))
                        admin_remove_slot(slot_index, slots)
                    elif admin_choice == '3':
                        admin_view_slots(slots)
                    elif admin_choice == '4':
                        admin_manage_users(users)
                    elif admin_choice == '5':
                        break
                    else:
                        print("Invalid option.")
            else:
                print("Incorrect admin password.")
        
        elif choice == '4':
            break
        
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
