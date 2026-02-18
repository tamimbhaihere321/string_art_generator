import streamlit as st
import numpy as np
from PIL import Image, ImageOps
from io import BytesIO

from utils.layout import generate_pin_layout
from utils.algorithm import generate_string_art
from utils.export import (
    export_pins_csv,
    export_threads_csv,
    export_instructions_txt,
    generate_drill_template
)

st.set_page_config(layout="wide")
st.title("Professional String Art Generator")


# ---------- HELPER: NUMPY IMAGE → PNG BYTES ----------

def image_to_png_bytes(img_array):
    img = Image.fromarray(img_array.astype("uint8"))
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf.getvalue()


# ---------- SIDEBAR ----------

st.sidebar.header("IMAGE")
uploaded = st.sidebar.file_uploader("Upload portrait", type=["png","jpg","jpeg"])
invert = st.sidebar.checkbox("Invert image")

st.sidebar.header("BOARD (mm)")
board_w = st.sidebar.number_input("Width", 100, 2000, 400)
board_h = st.sidebar.number_input("Height", 100, 2000, 400)
margin = st.sidebar.number_input("Margin", 0, 200, 20)

st.sidebar.header("PINS")
pin_count = st.sidebar.slider("Number of pins", 50, 600, 300)
layout_type = st.sidebar.selectbox("Layout", ["circular","square"])

st.sidebar.header("THREAD")
thread_count = st.sidebar.slider("Thread lines", 100, 20000, 8000)
darkness = st.sidebar.slider("Darkness strength", 0.01, 1.0, 0.2)
thickness = st.sidebar.slider("Preview thickness", 1, 5, 1)

run = st.sidebar.button("Generate")


# ---------- MAIN ----------

if uploaded and run:

    # --- LOAD & PREPROCESS IMAGE ---
    gray = Image.open(uploaded).convert("L")
    gray = ImageOps.fit(gray, (800,800))
    gray = np.array(gray)

    if invert:
        gray = 255 - gray

    gray = gray.astype(np.float32)/255.0

    st.write("### Processing… please wait")

    # --- GENERATE PIN LAYOUT ---
    pins = generate_pin_layout(
        board_w, board_h, margin,
        pin_count, layout_type
    )

    # --- LIVE UI ELEMENTS ---
    progress_bar = st.progress(0)
    status_text = st.empty()
    live_preview = st.empty()

    def update_ui(progress, preview_img=None, step=None):
        progress_bar.progress(progress)
        if step:
            status_text.text(f"Generating threads… step {step}")
        if preview_img is not None:
            live_preview.image(
                preview_img,
                caption="Live Thread Mapping",
                use_container_width=True
            )

    # --- GENERATE STRING ART ---
    preview, threads = generate_string_art(
        gray,
        pins,
        thread_count,
        darkness,
        thickness,
        progress_callback=update_ui
    )

    st.success("Finished")

    # --- SHOW RESULTS ---
    col1, col2 = st.columns(2)

    with col1:
        st.image(preview, caption="Final String Art", use_container_width=True)

    with col2:
        template = generate_drill_template(board_w, board_h, pins)
        st.image(template, caption="Pin Layout Template", use_container_width=True)

    # --- EXPORT FILES ---
    pins_csv = export_pins_csv(pins)
    threads_csv = export_threads_csv(threads)
    txt = export_instructions_txt(threads)

    preview_bytes = image_to_png_bytes(preview)

    # --- DOWNLOAD BUTTONS ---
    st.download_button(
        "Download preview.png",
        data=preview_bytes,
        file_name="preview.png",
        mime="image/png"
    )

    st.download_button(
        "Download drill_template.png",
        data=template,
        file_name="drill_template.png",
        mime="image/png"
    )

    st.download_button(
        "Download pins.csv",
        data=pins_csv,
        file_name="pins.csv",
        mime="text/csv"
    )

    st.download_button(
        "Download threads.csv",
        data=threads_csv,
        file_name="threads.csv",
        mime="text/csv"
    )

    st.download_button(
        "Download thread_instructions.txt",
        data=txt,
        file_name="thread_instructions.txt",
        mime="text/plain"
    )
