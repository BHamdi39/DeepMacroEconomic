"""Probe — أبسط تطبيق لتحديد هل المشكلة في السحابة أم في التطبيق نفسه؟"""
import streamlit as st

st.set_page_config(page_title="Probe", page_icon="🧪")
if "__bk0" not in st.query_params:
    st.query_params["__bk0"] = "ran"

st.write("Probe OK — إذا رأيت هذا السطر فالتطبيق يعمل.")
st.metric("value", 42)