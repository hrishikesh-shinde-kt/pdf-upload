import streamlit as st
from underwriting import load as load_underwriting
from portability import load as load_portability

st.set_page_config(
    page_title="Attributum",
    layout="wide",  # sets page to wide mode as default. 
)

# Adds logo and title on screen.
def add_logo():
  # Create a container for the logo and title
  header = st.container()

  # Add a logo to the left column
  with header:
    col1, col2 = st.columns([1,4])
    with col1:
      st.image('media/Attributum.png')

    with col2:
    #   st.title('PIVOT Portability from Attributum')
        st.title('PIVOT Platform - Capability Accelerator Modules stack')

def load_landing():
    add_logo()

def run():
    # Sidebar for navigation
    st.sidebar.title('PIVOT')
    page = st.sidebar.selectbox('Select page:', ['Landing', 'Underwriting', 'Portability', 'Operations', 'Diagnostics'])

    # Load different pages based on the selection
    if page == 'Landing':
        load_landing()
    elif page == 'Underwriting':
        load_underwriting()
    elif page == 'Portability':
        load_portability()
    
# Main logic.
run()
