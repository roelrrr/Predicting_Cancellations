import os
import pandas as pd
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler

# Defining a function to print the directory tree
def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))

def radar_grapher(dataframe, needs_scaling = False, name = ""):

    fig = go.Figure()
    original_index = dataframe.index
    if needs_scaling == True:
        dataframe = scaler_function(dataframe)

    for cluster in range(len(dataframe)):
        
        categories = list(dataframe)

        master_values = list()
        master_values.append(dataframe.iloc[cluster,:].values.tolist())

        fig.add_trace(go.Scatterpolar(
              r=dataframe.iloc[cluster,:].values.tolist(),
              theta=categories,
              fill='toself',
              name= original_index[cluster]
        ))
        
    fig.update_layout(
    polar=dict(
      radialaxis=dict(
        visible=True,
        range=[min(master_values), max(master_values)])),
        title_text = name + " Radar Graph"
      )
    
    fig.show()

def scaler_function(dataframe):

    original_column_headers = dataframe.columns
    scaler = StandardScaler()
    df_clean_scaled_array = scaler.fit_transform(dataframe)

    #transforming back into df from array
    df_clean_scaled = pd.DataFrame(df_clean_scaled_array, columns = original_column_headers)
    
    return df_clean_scaled

def datetime_converter(df_and_column, format):
    df_and_column = pd.to_datetime(df_and_column, format=format, infer_datetime_format=True)
    return df_and_column

def roomChange(row):
    if row['AssignedRoomType'] == row['ReservedRoomType']:
        return 0
    else:
        return 1
