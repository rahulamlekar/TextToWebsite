import streamlit as st
import urllib.request
from oai import chat, chat4
from serpapi import GoogleSearch
import requests_cache

requests_cache.install_cache(cache_name='st_cache', backend='sqlite', expire_after=5)


def image_search(query):
    API_KEY = "GOOGLE_API_KEY"
    params = {
        "q": query + " logo",
        "tbm": "isch",
        "ijn": "0",
        "api_key": API_KEY
    }
    search = GoogleSearch(params)
    results = search.get_dict()

    try:
        img_link = results["images_results"][0]["original"]
        ext = img_link.split('/')[-1].split('.')[-1]
        query = query.strip()
        file_name = f"{query}.jpg"

        urllib.request.urlretrieve(img_link, file_name)
        print(img_link, file_name)
        return file_name
    except Exception as e:
        print(e)
        return None


def get_design_and_keyword(user_text):
    design_template = """
user: <user query>
design: <description in 100 words>
STOP

user: build me a todo app
design: Create a to-do app that allows users to add, edit, and delete tasks, and mark tasks as complete. Implement a simple user-friendly interface.
STOP

user: an app to record thoughts, like and share
Design: Develop a thought-recording app that allows users to easily input, save, and organize their thoughts, ideas, and inspirations. Users can categorize their thoughts with tags, add multimedia content (images, audio, etc.), and share their thoughts with friends. Implement a clean and intuitive user interface. A feature that allows users to search through their saved thoughts using keyword.
STOP

user: build me a app to record my workouts and publish them
Design: Create a fitness tracking app that allows users to log their workouts, including exercise type, duration, and intensity. Users can also add notes, photos, and videos to document their progress. With options to track progress over time and set personal fitness goals.
STOP

user: {user_query}"""

    design = chat("You an expert frontend developer.", design_template.format(user_query=user_text), stop=["STOP"])
    # keyword = design.lower().split("keyword: ")[1].split(" ")[0].strip()
    return design

def generate_website(user_text, design):
    try:
        # file_name = image_search(keyword)

        prompt = f"""
        {design}

        - build a fully functioning website for the above design idea.
        - add necessary features as required.
        - be playful and humorous 
        - use <script src="jquery.js"></script>
        - use tailwindcss using   <script src="https://cdn.tailwindcss.com"></script>. 
        - output only working code in markdown format, NO text.
        """

        code = chat4("You an expert frontend developer.", prompt)
        
        try:
            code = code.split("```")[1][4:]
        except:
            pass

        with open("code.html", "w") as f:
            f.write(code)
    except Exception as e:
        st.write(e)

# st.write("### Transform your ideas into websites")
user_text = st.text_input("Describe your website:")

if user_text:
    design = get_design_and_keyword(user_text)
    generate_website(user_text, design)
    st.markdown("[Website is ready!](/Users/shubhamchandel/Documents/test-to-website/code.html)")
