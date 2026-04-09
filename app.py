import streamlit as st
import streamlit.components.v1 as components

# Set the page to wide mode
st.set_page_config(page_title="Fikreab AI Turbo", layout="wide")

# Put all of your HTML code inside these triple quotes
html_code = """
<!DOCTYPE html>
<html>
<head>
    </head>
<body>
    </body>
</html>
"""

# This line displays the HTML on the screen
components.html(html_code, height=1200, scrolling=True)
