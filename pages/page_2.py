import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")

with st.echo():
    st.title("CAT")

    st.markdown(
        "[![Click me](https://static-file-serving.streamlit.app/~/+/app/static/cat.jpg)](https://streamlit.io)")
