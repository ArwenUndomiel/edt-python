'''
    Fonction métier de l'application
'''
import datetime

def filter_edt(df_data, col, pf_name, deb_valid, fin_valid):
    '''
    Filtre les données d'un professeur ou d'une salle
    @param : df_data = données edt, col='Salle' ou 'Professeur'
        pf_name='nom prof ou salle', deb_valid=1er jour de recherche
        fin_valid=dernier jour de recherche
    '''
    now = datetime.datetime.now()
    deb_val = now.strftime("%Y-%m-%d") if deb_valid == "" else deb_valid
    fin_val = now.strftime("%Y-%m-%d") if fin_valid == "" else fin_valid
    df_final = df_data[(df_data[col] == pf_name) & (df_data.Debut_validite.isnull() |
                    df_data.Fin_validite.isnull() |((df_data['Debut_validite'] <= fin_val)\
                    & (df_data['Fin_validite'] >= deb_val)))]\
						.sort_values(by=["Jour","Heure debut"])
    return df_final

def dispo_salle(df_data, df_param_salle, jour, deb_valid, fin_valid, deb_cren, fin_cren):
    '''
    Filtre le salles disponibles
    @param : df_data = données edt, jour=liste des jours de la semaine,
        deb_valid=1er jour de recherche,fin_valid=dernier jour de recherche
        deb_cren=heure début du créneau souhaité, fin_cren= heure de fin du créneau
    '''
    now = datetime.datetime.now()
    deb_val = now.strftime("%Y-%m-%d") if deb_valid == "" else deb_valid
    fin_val = now.strftime("%Y-%m-%d") if fin_valid == "" else fin_valid
    cren_debut = datetime.datetime.strptime(deb_cren, '%H:%M').time()
    cren_fin = datetime.datetime.strptime(fin_cren, '%H:%M').time()
    df_salles_occupees = df_data[(df_data['Jour'] == jour) & (df_data.Debut_validite.isnull() | \
                            df_data.Fin_validite.isnull() | \
							((df_data['Debut_validite'] <= fin_val) & \
							(df_data['Fin_validite'] >= deb_val))) & \
							((df_data['Heure fin'] > cren_debut) & \
                            (df_data['Heure debut'] < cren_fin))].Salle
    df_final = df_param_salle.to_frame().merge(df_salles_occupees, indicator='i', how='outer')\
                    .query('i == "left_only"').drop('i', 1).sort_values(by=["Salle"])
    return df_final
