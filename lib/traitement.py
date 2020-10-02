import datetime
import pandas as pd

def filter_edt(df, col, pf_name, deb_valid, fin_valid):
    now = datetime.datetime.now()
    dv = now.strftime("%Y-%m-%d") if deb_valid == "" else deb_valid
    fv = now.strftime("%Y-%m-%d") if fin_valid == "" else fin_valid
    df_final = df[(df[col] == pf_name) & (df.Debut_validite.isnull() | df.Fin_validite.isnull() | ((df['Debut_validite'] <= fv) & (df['Fin_validite'] >= dv)))].sort_values(by=["Jour","Heure debut"])		
    return df_final

def dispo_salle(df, df_param_salle, jour, deb_valid, fin_valid, deb_cren, fin_cren):
    now = datetime.datetime.now()
    dv = now.strftime("%Y-%m-%d") if deb_valid == "" else deb_valid
    fv = now.strftime("%Y-%m-%d") if fin_valid == "" else fin_valid
    dc = datetime.datetime.strptime(deb_cren, '%H:%M').time()
    fc = datetime.datetime.strptime(fin_cren, '%H:%M').time()
    df_salles_occupees = df[(df['Jour'] == jour) & (df.Debut_validite.isnull() | df.Fin_validite.isnull() | ((df['Debut_validite'] <= fv) & (df['Fin_validite'] >= dv))) & ((df['Heure fin'] > dc) & (df['Heure debut'] < fc))].Salle
    df_final = df_param_salle.to_frame().merge(df_salles_occupees, indicator='i', how='outer').query('i == "left_only"').drop('i', 1)
    return df_final
