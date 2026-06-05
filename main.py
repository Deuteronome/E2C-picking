import pandas as pd

control_info = {
    "pim" : {
        "Armentières":1,
        "Lille":2,
        "Roubaix":2,
        "Saint Omer":1
    },
    "ran" : {
        "Armentières":1,
        "Lille":2,
        "Roubaix":2,
        "Saint Omer":1
    },
    "projet pro" : {
        "Armentières":1,
        "Lille":2,
        "Roubaix":2,
        "Saint Omer":1
    },
    "contacts" : {
        "Armentières":1,
        "Lille":2,
        "Roubaix":2,
        "Saint Omer":1
    },
    "stages" : {
        "Armentières":1,
        "Lille":2,
        "Roubaix":2,
        "Saint Omer":1
    }
}

df_tmp=pd.read_excel('./src/arm/stagiaires.xlsx')
df_arm = pd.DataFrame({'Nom': df_tmp['Nom'], 'Prénom':df_tmp['Prénom'], 'Site':df_tmp['Site'], 'Formateur':df_tmp['Formateur Référent'], 'Date':df_tmp['Date d\'entrée en formation']})

df_tmp=pd.read_excel('./src/lil/stagiaires.xlsx')
df_lil = pd.DataFrame({'Nom': df_tmp['Nom'], 'Prénom':df_tmp['Prénom'], 'Site':df_tmp['Site'], 'Formateur':df_tmp['Formateur Référent'], 'Date':df_tmp['Date d\'entrée en formation']})

df_tmp=pd.read_excel('./src/sto/stagiaires.xlsx')
df_sto = pd.DataFrame({'Nom': df_tmp['Nom'], 'Prénom':df_tmp['Prénom'], 'Site':df_tmp['Site'], 'Formateur':df_tmp['Formateur Référent'], 'Date':df_tmp['Date d\'entrée en formation']})

df_tmp=pd.read_excel('./src/rbx/stagiaires.xlsx')
df_rbx = pd.DataFrame({'Nom': df_tmp['Nom'], 'Prénom':df_tmp['Prénom'], 'Site':df_tmp['Site'], 'Formateur':df_tmp['Formateur Référent'], 'Date':df_tmp['Date d\'entrée en formation']})

df_all = pd.concat([df_arm,df_rbx,df_lil,df_sto], ignore_index=True)

df_all['Date']=pd.to_datetime(df_all['Date'])
limit = pd.Timestamp.now() - pd.DateOffset(months=1)

df_ok = df_all[
    (df_all['Date'].dt.year != 2025) &  # pas 2025
    (df_all['Date'] < limit)           # plus ancien que 1 mois
]

df_picking = pd.DataFrame(columns=["Contrôle", "Stagiaire", "Site", "Formateur", "Date"])

for control, sites in control_info.items():
    ref_pick = df_ok.groupby('Formateur').sample(n=1)
    for site, qty in sites.items():
        df_new_pick = ref_pick[ref_pick['Site'] == site].sample(n=qty)
        for row in df_new_pick.itertuples():
            df_picking = pd.concat([df_picking, pd.DataFrame([{"Contrôle":control, "Stagiaire":f"{row.Prénom} {row.Nom}", "Site":site, "Formateur":row.Formateur, "Date":row.Date.date()}])], ignore_index=True)

file_name = "./output/picking_list.xlsx"
df_picking.to_excel(file_name, index=False)


