import streamlit as st
import pandas as pd
import requests

colors = {
  'header': '#cfe4f7',
  'odd_row': '#e7f1fa',
  'even_row': '#f2f9ff',
}

blue_shades = [
    {'selector': '',
     'props': [('border', '1px solid #c7d2ff')]},
    {'selector': 'th',
     'props': [('background-color', '#4c68ff'),
               ('color', 'white'),
               ('font-weight', 'bold')]},
    {'selector': 'td',
     'props': [('background-color', '#e5e9ff')]},
    {'selector': 'tr:nth-of-type(odd)',
     'props': [('background-color', '#d8dcff')]},
    {'selector': 'tr:nth-of-type(even)',
     'props': [('background-color', '#f2f4ff')]},
    {'selector': 'tr:hover',
     'props': [('background-color', '#c1c9ff')]},
]

blue_shades = [
  {
    'selector': 'table',
    'props': [
      ('width', '100%'),
      ('border-collapse', 'collapse'),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
  {
    'selector': 'th',
    'props': [
      ('background-color', colors['header']),
      ('color', '#000'),
      ('font-weight', 'bold'),
      ('text-align', 'center'),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
  {
    'selector': 'tr:nth-of-type(odd)',
    'props': [
      ('background-color', colors['odd_row']),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
  {
    'selector': 'tr:nth-of-type(even)',
    'props': [
      ('background-color', colors['even_row']),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
  {
    'selector': 'td',
    'props': [
      ('text-align', 'center'),
      ('padding', '8px'),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
]

# Adds logo and title on screen.
def add_logo1():
  # Create a container for the logo and title
  header = st.container()

  # Add a logo to the left column
  with header:
    col1, col2 = st.columns([2,2])
    with col1:
      st.image('media/Attributum.png', use_column_width='auto')

    with col2:
      # st.title('PIVOT Portability from Attributum')
      st.title('PIVOT Platform')
      st.subheader('Capability Accelerator Modules Stack')
      
def add_logo():
  # Create two columns
  col1, col2 = st.columns([2, 2])

  # 1st Column: Vertically centered image
  with col1:
      st.image('media/Attributum.png', use_column_width='auto')

  # 2nd Column: Texts
  with col2:
      st.header("PIVOT Platform")
      st.subheader("Capability Accelerator Modules Stack")
      
  st.divider()
  st.write("### PIVOT Portability from Attributum")

# Formats text.
def change_name_format(name):
  return name.replace("_", " ").title()

# Returns list of keys of a dictonary.
def get_column_name(keys):
  return [change_name_format(key) for key in keys.keys()]

# Changes table border style.
def set_table_border():
  css = """
      <style>
      table.dataframe {
          border-collapse: separate;
          border-spacing: 0px;
          border-color: #4d6bff;
          border-width: 4px;
          border-style: outset;
          border-radius: 8px;
      }
      </style>
  """

  st.markdown(css, unsafe_allow_html=True)

# Displays table(s) according to the response.
def show_table(response):
  response_item = response['response']['data']
  response_item = {key: value for key, value in response_item.items() if value}
  for item in response_item:
    if isinstance(response_item[item], dict):
      df = pd.DataFrame(
        [list(response_item[item].values())],
        columns = get_column_name(response_item[item])
      )
    else: 
      df = pd.DataFrame(
        [list(i.values()) for i in response_item[item]],
        columns = get_column_name(response_item[item][0])
      )
    st.header(change_name_format(item))
    set_table_border()
    hide_table_row_index = """
            <style>
              thead tr th:first-child {display:none}
              tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    styled_df = df.style.set_table_styles(blue_shades)
    st.table(styled_df)

def custom_selectbox(label, options, disabled_options):
    selected_option = st.selectbox(label, options)
    if selected_option in disabled_options:
        st.markdown(f"Selected option: **{selected_option}** (disabled)")
    else:
        st.markdown(f"Selected option: **{selected_option}**")


# Main logic.
def load():
  add_logo() 

  # Getting the API-Key.
  port_api_key = st.text_input('API-Key')
  option = None

  if port_api_key:
    # Getting the list of options.
    url = "https://pivot-port-poldoc-health.attributum.com/api/company/all"
    if "Api-Key " not in port_api_key:
      port_api_key = f"Api-Key {port_api_key}"
    headers = {"Authorization": port_api_key}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      options = [company['name'].lower() for company in response.json()]
      options.insert(0, None)
      
      # Add more options.
      additional_options = ["star insurance", "Icici", "hdfc ergo", "Niva bupa", "United india uba", "national", "Care health", "Cigna ttk", "Chola ms"]
      for option in additional_options:
        if option.lower() not in options:
          options.append(option)

      # Getting Policy type input.
      option = st.selectbox(
        'Insurer Name',
        options
      )
    elif response.status_code == 403:
      st.write("Wrong API key. Enter Correct API key.")
    else:
      st.write("Some Error occured in API.")

  if option:
    # Getting pdf input.
    uploaded_pdf = st.file_uploader("Upload expiring policy pdf")
    if uploaded_pdf is not None:
      url = "https://pivot-port-poldoc-health.attributum.com/api/ml_process"
      files = {
        "input_file" : uploaded_pdf
      } 
      data = {
        "insurance_company" : option,
        "data_type" : "Generic"
      }
      if "Api-Key " not in port_api_key:
        port_api_key = f"Api-Key {port_api_key}"

      headers = {"Authorization": port_api_key}

      # Post API call.
      if option != "":
        response = requests.post(url, files=files, data=data, headers=headers)
        if response and response.status_code == 200:
          show_table(response.json())
        elif response.status_code == 403:
          st.write("Wrong API key. Enter Correct API key.")
        else:
          st.write("Some Error occured in API.")

