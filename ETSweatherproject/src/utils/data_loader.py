import pandas as pd
import os

def load_provinces(file_path):
    provinces_df = pd.read_csv(file_path, delimiter=';')
    return provinces_df

def load_municipalities(file_path):
    municipalities_df = pd.read_csv(file_path, delimiter=';')
    return municipalities_df

def get_province_list(provinces_df):
    return [(row['CPRO'], row['NPRO']) for index, row in provinces_df.iterrows()]

def get_municipality_list(municipalities_df, cpro):
    return [(row['CMUN'], row['NOMBRE']) for index, row in municipalities_df[municipalities_df['CPRO'] == cpro].iterrows()]