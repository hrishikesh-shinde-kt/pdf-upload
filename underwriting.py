import streamlit as st
import requests
import pandas as pd

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

# Formats text.
def change_name_format(name):
  if name == "YesMedicalDeclarationData":
    name = "Medical Declaration"
  if name == "YesNonMedicalDeclarationData":
    name = "Non Medical Declaration"
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

# Adds logo and title on screen.
def add_logo():
  header = st.container()

  with header:
    col1, col2 = st.columns([2,3])
    with col1:
      st.image('media/Attributum.png')

    with col2:
      st.title('PIVOT Underwriting Co-Pilot')

def load():
    add_logo()
    
    # Getting the API-Key.
    uw_api_key = st.text_input('API-Key')
    
    if uw_api_key:
      uploaded_pdf = st.file_uploader("Upload expiring policy pdf")
      url = "https://pivot-uwcopilot-telemer-health.attributum.com/api/ml_process"
      if "Api-Key " not in uw_api_key:
          uw_api_key = f"Api-Key {uw_api_key}"
      headers = {"Authorization": uw_api_key}

      files = {
        "input_file" : uploaded_pdf
      } 
      
      data = {
        "insurance_company" : "telemer_hdfcergo",
        "data_type" : "Generic"
      }
      response = requests.post(url, files=files, data=data, headers=headers)

      if response:
        show_table(response.json())
