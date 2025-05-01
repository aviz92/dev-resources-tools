import random
from random import choice
from string import ascii_letters, ascii_lowercase, ascii_uppercase, digits


def generate_random_string(length: int = 8, charset: str = ascii_letters + digits) -> str:
    """
    Generate a random string of a given length using a specified character set
    :param length: The length of the string to generate
    :param charset: The set of characters to use for generating the string
    Return - A random string based on the specified character set
    """
    return ''.join(choice(charset) for _ in range(length))


def generate_random_password(length: int = 8) -> str:
    """
    Generate a random password with a given length
    """
    special_characters = "!@#%^*"
    # Ensure the password starts with a letter
    password = choice(ascii_uppercase)
    # Ensure the password contains at least one digit or special character and one lowercase letter
    password += choice(digits + special_characters)
    password += choice(ascii_lowercase)

    # Fill the remaining characters with a mix of all types
    remaining_chars = ''.join(
        choice(ascii_letters + digits + special_characters) for _ in range(length - len(password))
    )

    password += remaining_chars

    # Shuffle the password to make it more random but keep the first character as a letter
    return password[0] + ''.join(random.sample(password[1:], len(password) - 1))


def generate_random_ipv4() -> str:
    # Generate the first octet (1-223 to avoid multicast and reserved ranges)
    first_octet = random.randint(1, 223)
    remaining_octets = [str(random.randint(0, 255)) for _ in range(3)]
    return f"{first_octet}.{'.'.join(remaining_octets)}"


def generate_random_ipv6() -> str:
    first_group = f'{random.randint(0x2000, 0x3fff):04x}'
    other_groups = [f'{random.randint(0, 0xffff):04x}' for _ in range(7)]
    return ':'.join([first_group] + other_groups)


def generate_random_ip(ip_version: int) -> str:
    """
    Generate a random IP address based on the specified version
    If the cluster IP type matters, please use this function as follows:
    generate_random_ip(ip_version=client.cluster.get_ip_version()) to get the IP version based on the cluster
    """
    if ip_version == 4:
        return generate_random_ipv4()
    if ip_version == 6:
        return generate_random_ipv6()
    raise ValueError(f"Unsupported IP version: {ip_version}. Supported versions are 4 and 6.")


def create_random_text(min_length: int = 64, max_length: int = 4096):
    """Generate a random string with a length between min_length and max_length characters."""
    length = random.randint(min_length, max_length)
    return ''.join(random.choice(ascii_letters) for _ in range(length))
