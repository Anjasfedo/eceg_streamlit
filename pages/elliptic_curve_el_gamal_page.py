import streamlit as st
from DummyKTPGenerator import DummyKTPGenerator  # Import DummyKTPGenerator
from EllipticCurveElGamal import EllipticCurveElGamal  # Import EllipticCurveElGamal

# Initialize instances
ktp_generator = DummyKTPGenerator()
ecc = EllipticCurveElGamal()

# Initialize session state
if "ktp_data" not in st.session_state:
    st.session_state["ktp_data"] = None
if "ciphertext" not in st.session_state:
    st.session_state["ciphertext"] = None
if "private_key" not in st.session_state:
    st.session_state["private_key"] = None
if "public_key" not in st.session_state:
    st.session_state["public_key"] = None
if "decrypted_data" not in st.session_state:
    st.session_state["decrypted_data"] = None
if "merged_data" not in st.session_state:
    st.session_state["merged_data"] = None

# App title
st.title("Elliptic Curve ElGamal Encryption with Single KTP Record")

# Input KTP Data: Manual or Automatic
st.subheader("Input KTP Data")

input_method = st.radio(
    "Input Method", ["Manual Input", "Automatic Generation"])

if input_method == "Manual Input":
    st.subheader("Enter KTP Details")
    # Use columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        nik = st.text_input("NIK", placeholder="Enter NIK")
        nama = st.text_input("Nama", placeholder="Enter Name")
        tempat_tgl_lahir = st.text_input(
            "Tempat/Tgl Lahir", placeholder="City, DD-MM-YYYY")
        jenis_kelamin = st.selectbox(
            "Jenis Kelamin", ["", "Laki-Laki", "Perempuan"], index=0)
        gol_darah = st.selectbox(
            "Golongan Darah", ["", "A", "B", "AB", "O"], index=0)

    with col2:
        agama = st.selectbox("Agama", [
                             "", "Islam", "Kristen", "Katolik", "Hindu", "Buddha", "Konghucu"], index=0)
        status_perkawinan = st.selectbox(
            "Status Perkawinan", ["", "Belum Kawin", "Kawin", "Cerai Hidup", "Cerai Mati"], index=0
        )
        pekerjaan = st.text_input("Pekerjaan", placeholder="Enter Job Title")
        kewarganegaraan = st.text_input(
            "Kewarganegaraan", placeholder="Enter Nationality (e.g., WNI)")
        berlaku_hingga = st.text_input(
            "Berlaku Hingga", placeholder="Enter Expiry (e.g., SEUMUR HIDUP)")

    # Address details
    st.subheader("Address Details")
    alamat = st.text_area("Alamat", placeholder="Enter Address")
    rt_rw = st.text_input("RT/RW", placeholder="Format: RT/RW")
    kel_desa = st.text_input(
        "Kel/Desa", placeholder="Enter Village/Subdistrict")

    # Collect input into a dictionary
    if st.button("Submit Manual Data"):
        st.session_state["ktp_data"] = {
            "NIK": nik,
            "Nama": nama,
            "Tempat/Tgl Lahir": tempat_tgl_lahir,
            "Jenis Kelamin": jenis_kelamin,
            "Gol Darah": gol_darah,
            "Alamat": alamat,
            "RT/RW": rt_rw,
            "Kel/Desa": kel_desa,
            "Agama": agama,
            "Status Perkawinan": status_perkawinan,
            "Pekerjaan": pekerjaan,
            "Kewarganegaraan": kewarganegaraan,
            "Berlaku Hingga": berlaku_hingga,
        }
        st.success("Manual KTP data submitted successfully!")

elif input_method == "Automatic Generation":
    if st.button("Generate Automatic Data"):
        st.session_state["ktp_data"] = ktp_generator.generate_ktp()
        st.success("Generated KTP data successfully!")

# Show KTP Data
if st.session_state["ktp_data"] is not None:
    st.subheader("Review KTP Data")
    ktp = st.session_state["ktp_data"]
    for key, value in ktp.items():
        st.write(f"- **{key}:** {value}")

    # Merge KTP data for encryption
    st.session_state["merged_data"] = DummyKTPGenerator.merge_ktp_data(ktp)
    st.subheader("Merged KTP Data")
    st.code(st.session_state["merged_data"], language="text", wrap_lines=True)
    st.write(
        f"**Length of Merged Data:** {len(st.session_state['merged_data'])}")

# Encrypt KTP Data
if st.session_state["ktp_data"] is not None:
    st.subheader("Encrypt KTP Data")

    if st.button("Encrypt Data"):
        # Generate keys
        private_key, public_key = ecc.generate_keys()
        st.session_state["private_key"] = private_key
        st.session_state["public_key"] = public_key

        # Encrypt data
        plaintext = st.session_state["merged_data"]
        st.session_state["ciphertext"] = ecc.encrypt_message(
            plaintext, public_key)
        st.success("Data encrypted successfully!")

    if st.session_state["ciphertext"]:
        st.subheader("Ciphertext")
        st.write("**Ciphertext:**")
        st.code(str(st.session_state["ciphertext"]),
                language="text", wrap_lines=True)
        st.write(
            f"**Length of Ciphertext:** {len(str(st.session_state['ciphertext']))}")

# Decrypt KTP Data
if st.session_state["ciphertext"] is not None:
    st.subheader("Decrypt KTP Data")

    if st.button("Decrypt Data"):
        st.session_state["decrypted_data"] = ecc.decrypt_message(
            st.session_state["ciphertext"], st.session_state["private_key"]
        )
        st.success("Data decrypted successfully!")

    if st.session_state["decrypted_data"]:
        st.subheader("Decrypted KTP Data")
        st.write("**Decrypted Data:**")
        st.code(st.session_state["decrypted_data"],
                language="text", wrap_lines=True)
        st.write(
            f"**Length of Decrypted Data:** {len(st.session_state['decrypted_data'])}")

# Restart Process
if st.button("Start Over"):
    st.session_state["ktp_data"] = None
    st.session_state["ciphertext"] = None
    st.session_state["private_key"] = None
    st.session_state["public_key"] = None
    st.session_state["decrypted_data"] = None
    st.session_state["merged_data"] = None
    st.rerun()
