
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from urllib.error import URLError, HTTPError
import socket
from functools import lru_cache

@lru_cache(maxsize=128)  # Cache up to 128 different robots.txt files
def can_fetch(url, user_agent='*'):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = RobotFileParser()
    rp.set_url(base_url)
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except (URLError, HTTPError, socket.timeout) as e:
        # Handle specific exceptions like URLError, HTTPError, or socket.timeout
        print(f"Exception while reading {base_url}: {e}")
        return True  # Assume allowed due to error
    except Exception as e:
        # Catch any other unexpected exceptions for debugging
        print(f"Unexpected exception while reading {base_url}: {e}")
        return True  # Assume allowed due to unknown error
