import streamlit as st
from EllipticCurveElGamal import EllipticCurveElGamal  # Import EllipticCurveElGamal

# Cached function to initialize ECC instance


@st.cache_resource
def initialize_ecc():
    return EllipticCurveElGamal()

# Cached function to generate keys


@st.cache_data
def generate_keys():
    ecc_instance = initialize_ecc()
    return ecc_instance.generate_keys()


# Initialize ECC instance
ecc = initialize_ecc()

# Initialize session state
if "ciphertext" not in st.session_state:
    st.session_state["ciphertext"] = None
if "public_key" not in st.session_state:
    st.session_state["public_key"] = None
if "private_key" not in st.session_state:
    st.session_state["private_key"] = None
if "decrypted_data" not in st.session_state:
    st.session_state["decrypted_data"] = None

# App title
st.title("Elliptic Curve ElGamal Encryption & Decryption")

# Sidebar for Key Management
st.sidebar.subheader("Key Management")

# Key generation button
if st.sidebar.button("Generate Keys"):
    st.cache_data.clear()
    st.cache_resource.clear()
    
    private_key, public_key = generate_keys()
    st.session_state["private_key"] = private_key
    st.session_state["public_key"] = public_key
    st.sidebar.success("Keys generated successfully!")

# Display current keys
if st.session_state["private_key"] and st.session_state["public_key"]:
    st.sidebar.subheader("Current Keys")
    st.sidebar.write(f"**Private Key:** {st.session_state['private_key']}")
    st.sidebar.write(f"**Public Key:** {st.session_state['public_key']}")
else:
    st.sidebar.warning("Generate keys first to proceed with encryption.")

# Input Data Section
st.subheader("Input Message to Encrypt")

message = st.text_area(
    "Enter the message", placeholder="Type your message here..."
)
if message:
    st.write(f"Message to Encrypt: **{message}**")
    st.write(f"Message Length: **{len(message)} characters**")

# Encrypt Data
if message and st.session_state["public_key"]:
    st.subheader("Encrypt Message")

    if st.button("Encrypt"):
        try:
            st.session_state["ciphertext"] = ecc.encrypt_message(
                message, st.session_state["public_key"]
            )
            st.success("Message encrypted successfully!")
        except Exception as e:
            st.error(f"Encryption failed: {e}")

    # Display ciphertext
    if st.session_state["ciphertext"]:
        st.subheader("Ciphertext")
        st.code(str(st.session_state["ciphertext"]), language="text")
        st.write(
            f"**Ciphertext Length:** {len(str(st.session_state['ciphertext']))} characters"
        )

# Decrypt Data
if st.session_state["ciphertext"]:
    st.subheader("Decrypt Message")

    # Input the private key for decryption
    input_private_key = st.text_input(
        "Enter the private key for decryption", type="password"
    )

    if input_private_key:
        try:
            input_private_key = int(input_private_key)
            if st.button("Decrypt"):
                st.session_state["decrypted_data"] = ecc.decrypt_message(
                    st.session_state["ciphertext"], input_private_key
                )
                st.success("Message decrypted successfully!")
        except ValueError:
            st.error("Invalid private key. Please enter a numeric value.")
        except Exception as e:
            st.error(f"Decryption failed: {e}")

    # Display decrypted data
    if st.session_state["decrypted_data"]:
        st.subheader("Decrypted Message")
        st.write(f"**Decrypted Data:** {st.session_state['decrypted_data']}")
        st.write(
            f"**Length of Decrypted Data:** {len(st.session_state['decrypted_data'])} characters"
        )

# Restart Process and Clear Cache
if st.button("Start Over"):
    for key in st.session_state.keys():
        del st.session_state[key]

    # Clear cached data and resources
    st.cache_data.clear()
    st.cache_resource.clear()

    st.rerun()
