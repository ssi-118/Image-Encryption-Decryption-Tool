# app.py
import streamlit as st

from crypto_utils import encrypt_ecb, decrypt_ecb, encrypt_cbc, decrypt_cbc
from image_utils import load_image, image_to_bytes, bytes_to_image


st.set_page_config(
    page_title="Visual Cryptography Sandbox",
    page_icon="lock",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, #ff8a8a 0, transparent 28%),
            radial-gradient(circle at top right, #7dd3fc 0, transparent 25%),
            linear-gradient(135deg, #111827 0%, #1f2937 45%, #0f172a 100%);
        color: #f9fafb;
    }

    h1, h2, h3 {
        color: #ffffff;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827, #312e81);
        border-right: 1px solid rgba(255,255,255,0.15);
    }

    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span {
        color: #f9fafb;
    }

    .hero-box {
        padding: 28px;
        border-radius: 18px;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.18);
        backdrop-filter: blur(10px);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #d1d5db;
        max-width: 850px;
    }

    .mode-card {
        padding: 16px;
        border-radius: 14px;
        background: rgba(255,255,255,0.09);
        border: 1px solid rgba(255,255,255,0.14);
        margin-bottom: 16px;
    }

    .good {
        color: #86efac;
        font-weight: 700;
    }

    .bad {
        color: #fca5a5;
        font-weight: 700;
    }

    .image-label {
        text-align: center;
        padding: 10px;
        border-radius: 999px;
        font-weight: 700;
        margin-bottom: 10px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
    }

    div[data-testid="stFileUploader"] {
        padding: 18px;
        border-radius: 16px;
        background: rgba(255,255,255,0.09);
        border: 1px dashed rgba(255,255,255,0.35);
    }

    .stButton button,
    .stDownloadButton button {
        border-radius: 999px;
        border: none;
        background: linear-gradient(90deg, #fb7185, #38bdf8);
        color: white;
        font-weight: 700;
        padding: 0.65rem 1.2rem;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        transform: scale(1.02);
        color: white;
    }

    img {
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.18);
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">Visual Cryptography Sandbox</div>
        <div class="hero-subtitle">
            Encrypt and decrypt images using AES
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

with st.sidebar:
    st.header("Control Panel")

    encryption_password = st.text_input(
        "Set Encryption Password",
        type="password",
        placeholder="Create a secret password"
    )

    decryption_password = st.text_input(
        "Enter Password to Decrypt",
        type="password",
        placeholder="Use the same password"
    )

    cipher_mode = st.radio(
        "Choose Cipher Mode",
        ["AES-ECB", "AES-CBC"],
        horizontal=False
    )

    if cipher_mode == "AES-ECB":
        st.markdown(
            """
            <div class="mode-card">
                <span class="bad">ECB Mode</span><br>
                Fast, simple, but visually leaky. Patterns may still appear.
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div class="mode-card">
                <span class="good">CBC Mode</span><br>
                Stronger visual scrambling. Repeated patterns disappear.
            </div>
            """,
            unsafe_allow_html=True
        )


uploaded_file = st.file_uploader(
    "Drop in a PNG or JPEG image",
    type=["png", "jpg", "jpeg"]
)


if uploaded_file is None:
    st.info("Upload a clear image such as a logo, cartoon, flag, portrait, or Tux penguin image.")

else:
    if not encryption_password:
        st.error("Please set an encryption password first.")

    elif not decryption_password:
        st.error("Please enter a password to decrypt the image.")

    else:
        original_image = load_image(uploaded_file)
        pixel_data = image_to_bytes(original_image)

        try:
            if cipher_mode == "AES-ECB":
                encrypted_data = encrypt_ecb(pixel_data, encryption_password)
                decrypted_data = decrypt_ecb(encrypted_data, decryption_password)

            else:
                encrypted_data, iv = encrypt_cbc(pixel_data, encryption_password)
                decrypted_data = decrypt_cbc(encrypted_data, decryption_password, iv)

            encrypted_image = bytes_to_image(encrypted_data, original_image.size)
            decrypted_image = bytes_to_image(decrypted_data, original_image.size)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="image-label">Original Image</div>', unsafe_allow_html=True)
                st.image(original_image, use_container_width=True)

            with col2:
                st.markdown('<div class="image-label">Encrypted Pixels</div>', unsafe_allow_html=True)
                st.image(encrypted_image, use_container_width=True)

            with col3:
                st.markdown('<div class="image-label">Decrypted Result</div>', unsafe_allow_html=True)
                st.image(decrypted_image, use_container_width=True)

            st.divider()

            if encryption_password == decryption_password:
                st.success("Password matched. The decrypted image is restored.")
            else:
                st.warning("Password did not match. The decrypted image may look broken.")

            st.download_button(
                label="Download Encrypted Pixel Data",
                data=encrypted_data,
                file_name="encrypted_image_pixels.bin",
                mime="application/octet-stream"
            )

        except ValueError:
            st.error("Decryption failed. The password is incorrect.")