import string

# Utility function to remove new line characters
def remove_newline(s):
    return s.strip()

# Caesar Cipher
def caesar(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            base = 'A' if char.isupper() else 'a'
            shifted = chr((ord(char) - ord(base) + shift) % 26 + ord(base))
            result.append(shifted)
        else:
            result.append(char)
    return ''.join(result)

# Playfair Cipher Utility Functions
def generate_playfair_matrix(key):
    used = [False] * 26
    matrix = []

    key = key.upper().replace('J', 'I')
    for char in key:
        if char.isalpha() and not used[ord(char) - ord('A')]:
            matrix.append(char)
            used[ord(char) - ord('A')] = True

    for char in string.ascii_uppercase:
        if char == 'J':
            continue
        if not used[ord(char) - ord('A')]:
            matrix.append(char)
            used[ord(char) - ord('A')] = True

    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == char:
                return r, c
    return None

def prepare_text(text):
    temp = [char for char in text.upper() if char.isalpha()]
    text = ''.join(temp).replace('J', 'I')

    result = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] == text[i + 1]:
            result.append(text[i])
            result.append('X')
            i += 1
        else:
            result.append(text[i])
            if i + 1 < len(text):
                result.append(text[i + 1])
            else:
                result.append('X')
            i += 2
    return ''.join(result)

def playfair_encrypt(text, key):
    matrix = generate_playfair_matrix(key)
    text = prepare_text(text)
    result = []

    for i in range(0, len(text), 2):
        r1, c1 = find_position(matrix, text[i])
        r2, c2 = find_position(matrix, text[i + 1])

        if r1 == r2:
            result.append(matrix[r1][(c1 + 1) % 5])
            result.append(matrix[r2][(c2 + 1) % 5])
        elif c1 == c2:
            result.append(matrix[(r1 + 1) % 5][c1])
            result.append(matrix[(r2 + 1) % 5][c2])
        else:
            result.append(matrix[r1][c2])
            result.append(matrix[r2][c1])

    return ''.join(result)

def playfair_decrypt(text, key):
    matrix = generate_playfair_matrix(key)
    result = []

    for i in range(0, len(text), 2):
        r1, c1 = find_position(matrix, text[i])
        r2, c2 = find_position(matrix, text[i + 1])

        if r1 == r2:
            result.append(matrix[r1][(c1 - 1) % 5])
            result.append(matrix[r2][(c2 - 1) % 5])
        elif c1 == c2:
            result.append(matrix[(r1 - 1) % 5][c1])
            result.append(matrix[(r2 - 1) % 5][c2])
        else:
            result.append(matrix[r1][c2])
            result.append(matrix[r2][c1])

    return ''.join(result)

# Hill Cipher Utility Functions
def mod_inverse(a):
    a = a % 26
    for i in range(1, 26):
        if (a * i) % 26 == 1:
            return i
    return None

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]

    det = 0
    for c in range(len(matrix)):
        sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        det += ((-1) ** c) * matrix[0][c] * determinant(sub_matrix)

    return det

def adjoint(matrix):
    adj = [[0]*len(matrix) for _ in range(len(matrix))]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            sub_matrix = [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]
            sign = (-1) ** (i + j)
            adj[j][i] = sign * determinant(sub_matrix)
    return adj

def inverse_matrix(matrix):
    det = determinant(matrix) % 26
    inv_det = mod_inverse(det)

    if inv_det is None:
        return None

    adj = adjoint(matrix)

    inv = [[(adj[i][j] * inv_det) % 26 for j in range(len(adj))] for i in range(len(adj))]
    return inv

def hill_encrypt(text, key):
    n = len(key)
    # Ensure the text is at least the length of n or padded
    padded_text = text.upper() + 'X' * (n - len(text) % n) if len(text) % n != 0 else text.upper()
    result = []

    for i in range(0, len(padded_text), n):
        vector = [ord(char) - ord('A') for char in padded_text[i:i + n]]
        encrypted_vector = [(sum(key[r][c] * vector[c] for c in range(n)) % 26) for r in range(n)]
        result.extend(chr(val + ord('A')) for val in encrypted_vector)

    return ''.join(result)

def hill_decrypt(text, key):
    inv_key = inverse_matrix(key)
    if inv_key is None:
        print("Key matrix is NOT invertible!")
        return text

    result = []

    for i in range(0, len(text), len(key)):
        vector = [ord(char) - ord('A') for char in text[i:i + len(key)]]
        decrypted_vector = [(sum(inv_key[r][c] * vector[c] for c in range(len(key))) % 26) for r in range(len(key))]
        result.extend(chr(val + ord('A')) for val in decrypted_vector)

    return ''.join(result).rstrip('X')  # Remove padding if needed

# Main menu function
def main():
    while True:
        print("\n===== CIPHER MENU =====")
        print("1. Caesar Cipher")
        print("2. Playfair Cipher")
        print("3. Hill Cipher")
        print("4. Exit")

        choice = int(input("Enter choice: "))
        if choice == 4:
            break

        if choice == 1:
            text = input("Enter plaintext: ")
            shift = int(input("Enter shift: "))
            encrypted = caesar(remove_newline(text), shift)
            print(f"Encrypted: {encrypted}")

            opt = input("Decrypt? (y/n): ")
            if opt.lower() == 'y':
                decrypted = caesar(encrypted, -shift)
                print(f"Decrypted: {decrypted}")

        elif choice == 2:
            text = input("Enter plaintext: ")
            key = input("Enter key: ")
            encrypted = playfair_encrypt(remove_newline(text), key)
            print(f"Encrypted: {encrypted}")

            opt = input("Decrypt? (y/n): ")
            if opt.lower() == 'y':
                decrypted = playfair_decrypt(encrypted, key)
                print(f"Decrypted: {decrypted}")

        elif choice == 3:
            n = int(input("Enter matrix size n: "))
            key = []
            print(f"Enter key matrix ({n}x{n}):")
            for _ in range(n):
                row = list(map(int, input().strip().split()))
                key.append(row)

            text = input("Enter plaintext: ")
            encrypted = hill_encrypt(remove_newline(text), key)
            print(f"Encrypted: {encrypted}")

            opt = input("Decrypt? (y/n): ")
            if opt.lower() == 'y':
                decrypted = hill_decrypt(encrypted, key)
                print(f"Decrypted: {decrypted}")

if __name__ == "__main__":
    main()
