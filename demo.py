import streamlit as st
from PIL import Image
st.title("Hello Everyone..!")
st.header("This is a header")
st.subheader("This is a subheader")
st.text("This is a text")
st.markdown("This is a markdown")
st.success("This is a success message")
st.info("This is a info message")
st.warning("This is a warning message")
st.error("This is a error message")
st.exception("This is a exception message")
st.write("This is a write")
st.write(range(10))
img = Image.open("image.jpg")
st.image(img, width=400, caption="Nature")

if st.checkbox("Show/Hide"):
    st.text("Showing or Hiding widget")

status = st.radio("Select Gender :",('Male','Female'))
if status == 'Male':
    st.success("Male")
else:
    st.success("Female") 
st.text("Selected status is : "+status) 

hobby = st.selectbox("Hobby :",['Reading','Writing','Coding'])
st.write("Selected hobby is :",hobby)

Languages = st.multiselect("Languages Known :",['Python','Java','C++','C#'])
st.write("You selected",len(Languages)," Languages")

st.button("Click me for no reason")

if st.button("About"):
    st.info("This is a demo app for Streamlit")

name = st.text_input('Enter your name :')
age = st.text_input('Enter your age :')
if st.button("Submit"):
    if int(age)>18:
        st.success(name +" is eligible to vote")
    else:
        st.error(name+" is not eligible to vote")     