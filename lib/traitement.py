import datetime

def filter_edt(df,col,pf_name,deb_valid,fin_valid):
    now = datetime.datetime.now()
    dv=now.strftime("%Y-%m-%d") if deb_valid == "" else deb_valid
    fv=now.strftime("%Y-%m-%d") if fin_valid == "" else fin_valid
    df_final = df[(df[col] == pf_name) & (df.Debut_validite.isnull() | df.Fin_validite.isnull() | ((df['Debut_validite'] <= fv) & (df['Fin_validite'] >= dv)))].sort_values(by=["Jour","Heure debut"])		
    return df_final