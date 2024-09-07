def sample_book_create():
    return {
        "title": "The Lean Startup",
        "page_count": 293,
        "description": "Helpful book",
        "category": "mystery",
        "author": "Obinna",
    }


def sample_book_missing_title():
    return {
        "author": "Sun Tzu",
        "description": "A book about military strategy and tactics",
        "published_year": 500,
        "category": "Strategy",
        "publisher": "Penguin Classics",
    }


def sample_borrowed_book_create():
    return {"book_id": 1, "user_id": 1, "days_to_borrow": 3, "due_date": "2024-10-31"}


def sample_search_category():
    return {
        "category": "mystery",
    }


def sample_search_nonexistent_category():
    return {
        "category": "comedy",
    }


def sample_search_publisher():
    return {
        "publisher": "obinna",
    }


def sample_search_nonexistent_publisher():
    return {
        "publisher": "blah blah",
    }
