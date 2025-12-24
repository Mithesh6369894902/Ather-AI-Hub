import streamlit as st

st.set_page_config(
    page_title="Ather AI Hub",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 Ather AI Hub")
st.caption("A Unified Platform for Data, Vision, NLP, ML & Finance")

module = st.sidebar.radio(
    "Select AI Engine",
    [
        "🏠 Home",
        "📊 InfernoData",
        "✍ TextVortex",
        "📈 AlphaFlux",
        "👁 VisionBlaze",
        "🤖 ModelCraft X"
    ]
)

def run_module(path):
    with open(path, "r", encoding="utf-8") as f:
        exec(f.read(), globals())

if module == "🏠 Home":
    st.markdown("""
    ## Welcome to **Ather AI Hub**
    
    A modular AI platform integrating:
    - Dataset Engineering (InfernoData)
    - NLP Analytics (TextVortex)
    - Financial Intelligence (AlphaFlux)
    - Computer Vision (VisionBlaze)
    - Machine Learning Modeling (ModelCraft X)
    
    Designed for **research, education, and real-world AI experimentation**.
    """)

elif module == "📊 InfernoData":
    run_module("modules/infernodata/app.py")

elif module == "✍ TextVortex":
    run_module("modules/textvortex/app.py")

elif module == "📈 AlphaFlux":
    run_module("modules/alphaflux/app.py")

elif module == "👁 VisionBlaze":
    run_module("modules/visionblaze/app.py")

elif module == "🤖 ModelCraft X":
    run_module("modules/modelcraftx/app.py")
