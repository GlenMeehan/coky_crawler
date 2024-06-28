
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

def can_fetch(url, user_agent='*'):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(base_url)
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except:
        return True  # If robots.txt is not found or unreadable, assume it's allowed
