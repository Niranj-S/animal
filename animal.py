import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

genai.configure(api_key=st.secrets['API_KEY'])



def get_gemini_repsonse(input,image,prompt):
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Animal Detection App")

st.header("Food recipe App")
st.write("upload the food image and you'll find out information about the animal :)")
input=''
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Teach me about the animal")

input_prompt="""
You are an animal expert and you have to detect whatever animal from the image, response in the following format

Name : <name of animal>
Species : <scientific name>
Habitat: <habitat of animal>
Type: <wether animal is carnivorous, omnivorous, or herbivore>
Status : <if animal is exint or not>
Origin : <nationality of region of animal>
About : <brief description of animal>
"""

## If submit button is clicked

if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_repsonse(input_prompt,image_data,input)
    st.subheader("The Animal is:")
    st.write(response)
