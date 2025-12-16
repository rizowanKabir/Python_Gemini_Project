import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

# Configure page settings
st.set_page_config(
    page_title="NLP Project UI",
    page_icon="🚆",
    layout="wide"
)

class NLPModel:
    def get_model(self):
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            model = genai.GenerativeModel("gemini-2.5-flash")
            return model
        except Exception as e:
            st.error(f"Error configuring model: {e}")
            return None

def main():
    st.title("🚆 NLP Application")
    # Initialize Session State
    if 'database' not in st.session_state:
        st.session_state.database = {} # Format: {email: {'name': name, 'password': password}}
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_user' not in st.session_state:
        st.session_state.current_user = None

    # Sidebar for Navigation / Auth
    with st.sidebar:
        st.header("Navigation")
        if not st.session_state.logged_in:
            option = st.radio("Choose Option", ["Login", "Register"])
        else:
            st.success(f"Welcome, {st.session_state.database[st.session_state.current_user]['name']}!")
            if st.button("Logout"):
                st.session_state.logged_in = False
                st.session_state.current_user = None
                st.rerun()

    # Main Content Area
    if not st.session_state.logged_in:
        if option == "Register":
            st.subheader("Create a New Account")
            with st.form("register_form"):
                name = st.text_input("Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Register")

            if submit:
                if email in st.session_state.database:
                    st.error("Email already exists!")
                elif name and email and password:
                    st.session_state.database[email] = {'name': name, 'password': password}
                    st.success("Registration successful! Please login.")
                else:
                    st.warning("Please fill in all fields.")

        elif option == "Login":
            st.subheader("Login to your Account")
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")

            if submit:
                if email in st.session_state.database:
                    if st.session_state.database[email]['password'] == password:
                        st.session_state.logged_in = True
                        st.session_state.current_user = email
                        st.success("Login Successful!")
                        st.rerun()
                    else:
                        st.error("Incorrect Password")
                else:
                    st.error("Email not found. Please register first.")

    else:
        # User is logged in, show features
        st.subheader("NLP Features")

        feature = st.selectbox(
            "Select a Service",
            ["Sentiment Analysis", "Language Translation", "Language Detection"]
        )

        nlp = NLPModel()
        model = nlp.get_model()

        if feature == "Sentiment Analysis":
            st.info("Analyze the sentiment of a sentence.")
            user_text = st.text_area("Enter text for sentiment analysis")
            if st.button("Analyze Sentiment"):
                if user_text:
                    with st.spinner("Analyzing..."):
                        response = model.generate_content(f"Give me the sentiment of this sentence: {user_text}")
                        st.write("### Result:")
                        st.write(response.text)
                else:
                    st.warning("Please enter some text.")

        elif feature == "Language Translation":
            st.info("Translate text to Hindi.")
            user_text = st.text_area("Enter text to translate")
            if st.button("Translate"):
                if user_text:
                    with st.spinner("Translating..."):
                        response = model.generate_content(f"Give me Bangla translation of this sentence: {user_text}")
                        st.write("### Result:")
                        st.write(response.text)
                else:
                    st.warning("Please enter some text.")

        elif feature == "Language Detection":
            st.info("Detect the language of a text.")
            user_text = st.text_area("Enter text for language detection")
            if st.button("Detect Language"):
                if user_text:
                    with st.spinner("Detecting..."):
                        response = model.generate_content(f"Detect the language of this sentence: {user_text}")
                        st.write("### Result:")
                        st.write(response.text)
                else:
                    st.warning("Please enter some text.")

if __name__ == "__main__":
    main()
