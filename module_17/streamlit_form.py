import streamlit as st

with st.form("my_form", clear_on_submit=True):
    name = st.text_input("Enter your name")
    age = st.slider("Enter your age", min_value=0, max_value=100)
    email = st.text_input("Enter your email")
    biography = st.text_area("Enter your biography")
    terms = st.checkbox("I agree to terms and conditions")
    submit_button = st.form_submit_button(label="Submit")

if submit_button:
    st.write(f"Name: {name}")
    st.write(f"Age: {age}")
    st.write(f"Email: {email}")
    st.write(f"Biography: {biography}")
    if terms:
        st.write("You agree to terms and conditions")
    else:
        st.write("You did not agree to terms and conditions")