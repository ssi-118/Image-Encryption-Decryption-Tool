# Visual Cryptography Sandbox

A beginner-friendly Streamlit web app that encrypts and decrypts images using AES.  
The project visually demonstrates how different AES modes affect image data, especially the difference between ECB and CBC.

## Features

- Upload PNG, JPG, or JPEG images
- Set a password for encryption
- Use the same password to decrypt the image
- Compare:
  - Original image
  - Encrypted image
  - Decrypted image
- Choose between:
  - AES-ECB
  - AES-CBC
- Download encrypted pixel data
- Fun Streamlit-based web interface

## Project Idea

Most encryption tools simply turn a file into unreadable encrypted data.

This project is different because it encrypts the raw image pixels and displays the encrypted result as an image. This makes it easier to understand how encryption affects visual data.

## AES Modes

### AES-ECB

ECB stands for Electronic Codebook.

In ECB mode, identical blocks of data produce identical encrypted blocks. Because of this, image patterns may still be visible after encryption.

### AES-CBC

CBC stands for Cipher Block Chaining.

In CBC mode, each block depends on the previous block, making the encrypted result look much more random. This hides repeated patterns better than ECB.

Note: AES-ECB should not be used for real-world secure encryption because it can leak patterns.

## Images You Can Use

Good demo images:

- Tux penguin image
- Logos
- Flags
- Cartoon images
- Icons
- Simple portraits
- Black-and-white drawings
- Images with plain backgrounds
- Pixel art

Avoid images that are too noisy, blurry, dark, or full of tiny details because the ECB pattern effect may be harder to see.

## Project Structure

```text
visual-cryptography-sandbox/
│
├── assets/
│   └── sample_images/
│       ├── cartoon.png
│       ├── flag.jpg
│       ├── logo.jpg
│       └── penguin.png
│
├── docs/
│   └── IED_IP_OP.docx
│
├── src/
│   ├── app.py
│   ├── crypto_utils.py
│   └── image_utils.py
│
├── requirements.txt
└── README.md
```

## Requirements

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

`requirements.txt`:

```text
streamlit
pillow
pycryptodome
numpy
```

## How To Run

Run the Streamlit app:

```bash
streamlit run src/app.py
```

Then open the local URL shown in the terminal.

Usually it will be:

```text
http://localhost:8501
```

## How To Use

1. Upload a PNG, JPG, or JPEG image.
2. Enter an encryption password.
3. Enter the same password again for decryption.
4. Select AES-ECB or AES-CBC.
5. View the original, encrypted, and decrypted images.
6. Download the encrypted pixel data if needed.

## Expected Output

The app displays three images:

```text
Original Image      Encrypted Image      Decrypted Image
```

If the correct password is used, the decrypted image should match the original image.

If the wrong password is used, decryption will fail or the decrypted image will look incorrect.

## Live Demo
