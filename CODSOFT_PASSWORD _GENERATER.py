import string
import secrets

def generate_password(length=12, use_upper=True, use_digits=True, use_symbols=True):
    if length < 4:
        raise ValueError("Password length must be at least 4 characters.")

    pools = [string.ascii_lowercase]
    guaranteed = [secrets.choice(string.ascii_lowercase)]

    if use_upper:
        pools.append(string.ascii_uppercase)
        guaranteed.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        pools.append(string.digits)
        guaranteed.append(secrets.choice(string.digits))
    if use_symbols:
        pools.append(string.punctuation)
        guaranteed.append(secrets.choice(string.punctuation))

    all_characters = "".join(pools)
    remaining_length = length - len(guaranteed)
    password_chars = guaranteed + [secrets.choice(all_characters) for _ in range(remaining_length)]

    system_random = secrets.SystemRandom()
    system_random.shuffle(password_chars)

    return "".join(password_chars)

def evaluate_strength(length):
    if length < 8:
        return "Weak"
    elif length < 12:
        return "Moderate"
    elif length < 16:
        return "Strong"
    return "Very Strong"

def main():
    print("=== Secure Password Generator ===")
    while True:
        user_input = input("\nEnter password length (or 'q' to quit): ").strip().lstrip('\ufeff')
        if user_input.lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            break

        try:
            length = int(user_input)
            password = generate_password(length)
            strength = evaluate_strength(length)
            print(f"Generated Password: {password}")
            print(f"Strength          : {strength}")
        except ValueError as e:
            print(f"Error: {e}. Please enter a valid number (minimum 4).")

if __name__ == "__main__":
    main()
