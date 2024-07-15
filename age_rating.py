# age_rating.py

def age_rating(content):
    adult_keywords = {"explicit", "violence", "gambling", "drugs", "alcohol"}
    for keyword in adult_keywords:
        if keyword in content.lower():
            return "18+"  # Adult content
    return "All Ages"  # General audience
