import google.generativeai as genai 
from dotenv import load_dotenv
import os
import sys

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


class BaseModel:
    def __init__(self):
        self.GEMINI_API_KEY = GEMINI_API_KEY

    def get_model(self):
        try:
            genai.configure(api_key=self.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-2.5-flash")
            return model
        except Exception as e:
            print(e)

class AppFeatures(BaseModel):
    def __init__(self):
        super().__init__()
        self.__database = {}
        self.first_menu()

    def first_menu(self):
        first_input = input("""
            Hi ! How would you like to Proceed?
                1. Not a number? Register
                2. Already a number? Login            
                3. Bhai galti se aa gaye kia? Exit
       
                 """ )  

        if first_input == "1":
            # register
            self.__register()
        elif first_input == "2":
            #Login 
            self.__login()
        else:
            sys.exit() 

    def second_menu(self):
        second_input = input("""
            Hi! How would You like to proceed??
            1. Sentiment Analysis
            2. Language Translation
            3. Language Detection

        """)

        if second_input == "1":
            # Sentiment Analysis
            self.__sentiment_analysis()
        elif second_input == "2":
            # Language Translation
            self.__language_translation()
        elif second_input == "3":
            # Language Detection
            self.__language_detection()
        else:
            sys.exit() 

    def __sentiment_analysis(self):
        user_text = input("Enter Your Text: ")
        model = self.get_model()
        response = model.generate_content(f"Give me the sentiment of this sentence: {user_text}")
        result = response.text
        print(result)
        self.second_menu()

    def __language_translation(self):
        user_text = input("Enter Your Text: ")
        model = self.get_model()
        response = model.generate_content(f"Give me the Bangla translation of this sentence: {user_text}")
        result = response.text
        print(result)
        self.second_menu()  

    
    def __language_detection(self):
        user_text = input("Enter Your Text: ")
        model = self.get_model()
        response = model.generate_content(f"Give me the language detection of this sentence: {user_text}")
        result = response.text
        print(result)
        self.second_menu()       


               

    def __register(self):

        name = input("Enter Your Name: ")
        email = input("Enter Your Email: ")
        password = input("Enter Your Password: ")

        if email in self.__database:
            print("Email Already Exists.")
            self.first_menu()
        else:
            self.__database[email] = [name, password]  
            print("Registration Successful. Now you can Login")  
            self.first_menu()

    def __login(self):
        email = input("Enter Your Email: ")
        password = input("Enter Your Password: ")

        if email in self.__database:
            if self.__database[email][1] == password:
                print("Login! Successful")
                # Second menu()
                self.second_menu()
            else:
                print("Incorrect Password !!") 
                self.__login()
        else:
            print("Email not found.Please register first !!") 
            self.first_menu()          


app = AppFeatures()           


    