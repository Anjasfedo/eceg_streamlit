import streamlit as st
from DummyKTPGenerator import DummyKTPGenerator
from EllipticCurveElGamal import EllipticCurveElGamal
from HuffmanEncoding import HuffmanEncoding
from LampelZivWelch import LampelZivWelch
from LeastSignificantBit import LeastSignificantBit
from PIL import Image
import io
import pickle

# Initialize modules
ktp_generator = DummyKTPGenerator()

# Cached functions for ECC


@st.cache_resource
def initialize_ecc():
    return EllipticCurveElGamal()


@st.cache_data
def generate_keys():
    ecc_instance = initialize_ecc()
    return ecc_instance.generate_keys()


ecc = initialize_ecc()

# Streamlit App Title
st.title("Integrated Encryption, Compression, and Steganography App")

# Sidebar: ECC Key Management
st.sidebar.header("Key Management")
if "private_key" not in st.session_state:
    st.session_state["private_key"] = None
if "public_key" not in st.session_state:
    st.session_state["public_key"] = None

# Key generation button
if st.sidebar.button("Generate ECC Keys"):
    st.cache_data.clear()
    st.cache_resource.clear()
    st.session_state["private_key"], st.session_state["public_key"] = generate_keys()
    st.sidebar.success("Keys generated successfully!")

# Display current keys in the sidebar
if st.session_state["private_key"] and st.session_state["public_key"]:
    st.sidebar.subheader("Current Keys")
    st.sidebar.write(f"**Private Key:** {st.session_state['private_key']}")
    st.sidebar.write(f"**Public Key:** {st.session_state['public_key']}")
else:
    st.sidebar.warning("Generate ECC keys to proceed.")

# Sidebar: LSB Configuration
st.sidebar.subheader("LSB Configuration")
k_val = st.sidebar.slider("Number of LSBs (k_val)",
                          min_value=1, max_value=8, value=4)
lsb = LeastSignificantBit(k_val=k_val)

# Sidebar Navigation
app_mode = st.sidebar.selectbox(
    "Choose a Mode",
    ["Generate, Encrypt & Embed", "Extract, Decrypt & Recover"]
)

### GENERATE, ENCRYPT & EMBED ###
if app_mode == "Generate, Encrypt & Embed":
    st.header("Generate, Encrypt, and Embed Data")

    # Step 1: Input or Generate KTP Data
    st.subheader("1. Input Text or Generate KTP Data")
    user_text = st.text_area(
        "Enter text to encrypt, or leave blank to generate KTP data:"
    )

    if not user_text:
        num_records = st.slider("Number of KTPs to generate", 1, 10, 1)
        generated_data = ktp_generator.generate_multiple_ktps(
            count=num_records)
        user_text = '\n'.join([ktp_generator.merge_ktp_data(ktp)
                              for ktp in generated_data])
        st.write("Generated KTP Data:")
        st.code(user_text)

    # Step 2: Encrypt the Data
    st.subheader("2. Encrypt Data with Elliptic Curve ElGamal (ECEG)")
    if st.session_state["private_key"] and st.session_state["public_key"]:
        if st.button("Encrypt"):
            ciphertext = ecc.encrypt_message(
                user_text, st.session_state["public_key"])
            st.session_state["ciphertext"] = ciphertext
            st.success("Data encrypted successfully!")
            st.code(ciphertext, language="text")
    else:
        st.warning("Generate ECC keys to proceed with encryption.")

    # Step 3: Optional Compression
    st.subheader("3. Optional: Compress the Encrypted Data")
    compress_option = st.radio("Choose compression method:", [
                               "None", "Huffman", "LZW"])
    if compress_option != "None" and "ciphertext" in st.session_state:
        if compress_option == "Huffman":
            compressed_data, codebook, huffman_tree, padding = HuffmanEncoding.build_huffman(
                st.session_state["ciphertext"]
            )
            st.session_state["compressed_data"] = compressed_data

            # Save Huffman tree and padding as a file
            huffman_bundle = {"huffman_tree": huffman_tree, "padding": padding}
            huffman_file = io.BytesIO()
            pickle.dump(huffman_bundle, huffman_file)
            huffman_file.seek(0)

            st.success("Data compressed with Huffman Encoding!")
            st.code(compressed_data, language="text")

            # Download Huffman tree and padding
            st.download_button(
                label="Download Huffman Tree and Padding",
                data=huffman_file,
                file_name="huffman_tree_padding.pkl",
                mime="application/octet-stream",
            )
        elif compress_option == "LZW":
            compressed_data = LampelZivWelch().compress(
                st.session_state["ciphertext"])
            st.session_state["compressed_data"] = compressed_data
            st.success("Data compressed with LZW Compression!")
            st.code(compressed_data, language="text")

    # Step 4: Embed into an Image
    st.subheader("4. Embed Data into an Image")
    uploaded_image = st.file_uploader(
        "Upload an image to embed the data:", type=["png", "jpg", "jpeg"]
    )
    if uploaded_image and "ciphertext" in st.session_state:
        # Read the uploaded image
        input_image = Image.open(uploaded_image)
        st.image(input_image, caption="Uploaded Image Preview",
                 use_column_width=True)

        # Calculate maximum message length
        img_width, img_height = input_image.size
        color_channels = len(input_image.getbands())
        max_message_length = (
            (img_width * img_height * color_channels * k_val) - 1) // 8
        st.info(f"Maximum Message Length: {max_message_length} characters")

        # Input the message to embed
        data_to_embed = (
            st.session_state["compressed_data"]
            if compress_option != "None"
            else st.session_state["ciphertext"]
        )
        output_file_name = st.text_input(
            "Output File Name", value="stego_image.png")

        if len(data_to_embed) > max_message_length:
            st.error("Data exceeds the maximum length!")
        elif st.button("Embed Message"):
            try:
                # Embed the message
                buffer = io.BytesIO()
                input_image.save(buffer, format="PNG")
                buffer.seek(0)
                stego_image = lsb.embed_message(
                    buffer, output_file_name, data_to_embed)

                st.success("Data embedded into the image successfully!")
                st.image(stego_image, caption="Stego Image Preview",
                         use_column_width=True)

                # Prepare stego image for download
                buffer = io.BytesIO()
                stego_image.save(buffer, format="PNG")
                buffer.seek(0)

                st.download_button(
                    label="Download Stego Image",
                    data=buffer.getvalue(),
                    file_name="stego_image.png",
                    mime="image/png",
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")


### EXTRACT, DECRYPT & RECOVER ###
elif app_mode == "Extract, Decrypt & Recover":
    st.header("Extract, Decrypt, and Recover Data")

    # Step 1: Extract Data from an Image
    st.subheader("1. Extract Data from an Image")
    uploaded_stego_image = st.file_uploader(
        "Upload the stego image:", type=["png", "jpg", "jpeg"])
    if uploaded_stego_image:
        stego_image = Image.open(uploaded_stego_image)
        st.image(stego_image, caption="Stego Image Preview",
                 use_column_width=True)

        # Prepare the stego image as a binary stream
        buffer = io.BytesIO()
        stego_image.save(buffer, format="PNG")
        buffer.seek(0)

        if st.button("Extract Message"):
            try:
                # Extract message
                extracted_data = lsb.extract_message(buffer)
                st.session_state["extracted_data"] = extracted_data
                st.success("Message extracted successfully!")
                st.code(extracted_data, language="text")
            except Exception as e:
                st.error(f"An error occurred: {e}")

    # Step 2: Decompress Data
    st.subheader("2. Optional: Decompress the Data")
    decompress_option = st.radio("Choose decompression method:", [
                                 "None", "Huffman", "LZW"])
    if decompress_option != "None" and "extracted_data" in st.session_state:
        if decompress_option == "Huffman":
            uploaded_huffman_file = st.file_uploader(
                "Upload Huffman Tree and Padding File", type="pkl"
            )
            if uploaded_huffman_file:
                huffman_bundle = pickle.load(uploaded_huffman_file)
                huffman_tree = huffman_bundle["huffman_tree"]
                padding = huffman_bundle["padding"]

                decompressed_data = HuffmanEncoding.decode(
                    st.session_state["extracted_data"], huffman_tree, padding
                )
                st.session_state["decompressed_data"] = decompressed_data
                st.success("Data decompressed with Huffman Decoding!")
                st.code(decompressed_data, language="text")
        elif decompress_option == "LZW":
            decompressed_data = LampelZivWelch().decompress(
                st.session_state["extracted_data"])
            st.session_state["decompressed_data"] = decompressed_data
            st.success("Data decompressed with LZW!")
            st.code(decompressed_data, language="text")

    # Step 3: Decrypt Data
    st.subheader("3. Decrypt the Data")
    if "decompressed_data" in st.session_state or "extracted_data" in st.session_state:
        data_to_decrypt = st.session_state.get(
            "decompressed_data", st.session_state["extracted_data"]
        )
        private_key_input = st.text_input(
            "Enter your private key:", type="password")
        if private_key_input and st.button("Decrypt"):
            try:
                decrypted_data = ecc.decrypt_message(
                    data_to_decrypt, int(private_key_input))
                st.success("Data decrypted successfully!")
                st.text_area("Decrypted Message:", decrypted_data, height=200)
            except Exception as e:
                st.error(f"Decryption failed: {e}")
