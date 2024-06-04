import streamlit as st
from underwriting import load as load_underwriting
from portability import load as load_portability

st.set_page_config(
    page_title="Attributum",
    layout="wide",  # sets page to wide mode as default. 
)

def run():
    # Sidebar for navigation
    st.sidebar.title('PIVOT')
    page = st.sidebar.selectbox('Select page:', ['Underwriting', 'Portability', 'Operations', 'Diagnostics'])
    # Load different pages based on the selection
    if page == 'Underwriting':
        load_underwriting()
    elif page == 'Portability':
        load_portability()
    
# Main logic.
run()
