import streamlit as st
import pandas as pd
import numpy as np
import logging
import time 

#from pannel.app.bar import BarPlot
from pannel.app import BarPlot
from pannel.core import local_css
from logging.handlers import RotatingFileHandler


LOGGER_PATH = 'log.out'
LOGGER_FORMAT = '%(asctime)s %(levelname)-8s %(message)s'
formatter = logging.Formatter(LOGGER_FORMAT)

logging.basicConfig(
    format=LOGGER_FORMAT,
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('')
handler = RotatingFileHandler(
    LOGGER_PATH, 
    maxBytes=1000,
    backupCount=2
)
handler.setFormatter(formatter)
logger.addHandler(handler)

st.set_page_config(layout="wide")


def get_raw_data():
    df = pd.DataFrame({
        'index': ['Ontem', 'Semana', 'Mês'],
        'PDRI': [394.976, 401.40242, np.nan],
        'KAIO': [334.1628, 603.489058, np.nan],
        'MNIZ': [334.019920, 652.165268, 779.078412],
        'MART': [158.456420, 1008.507369, 1628.506739],
        'MNNO': [154.506, np.nan, np.nan],
        'CLAU': [np.nan, 1256.089602, 1324.027802],
        'VRON': [np.nan, np.nan, 2738.0719],
        'FERR': [np.nan, np.nan, 2388.145417],
    })

    return df

def get_data():
    
    df = get_raw_data()
    
    source = df.melt('index')
    mask = source['value'].notna()
    source=source[mask]
    
    return source

def get_centered_values(values, padding):
    """Construct centered elements for each unit in values with a p padding units
       before and after each value unit.
       
       i.e:
       
       values = ['A', 'B']
       padding = 1
        ________ ________ ________ ________ ________ ________     
       |  blank |    A   |  blank |  blank |    B   |  blank |
        -------- -------- -------- -------- -------- -------- 
     """
    num_values = len(values)
    columns = (2*padding+1)*num_values
    
    idx = 0
    rows = st.columns(columns)
    for i in range(columns):
        if i % (2*padding+1) == padding:
            rows[i].info(values[idx])
            idx += 1


def get_data_from_time(time):
    data = get_raw_data()
    source = data.melt('index')
    mask  = source['value'].notna()
    mask &= source['index']==time
    d = source[mask].drop('index', axis=1)
    d.columns = ['Token', 'Vol.']
    d = d.reset_index().drop('index', axis=1)
    return d


def to_style(data):

    s = data.style

    #colors = ['#445679', '#314267']
    cell_hover = {  # for row hover use <tr> instead of <td>
        'selector': 'td:hover',
        #'text-align':'center',
        'props': [('background-color', '#003942')]
    }
    index_names = {
        'selector': '.index_name',
        #'text-align':'center',
        'props': 'font-style: italic; color: darkgrey; font-weight:normal;'
    }
    headers = {
        'selector': 'th',
        #'text-align':'center',
        'props': 'background-color: #003942; color: white;'
    }
    cells = {  
        'selector': 'td',
        #'text-align':'center',
        'props': 'background-color: #247286; color: white;'
    }
    s.set_table_styles([cell_hover, index_names, headers, cells])
    
    s.set_table_styles([  # create internal CSS classes
        {'selector': '.true', 'props': 'background-color: #e6ffe6;'},
        {'selector': '.false', 'props': 'background-color: #ffe6e6;'},
    ], overwrite=False)
    
    return s.set_properties(**{'text-align': 'center'})



source = get_data()
# Save output in log.out
logger.info(f"Total Cliente: {source.value.max()}") # example

# Create Barplot
barplot = BarPlot().compute(source)



st.title('Clientes')

with st.container():
    #  -----------------------------------------------------------------------
    # |         Cadastros - Novos         |     Clientes Ativos - Acumulado   |
    #  -----------------------------------------------------------------------
    # | Ontem | Hoje | Agosto | Conversão | Julho | Ontem | Agosto | Var. mês |
    #  -----------------------------------------------------------------------
    # |   25  |  30  |   200  |    75%    |  120  |  150  |   150  |   +25%   |
    #  -----------------------------------------------------------------------
    
    titles = [
        'Cadastros - Novos',
        'Clientes Ativos - Acumulado',
        #'Clientes Ativos - Acumulado 2'
    ]
    
    # First Row
    get_centered_values(values=titles, padding=1) # padding := {0, 1, 2, ...}
    
    # Second Row
    columns = st.columns(8)
    values = [ 
        "Ontem", "Hoje", "Agosto",
        "Conversão", "Julho" ,"Ontem",
        "Agosto", "Var. mês"
    ]
    for col, value in zip(columns, values):
        col.info(value)

    # Third Row
    columns = st.columns(8)
    values = [ 
        "25", "30", "200",
        "75%", "120","-25%",
        "0", "+25%"
    ]
    for col, value in zip(columns, values):
        if value.startswith("+"): # any condition
            col.success(value)    # Green
        elif value.startswith("-"): # any condition
            col.error(value)      # Red
        elif value == '0': # any condition
            col.warning(value)    # Yellow
        else:
            col.info(value)
        # Alternatively:
        # st.markdown(Cell(body=l, type="text"), unsafe_allow_html=True)
    
    # Forth Row
    
    # See more details in: https://pandas.pydata.org/pandas-docs/stable/user_guide/style.html
    values = [
        ('Ontem', to_style(get_data_from_time('Ontem'))),
        ('Semana', to_style(get_data_from_time('Semana'))),
        ('Mês', to_style(get_data_from_time('Mês'))),
    ]
    columns = st.columns(len(values))
    for col, value in zip(columns, values):
        col.markdown("<div><style>h3 {text-align: center;}</style><h3>"+value[0]+"</h3></div>", unsafe_allow_html=True)
        col.table(value[1])

    # Fifth Row
    columns = st.columns(1)
    col = columns[0]
    col.write(barplot, use_container_width=True)


st.title('Transações')
with st.container():
    row1 = st.columns(1)
    row1[0].info("Top 5 - Tokens Negociados")

    row2 = st.columns(2)

    valores1= [
        "Ontem", "Semana", "Mês"
    ]
    valores2= [
        "Ontem", "Hoje", "Julho", "Agosto"
    ]
    
    
    
    
    
