import streamlit as st
from PIL import Image
import numpy as np

st.set_page_config(
    page_title="VisionBlaze",
    page_icon="👁",
    layout="wide"
)

st.title("👁 VisionBlaze")
st.subheader("Interactive Computer Vision Playground")

st.markdown("""
VisionBlaze enables **real-time image processing**,  
**visual feature extraction**, and **CV experimentation**.
""")

st.divider()

tab1, tab2, tab3 = st.tabs([
    "🖼 Image Processing",
    "🔍 Feature Detection",
    "🧩 Segmentation"
])

with tab1:
    st.header("🖼 Image Processing")
    img = st.file_uploader("Upload image", type=["jpg", "png"])
    if img:
        image = Image.open(img)
        st.image(image, caption="Original Image")

with tab2:
    st.header("🔍 Feature Detection")
    st.info("Add edge / face detection logic here")

with tab3:
    st.header("🧩 Image Segmentation")
    st.info("Add segmentation logic here")
