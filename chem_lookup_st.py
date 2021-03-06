import pandas as pd
import os
import numpy as np
import streamlit as st


# Load data
file_name = 'solvent_scale_table.xlsx'
#path = os.path.join(os.getcwd(), file_name)
#df = pd.read_excel(file_name, sheet_name = 'main')
df = pd.read_csv('solvent_scale_table.csv')
cols = [i for i in df.columns if i not in ['solvent','class', 'avg_dielectric_constant']]
for col in cols:
    df[col]=pd.to_numeric(df[col], errors ='coerce')
df['solvent'] = df['solvent'].str.lower()
df.set_index('solvent', inplace=True)
df.sort_index(axis =0, inplace=True)


st.title('Chemical Lookup Table')
st.text('By Dao & Jon')
##################################
# See all data for selected solvents
st.subheader('All Data')
option1 = st.sidebar.multiselect('Please pick a solvent of interest', list(df.index.values))
all_option1 = st.sidebar.checkbox("Select all solvents")
if all_option1:
    option1 = list(df.index.values)
df_solvent = df[df.index.isin(option1)] #df[df['solvent'].isin(options)]
st.dataframe(df_solvent.transpose())

##################################
# Find solvents given solubilty range
st.subheader('Solubility Data')
options2 = st.sidebar.multiselect('Please pick chemical of interest for solubility', ['cis', 'cis_acid', 'cis_monoester', 'cis_qp',
                                                                              'cis_amide', 'laudanosine_besylate', 'laudanosine',
                                                                              'midazolam_acetamide', 'midazolam_lactam',
                                                                              'diha'], default = ['cis'])
columns = list(df.columns)
new_col = [col_name for chem in options2 for col_name in columns if (chem +'_min' in col_name) or (chem +'_max' in col_name)]
df_solubility = df[new_col]
df_min =  df_solubility.loc[:, df_solubility.columns.str.contains('min')]
df_max = df_solubility.loc[:, df_solubility.columns.str.contains('max')]
try:
    min = float(df_min.min().min())
    max = float(df_max.max().max())
    value = st.slider('Please select a threshold value (greater than max) for solubility [mg/mL]', min_value = min,max_value = max, step = float(1))
except:
    st.write('Please select chemical(s) of interest')

#df_min = df_min[df_min <= value]
#df_min = df_min.dropna(thresh =df_min.shape[1])
df_max = df_max[df_max >= value]
df_max = df_max.dropna(thresh =df_max.shape[1])
st.dataframe(df_min.join(df_max, how = 'inner'))

##################################
# Find variable of interest given threshold value
st.subheader('Variable of Interest')
df_var = df.iloc[:,0:7]
options3 = st.selectbox('Please pick chemical of interest for solubility',list(df_var.columns), index = 0)
df_var2 = df_var[options3]
var = st.slider('Please select a threshold value (greater than) for {}'.format(options3), min_value = float(df_var2.min()),max_value = float(df_var2.max()), value =float(0), step = float(.01))
st.dataframe(df_var2[df_var2 >= var])
