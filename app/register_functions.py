def check_passwordrequirements(password):
    if len(password) >= 8:
        return True
    return False

def check_usernamerequirements(username):
    if len(username) >= 3:
        return True
    return False