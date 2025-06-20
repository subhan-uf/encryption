# Custom Encryption Method

This repository contains a Python implementation of a multi–stage encryption scheme developed by the original author of this project. The code was written as a personal exploration of cryptographic ideas and combines well–known techniques in a unique sequence. While it is an original effort, the scheme has not undergone expert review or formal security evaluation.

## Overview

The program in `nis_1.py` performs the following steps:

1. **Text Preprocessing**
   - Removes non–alphabetic characters and stores the original space positions so they can be restored later.

2. **Vigenère Encryption with Fibonacci–Indexed Key**
   - Extracts characters from the provided key at Fibonacci sequence positions and uses the resulting string as the Vigenère key to encrypt the plaintext.

3. **Generating a New Key**
   - Characters from the original key that are not at Fibonacci positions are combined with the Vigenère output by adding their ASCII values (modulo 26). This yields a new key used to create a Playfair matrix.

4. **Playfair Encryption**
   - A standard 5×5 Playfair matrix is generated from the new key. The text from the Vigenère step is then encrypted with Playfair, tracking any `j` to `i` substitutions for accurate decryption later.

5. **Randomization**
   - The resulting Playfair text is shuffled using Python's random module with the original key as the seed. This step can be reversed with the same key during decryption.

6. **Decryption Process**
   - The operations are reversed in the following order: derandomize, Playfair decrypt, Vigenère decrypt, and finally spaces are reinserted to reconstruct the original message.

## Usage

Run the script directly with Python 3:

```bash
python nis_1.py
```

The current implementation contains hardcoded plaintext and key values near the bottom of the script. You can modify these variables to experiment with different inputs.

## Disclaimer

This encryption method was solely created by the repository owner as a learning project. The approach combines known ciphers in a novel way, but it has **not** been vetted by professional cryptographers. Consequently, no guarantees are made about its resistance to cryptanalysis or real‑world attacks. Use it for educational purposes only and not for securing sensitive data.

## Repository Contents

- `nis_1.py` – Implementation of the encryption and decryption workflow described above.
- `tempCodeRunnerFile.py` – Temporary file likely generated by an editor. It is not required for the encryption process.

