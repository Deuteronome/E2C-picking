import pandas as pd
import openpyxl as xl

df_tmp=pd.read_excel('./src/arm/stagiaires.xlsx')
df_arm = pd.DataFrame({'Nom': df_tmp['Nom'], 'Prénom':df_tmp['Prénom'], 'Site':df_tmp['Site'], 'Formateur Référent':df_tmp['Formateur Référent'], 'Date':df_tmp['Date d\'entrée en formation']})

df_tmp=pd.read_excel('./src/rbx/stagiaires.xlsx')
df_rbx = pd.DataFrame({'Nom': df_tmp['Nom'], 'Prénom':df_tmp['Prénom'], 'Site':df_tmp['Site'], 'Formateur Référent':df_tmp['Formateur Référent'], 'Date':df_tmp['Date d\'entrée en formation']})

df_all = pd.concat([df_arm,df_rbx], ignore_index=True)

df_all['Date']=pd.to_datetime(df_all['Date'])
limit = pd.Timestamp.now() - pd.DateOffset(months=1)

df_ok = df_all[
    (df_all['Date'].dt.year != 2025) &  # pas 2025
    (df_all['Date'] < limit)           # plus ancien que 1 mois
]

sub_pick = df_ok.groupby('Formateur Référent').sample(n=1)
pick = sub_pick.groupby('Site').sample(n=2)

print(pick)