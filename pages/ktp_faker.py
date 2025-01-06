import streamlit as st
from DummyKTPGenerator import DummyKTPGenerator  # Import your package

# Streamlit App Title
st.title("Dummy KTP Generator")

# Sidebar Configuration
st.sidebar.header("Configuration")
num_records = st.sidebar.slider("Number of KTPs to generate", 1, 100, 10)

# Generator Instance
generator = DummyKTPGenerator()

# Generate KTPs
ktp_data = generator.generate_multiple_ktps(count=num_records)

# Display Results
st.subheader(f"Generated {num_records} Dummy KTP(s)")
for idx, ktp in enumerate(ktp_data, start=1):
    st.write(f"**KTP {idx}:**")
    st.json(ktp)

# Download Option
st.subheader("Download Generated Data")
if st.button("Generate CSV File"):
    import pandas as pd
    from io import BytesIO

    # Convert KTP data to DataFrame
    df = pd.DataFrame(ktp_data)

    # Convert DataFrame to CSV in-memory
    csv = BytesIO()
    df.to_csv(csv, index=False)

    # Download Button
    st.download_button(
        label="Download CSV",
        data=csv.getvalue(),
        file_name="dummy_ktp_data.csv",
        mime="text/csv",
    )
