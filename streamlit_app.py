import streamlit as st
import giskard

st.title("🔍 Giskard Scanner App")
st.write("Giskard version:", giskard.__version__)

if st.button("Test"):
    st.success("Giskard est bien installé!")
