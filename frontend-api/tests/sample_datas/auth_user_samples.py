def sample_auth_user_create():
    return {
        "email": "obbyprecious12@gmail.com",
        "password": "2Strong",
        "first_name": "precious",
        "last_name": "ohanyere",
    }


def sample_auth_user_wrong_email():
    return {
        "email": "obbyprecious12.gmail.com",
        "password": "2Strong",
    }


def sample_login_user():
    return {"username": "obbyprecious12@gmail.com", "password": "2Strong"}


def sample_login_user_wrong_email():
    return {"username": "wrongemail.com", "password": "2Strong"}


def sample_header():
    return {
        "user-agent": "PostmanRuntime/7.28.0",
        "host": "127.0.0.1",
    }
