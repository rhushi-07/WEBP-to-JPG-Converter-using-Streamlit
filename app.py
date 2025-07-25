import streamlit as st
from PIL import Image
import io
import zipfile

st.set_page_config(page_title="WEBP to JPG Converter", layout="centered")

st.title("🖼️ Convert WEBP files to JPG")
st.write("Upload multiple `.webp` files and convert them into `.jpg` format.")

uploaded_files = st.file_uploader("Choose WEBP files", type=["webp"], accept_multiple_files=True)

if uploaded_files:
    converted_images = []
    
    for uploaded_file in uploaded_files:
        try:
            image = Image.open(uploaded_file).convert("RGB")
            buffer = io.BytesIO()
            image.save(buffer, format="JPEG")
            buffer.seek(0)
            converted_images.append((uploaded_file.name.replace('.webp', '.jpg'), buffer))
            st.success(f"Converted: {uploaded_file.name}")
        except Exception as e:
            st.error(f"Failed to convert {uploaded_file.name}: {e}")

    if converted_images:
        # Option to download images individually
        st.subheader("Download Converted Images")
        for filename, img_buffer in converted_images:
            st.download_button(label=f"📥 Download {filename}", data=img_buffer, file_name=filename, mime="image/jpeg")

        # Option to download all as zip
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zip_file:
            for filename, img_buffer in converted_images:
                zip_file.writestr(filename, img_buffer.getvalue())
        zip_buffer.seek(0)

        st.download_button(
            label="📦 Download All as ZIP",
            data=zip_buffer,
            file_name="converted_images.zip",
            mime="application/zip"
        )
