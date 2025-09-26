import streamlit as st

# displaying text

st.title("my title")

st.header("this is my header",divider="gray")

st.subheader("this is subheader")

st.markdown("**am good**")

st.html('<h1 style="color: aqua; " >am good</h1>')


tab1,tab2=st.tabs(tabs=['        tab1         ','        tab2      '])

tab1.title("am good")

tab2.title("am good perfect")


st.page_link("pages/appp.py",label="derv")