import streamlit as st

def main():
   st.title("Hello World")
   age = st.number_input("enter your age: ", min_value=0, max_value=100)
   st.write(f"Your age is: {age}")
   user_input1 = st.text_input("Enter text", "Sample text")
   st.write("You entered:", user_input1)
   if st.checkbox("Check me"):
       st.write("You're seeing this message because you checked the checkbox")
   if st.button("Click me"):
       st.write("Button Clicked!")
   message = st.text_area("Enter a message")
   st.write(f"You message: {message}")
   choice = st.radio("Pick one", ["Choice 1", "Option 2", "Option 3"])
   st.write(f"You chose: {choice}")
   if st.button("Success"):
       st.write("Operation was successful")
       try:
           1/0
       except Exception as e:
           st.exception(e)


if __name__ == "__main__":
    main()