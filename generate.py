import streamlit as st
import barcode
from barcode.writer import ImageWriter, SVGWriter
from io import BytesIO
import base64

st.set_page_config(page_title="Barcode Generator")

def generate_barcode_bytes(data, file_format):
    code128 = barcode.get_barcode_class('code128')
    writer = ImageWriter() if file_format.lower() == 'jpg' else SVGWriter()

    options = {
        'module_height': 15.24,
        'module_width': 0.25,
        'quiet_zone': 2.0,
        'write_text': False,
        'dpi': 300
    }

    rv = BytesIO()
    bc = code128(str(data), writer=writer)
    bc.write(rv, options=options)
    rv.seek(0)
    return rv

st.title("Barcode Generator")

col1, col2 = st.columns([2, 1])
with col1:
    barcode_data = st.text_input("Enter Barcode Number", placeholder="e.g. 123456789")
with col2:
    file_format = st.selectbox("Select Format", ["SVG", "JPG"])

if barcode_data:
    try:
        barcode_bytes = generate_barcode_bytes(barcode_data, file_format)
        st.divider()
        
        st.write("### Preview")
        if file_format == "SVG":
            svg_data = barcode_bytes.getvalue().decode("utf-8")
            b64_svg = base64.b64encode(svg_data.encode("utf-8")).decode("utf-8")
            data_uri = f"data:image/svg+xml;base64,{b64_svg}"
            
            st.iframe(data_uri, height=200)
        else:
            st.image(barcode_bytes, caption=f"Preview: {barcode_data}")

        barcode_bytes.seek(0)
        extension = file_format.lower()
        mime_type = "image/jpeg" if extension == "jpg" else "image/svg+xml"
        
        st.download_button(
            label=f"Download {file_format}",
            data=barcode_bytes,
            file_name=f"barcode_{barcode_data}.{extension}",
            mime=mime_type
        )

    except Exception as e:
        st.error(f"Could not generate barcode: {e}")
