users = [{"username": "raffay", "password": "secret123", "email": "raffay@example.com"}]

def verify_login(choice: int, identifier: str, password: str) -> bool:
    if choice != 1 and choice != 2:
        return False

    for user in users:
        if choice == 1:
            if identifier == user["email"] and password == user["password"]:
                return True
        if choice == 2:
            if identifier == user["username"] and password == user["password"]:
                return True

    return False

def register_user(username: str, email: str, password: str) -> bool:
    for user in users:
        if user["username"] == username or user["email"] == email:
            return False 

    users.append({"username": username, "email": email, "password": password})
    return True