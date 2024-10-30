import random
import re

# Function to store space positions and remove spaces and special characters (but keep numbers)
def preprocess_text(text):
    cleaned_text = re.sub(r'[^A-Za-z0-9 ]', '', text)  # Keep alphabetic characters and digits
    space_positions = [i for i, char in enumerate(cleaned_text) if char == ' ']
    cleaned_text = re.sub(r'[^A-Za-z0-9]', '', text)  # Remove spaces
    return space_positions, cleaned_text.upper()

# Function to add spaces back to decrypted text
def add_spaces_to_text(text, space_positions):
    for pos in space_positions:
        text = text[:pos] + ' ' + text[pos:]
    return text

# Helper functions to convert characters to index and back for A-Z0-9
def char_to_index(char):
    if char.isdigit():
        return ord(char) - ord('0') + 26
    else:
        return ord(char) - ord('A')

def index_to_char(index):
    if index < 26:
        return chr(index + ord('A'))
    else:
        return chr(index - 26 + ord('0'))

# Function to generate Fibonacci indexed characters from a key
def fibonacci_indexed_chars(key):
    fib_indices = []
    a, b = 0, 1
    while a < len(key):
        fib_indices.append(a)
        a, b = b, a + b
    fib_chars = [key[i] for i in fib_indices]
    print("Fibonacci Indexed Characters:", fib_chars)
    return fib_chars

# Function to generate Non-Fibonacci indexed characters from a key
def non_fibonacci_indexed_chars(key):
    fib_indices = set(fibonacci_indexed_chars(range(len(key))))
    non_fib_chars = [key[i] for i in range(len(key)) if i not in fib_indices]
    print("Non-Fibonacci Indexed Characters:", non_fib_chars)
    return non_fib_chars

# Vigenère Cipher Encryption with mod 36
def encrypt_vigenere(plaintext, key):
    key = ''.join(fibonacci_indexed_chars(key)).upper()  # Ensure key is uppercase
    encrypted_text = []
    for i in range(len(plaintext)):
        pt_index = char_to_index(plaintext[i])
        key_index = char_to_index(key[i % len(key)])
        encrypted_char = index_to_char((pt_index + key_index) % 36)
        encrypted_text.append(encrypted_char)
    result = "".join(encrypted_text)
    print("Vigenère Encrypted Text:", result)
    return result

# Vigenère Cipher Decryption with mod 36
def decrypt_vigenere(ciphertext, key):
    key = ''.join(fibonacci_indexed_chars(key)).upper()
    decrypted_text = []
    adjusted_key = (key * ((len(ciphertext) // len(key)) + 1))[:len(ciphertext)]
    for i in range(len(ciphertext)):
        ct_index = char_to_index(ciphertext[i])
        key_index = char_to_index(adjusted_key[i])
        decrypted_char = index_to_char((ct_index - key_index + 36) % 36)
        decrypted_text.append(decrypted_char)
    result = "".join(decrypted_text)
    print("Vigenère Decrypted Text:", result)
    return result

# Function to add ASCII values of two characters and mod by 36
def add_ascii_chars(vigenere_output, non_fib_key):
    new_key = ""
    for i in range(len(non_fib_key)):
        combined_ascii = (char_to_index(non_fib_key[i]) + char_to_index(vigenere_output[i % len(vigenere_output)])) % 36
        new_key += index_to_char(combined_ascii)
    print("New Key after ASCII Addition:", new_key)
    return new_key

# Generate 5x5 Playfair Key Square (only for letters)
def generate_playfair_matrix(key):
    key = key.lower().replace("j", "i")
    matrix = []
    seen = set()
    for char in key:
        if char not in seen and char in "abcdefghiklmnopqrstuvwxyz":
            seen.add(char)
            matrix.append(char)
    for char in "abcdefghiklmnopqrstuvwxyz":
        if char not in seen:
            matrix.append(char)
    matrix_5x5 = [matrix[i:i + 5] for i in range(0, 25, 5)]
    print("Playfair Matrix:", matrix_5x5)
    return matrix_5x5

# Helper functions for Playfair Encryption and Decryption
def search(matrix, element):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == element:
                return i, j
    return None

# Playfair Encryption with j-to-i tracking
def encrypt_playfair(matrix, text):
    encrypted_text = []
    digraphs = format_playfair_input(text)
    j_to_i_positions = [i for i, char in enumerate(text.lower()) if char == 'j']  # Track 'j' replacements
    for digraph in digraphs:
        e1_pos, e2_pos = search(matrix, digraph[0]), search(matrix, digraph[1])
        if e1_pos[0] == e2_pos[0]:  # Same row
            encrypted_text.append(matrix[e1_pos[0]][(e1_pos[1] + 1) % 5] + matrix[e2_pos[0]][(e2_pos[1] + 1) % 5])
        elif e1_pos[1] == e2_pos[1]:  # Same column
            encrypted_text.append(matrix[(e1_pos[0] + 1) % 5][e1_pos[1]] + matrix[(e2_pos[0] + 1) % 5][e2_pos[1]])
        else:  # Rectangle
            encrypted_text.append(matrix[e1_pos[0]][e2_pos[1]] + matrix[e2_pos[0]][e1_pos[1]])
    result = "".join(encrypted_text)
    print("Playfair Encrypted Text:", result)
    return result, j_to_i_positions  # Return j-to-i positions for later use

# Playfair Decryption with i-to-j replacement
def decrypt_playfair(matrix, text, j_to_i_positions):
    decrypted_text = []
    digraphs = format_playfair_input(text)
    for digraph in digraphs:
        e1_pos, e2_pos = search(matrix, digraph[0]), search(matrix, digraph[1])
        if e1_pos[0] == e2_pos[0]:  # Same row
            decrypted_text.append(matrix[e1_pos[0]][(e1_pos[1] - 1) % 5] + matrix[e2_pos[0]][(e2_pos[1] - 1) % 5])
        elif e1_pos[1] == e2_pos[1]:  # Same column
            decrypted_text.append(matrix[(e1_pos[0] - 1) % 5][e1_pos[1]] + matrix[(e2_pos[0] - 1) % 5][e2_pos[1]])
        else:  # Rectangle
            decrypted_text.append(matrix[e1_pos[0]][e2_pos[1]] + matrix[e2_pos[0]][e1_pos[1]])
    result = "".join(decrypted_text)

    # Convert 'i' back to 'j' at recorded positions
    result_list = list(result)
    for pos in j_to_i_positions:
        if pos < len(result_list) and result_list[pos] == 'i':
            result_list[pos] = 'j'
    result_with_js = ''.join(result_list)
    print("Playfair Decrypted Text:", result_with_js)
    return result_with_js

# Playfair Digraph Formatting
def format_playfair_input(text):
    text = text.lower().replace(" ", "").replace("j", "i")
    formatted_text = ""
    i = 0
    while i < len(text):
        formatted_text += text[i]
        if i + 1 < len(text) and text[i] != text[i + 1]:
            formatted_text += text[i + 1]
            i += 2
        else:
            formatted_text += 'x' if text[i] != 'x' else 'z'
            i += 1
    if len(formatted_text) % 2 != 0:
        formatted_text += 'x'
    digraphs = [formatted_text[i:i+2] for i in range(0, len(formatted_text), 2)]
    print("Formatted Playfair Digraphs:", digraphs)
    return digraphs

# Randomize and Derandomize functions
def randomize_text(text, seed):
    random.seed(seed)
    text_list = list(text)
    random.shuffle(text_list)
    result = "".join(text_list)
    print("Randomized Text:", result)
    return result

def derandomize_text(text, seed):
    random.seed(seed)
    indices = list(range(len(text)))
    random.shuffle(indices)
    result = [""] * len(text)
    for i, index in enumerate(indices):
        result[index] = text[i]
    final_result = "".join(result)
    print("Derandomized Text:", final_result)
    return final_result

# Main process with step-by-step output
plaintext = "I HAVE 22 LOVE STORIES"
key = "THISISALONGKEYWITHOUTNUMBERS"

# Preprocess text to remove special characters and get space positions
space_positions, plaintext_no_spaces = preprocess_text(plaintext)

# Vigenère encryption using Fibonacci-indexed characters
vigenere_encrypted = encrypt_vigenere(plaintext_no_spaces, key)

# ASCII addition to generate new key for Playfair matrix
non_fib_key = non_fibonacci_indexed_chars(key)
ascii_added_key = add_ascii_chars(vigenere_encrypted, non_fib_key)

# Generate Playfair matrix using the new ASCII-summed key
matrix = generate_playfair_matrix(ascii_added_key)

# Playfair encryption on the Vigenère output
playfair_encrypted, j_to_i_positions = encrypt_playfair(matrix, vigenere_encrypted)

# Randomization
randomized_text = randomize_text(playfair_encrypted, key)

# Decryption process
derandomized_text = derandomize_text(randomized_text, key)
playfair_decrypted = decrypt_playfair(matrix, derandomized_text, j_to_i_positions)

# Correct Vigenère decryption step
vigenere_decrypted = decrypt_vigenere(playfair_decrypted, key)

# Add spaces back to final decrypted text
final_decrypted_text_with_spaces = add_spaces_to_text(vigenere_decrypted, space_positions)

print("Final Decrypted Text:", final_decrypted_text_with_spaces)
