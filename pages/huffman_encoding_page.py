import streamlit as st
# Ensure this module is implemented and available
from HuffmanEncoding import HuffmanEncoding
import pickle


def visualize_huffman_tree(node, prefix=""):
    """
    Recursively visualize the Huffman tree as a text-based structure.
    """
    if node.char is not None:  # Leaf node
        return f"{prefix} -> {node.char} ({node.freq})\n"

    result = ""
    if node.left:
        result += visualize_huffman_tree(node.left, prefix + "0")
    if node.right:
        result += visualize_huffman_tree(node.right, prefix + "1")
    return result


# App title
st.title("Huffman Encoding and Decoding")

# Sidebar
option = st.sidebar.selectbox(
    "Choose an Option", ["Encode Text", "Decode Text"])

# Encoding Section
if option == "Encode Text":
    st.header("Encode Text")

    # Input text
    input_text = st.text_area("Enter the Text to Encode", "")

    if input_text:
        try:
            # Perform Huffman encoding
            encoded_text, codebook, huffman_tree, padding = HuffmanEncoding.build_huffman(
                input_text)

            # Calculate compression ratio
            compression_ratio = HuffmanEncoding.get_compression_ratio(
                input_text, encoded_text)

            # Display results
            st.subheader("Encoded Text")
            st.code(encoded_text)

            st.subheader("Compression Ratio")
            st.write(f"**{compression_ratio:.2f}%** compression achieved.")

            st.subheader("Huffman Codebook")
            st.json(codebook)

            st.subheader("Huffman Tree")
            tree_representation = visualize_huffman_tree(huffman_tree)
            st.text(tree_representation)

            st.subheader("Padding Information")
            st.write(f"Padding Bits: {padding}")

            # Download encoded text
            st.download_button(
                label="Download Encoded Text",
                data=encoded_text,
                file_name="encoded_text.txt",
                mime="text/plain",
            )

            # Bundle Huffman tree and padding into one file
            bundle = {"huffman_tree": huffman_tree, "padding": padding}
            st.download_button(
                label="Download Huffman Tree and Padding",
                data=pickle.dumps(bundle),
                file_name="huffman_tree_padding.pkl",
                mime="application/octet-stream",
            )

        except Exception as e:
            st.error(f"An error occurred during encoding: {e}")

# Decoding Section
elif option == "Decode Text":
    st.header("Decode Text")

    # Input encoded text
    encoded_text = st.text_area("Enter the Encoded Text", "")

    # Upload bundled Huffman tree and padding file
    uploaded_bundle = st.file_uploader(
        "Upload Huffman Tree and Padding File", type="pkl")

    if encoded_text and uploaded_bundle:
        try:
            # Load bundled Huffman tree and padding
            bundle = pickle.loads(uploaded_bundle.read())
            huffman_tree = bundle["huffman_tree"]
            padding = bundle["padding"]

            # Decode the text
            decoded_text = HuffmanEncoding.decode(
                encoded_text, huffman_tree, int(padding))

            # Display results
            st.subheader("Decoded Text")
            st.code(decoded_text)

            # Validate
            st.write("Decompression successful.")

        except Exception as e:
            st.error(f"An error occurred during decoding: {e}")
    else:
        st.warning("Ensure all required inputs are provided for decoding.")

# Footer
st.sidebar.info("Built with Huffman Encoding Algorithm")
