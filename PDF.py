import streamlit as st
from PIL import Image
import io
from fpdf import FPDF

st.set_page_config(page_title="Image to PDF Converter", layout="centered")
st.title("📄 Image to PDF Converter (500MB Supported)")

uploaded_file = st.file_uploader(
    "Upload Image", 
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    # 500MB limit
    if uploaded_file.size > 500 * 1024 * 1024:
        st.error("❌ File must be under 500MB!")
        st.stop()

    # Open the image
    try:
        img = Image.open(uploaded_file)
    except:
        st.error("❌ Invalid image!")
        st.stop()

    # Show image
    st.image(img, caption="Uploaded Image", use_container_width=True)

    # Convert to RGB
    if img.mode != "RGB":
        img = img.convert("RGB")

    # A4 size (points)
    max_width = 595
    max_height = 842

    # Auto resize while maintaining ratio
    img.thumbnail((max_width, max_height), Image.LANCZOS)

    # Convert to bytes for PDF
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    # Create PDF
    pdf = FPDF(unit="pt", format=[max_width, max_height])
    pdf.add_page()
    pdf.image(img_bytes, x=0, y=0, w=max_width, h=max_height)

    # Export PDF → returns bytearray
    pdf_bytearray = pdf.output(dest="S")

    # Convert bytearray to bytes
    pdf_bytes = bytes(pdf_bytearray)

    st.success("✅ PDF is ready!")

    # Download button (works 100%)
    st.download_button(
        label="⬇ Download PDF",
        data=pdf_bytes,
        file_name="converted.pdf",
        mime="application/pdf"
    )
