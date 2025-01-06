import streamlit as st
from PIL import Image
from LeastSignificantBit import LeastSignificantBit
import io

# App title
st.title("LSB Steganography")

# Sidebar options
option = st.sidebar.selectbox(
    "Choose an Option", ["Embed Message", "Extract Message"])

# Initialize LeastSignificantBit class
k_val = st.sidebar.slider("Number of LSBs (k_val)",
                          min_value=1, max_value=8, value=2)
lsb = LeastSignificantBit(k_val=k_val)

# Initialize session state
if "embed_done" not in st.session_state:
    st.session_state.embed_done = False

if option == "Embed Message":
    st.header("Embed a Message into an Image")

    if not st.session_state.embed_done:
        # Upload the input image
        uploaded_image = st.file_uploader(
            "Upload an Image", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image Preview",
                     use_column_width=True)

        # Input the message to embed
        message = st.text_area("Enter the Message to Embed")
        st.info(
            f"Message Length: {len(message)} characters")

        if uploaded_image and message:
            output_file_name = st.text_input(
                "Output File Name", value="stego_image")
            
            output_file_name = f"{output_file_name}.png" if not output_file_name.endswith(
                ".png") else output_file_name

            if st.button("Embed Message"):
                try:
                    input_image = Image.open(uploaded_image)
                    # Save uploaded image for processing
                    input_image.save("temp_input_image.png")

                    # Embed the message
                    stego_image = lsb.embed_message(
                        "temp_input_image.png", output_file_name, message)

                    st.session_state.embed_done = True  # Mark embedding as done
                    st.session_state.stego_image = stego_image  # Store the stego image
                    st.session_state.output_file_name = output_file_name  # Store output file name

                    st.success(
                        f"Message successfully embedded! Stego image saved as {output_file_name}")
                except Exception as e:
                    st.error(f"An error occurred: {e}")
    else:
        # Display the stego image preview and download button
        stego_image = st.session_state.stego_image
        st.image(stego_image, caption="Stego Image Preview",
                 use_column_width=True)

        # Prepare the image for download
        buffer = io.BytesIO()
        stego_image.save(buffer, format="PNG")
        buffer.seek(0)  # Reset the pointer to the start of the buffer

        st.download_button(
            label="Download Stego Image",
            data=buffer.getvalue(),  # Get the binary data for download
            file_name=st.session_state.output_file_name,
            mime="image/png",
        )

        # Option to start over
        if st.button("Start Over"):
            st.session_state.embed_done = False
            st.session_state.stego_image = None
            st.session_state.output_file_name = None
            st.rerun()

elif option == "Extract Message":
    st.header("Extract a Message from an Image")

    # Upload the stego image
    stego_image = st.file_uploader(
        "Upload a Stego Image", type=["png", "jpg", "jpeg"])
    if stego_image:
        st.image(stego_image, caption="Uploaded Stego Image Preview",
                 use_column_width=True)

    if stego_image:
        if st.button("Extract Message"):
            try:
                uploaded_stego_image = Image.open(stego_image)
                # Save uploaded image for processing
                uploaded_stego_image.save("temp_stego_image.png")

                # Extract the message
                extracted_message = lsb.extract_message("temp_stego_image.png")

                st.success("Message successfully extracted!")
                st.text_area("Extracted Message",
                             extracted_message, height=200)
                st.info(
                    f"Extracted Message Length: {len(extracted_message)} characters")
            except Exception as e:
                st.error(f"An error occurred: {e}")

# Footer
st.sidebar.info("Built with LeastSignificantBit Steganography")
