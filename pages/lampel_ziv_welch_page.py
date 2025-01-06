import streamlit as st
from LampelZivWelch import LampelZivWelch

# Initialize the LZW class
lzw = LampelZivWelch()

# App title
st.title("Lampel-Ziv-Welch (LZW) Compression and Decompression")

# Page selection
option = st.sidebar.selectbox(
    "Choose an Option", ["Compress a String", "Decompress a String"]
)

if option == "Compress a String":
    st.header("Compress a String")

    # Input text
    input_text = st.text_area("Enter the Text to Compress", "")

    if input_text:
        # Compress the text
        compressed_data = lzw.compress(input_text)

        # Calculate compression ratio
        compression_ratio = lzw.get_compression_ratio(
            input_text, compressed_data)

        # Display results
        st.subheader("Compressed Data")
        st.code(compressed_data)

        st.subheader("Compression Ratio")
        st.write(f"**{compression_ratio:.2f}%** compression achieved.")

        # Download compressed data
        st.download_button(
            label="Download Compressed Data",
            data=compressed_data,
            file_name="compressed_data.txt",
            mime="text/plain",
        )

if option == "Decompress a String":
    st.header("Decompress a String")

    # Input compressed text
    compressed_text = st.text_area("Enter the Compressed Data", "")

    if compressed_text:
        try:
            # Decompress the text
            decompressed_data = lzw.decompress(compressed_text)

            # Display results
            st.subheader("Decompressed Data")
            st.code(decompressed_data)

            # Validate
            st.write("Decompression successful.")
        except Exception as e:
            st.error(f"An error occurred during decompression: {e}")

# Footer
st.sidebar.info("Built with Lampel-Ziv-Welch Compression Algorithm")
