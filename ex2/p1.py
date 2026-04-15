def gcd(a, b):
    """Function to find the greatest common divisor of a and b."""
    while b:
        a, b = b, a % b
    return a

def prime_factors(n):
    """Function to find all distinct prime factors of n."""
    factors = set()
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.add(i)
            n //= i
        i += 1
    if n > 1:
        factors.add(n)
    return factors

def is_primitive_root(g, p):
    """Check if g is a primitive root of p."""
    phi = p - 1  # Euler's Totient for prime p
    factors = prime_factors(phi)

    # Check all prime factors
    for factor in factors:
        if pow(g, phi // factor, p) == 1:
            return False
    return True

def primitive_roots_of_prime(prime):
    """Find all primitive roots of the prime number."""
    roots = []
    for g in range(2, prime):
        if is_primitive_root(g, prime):
            roots.append(g)
    return roots

# Main program
while True:
    print("\nMenu:")
    print("1. Find primitive roots of a prime number")
    print("2. Find GCD of two numbers")
    print("3. Exit")

    choice = input("Choose an option (1/2/3): ")

    if choice == '1':
        try:
            n = int(input("Enter a prime number to find its primitive roots: "))
            if n < 2:
                print("Please enter a prime number greater than 1.")
            else:
                roots = primitive_roots_of_prime(n)
                if roots:
                    print(f"The primitive roots of {n} are: {roots}")
                else:
                    print(f"There are no primitive roots for {n}.")
        except ValueError:
            print("Please enter a valid integer.")

    elif choice == '2':
        try:
            a = int(input("Enter the first number: "))
            b = int(input("Enter the second number: "))
            result = gcd(a, b)
            print(f"The GCD of {a} and {b} is: {result}")
        except ValueError:
            print("Please enter valid integers.")

    elif choice == '3':
        print("Exiting the program.")
        break

    else:
        print("Invalid choice, please try again.")
