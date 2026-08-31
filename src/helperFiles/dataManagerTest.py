import secureFileManager
import objects

while True:
    match input("Login or create new user? (1. Login/2. Create): "):
        case "1":
            try:
                dm = secureFileManager.SecureDataManager(input("Enter username: "), input("Enter password: "))
                print(f"User data loaded successfully for user '{dm.username}': {dm.user_data}")
            except objects.NoAccountError:
                print("Account not found. Please create a new account.")
            continue
        case "2":
            dm = secureFileManager.SecureDataManager(input("Enter username: "), input("Enter password: "), create=True)
            print(f"User data created successfully for user '{dm.username}': {dm.user_data}")
            continue
        case _:
            print("Invalid option. Please enter '1' to login or '2' to create a new user.")
            continue
