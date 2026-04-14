import pandas as pd

euro = pd.read_csv('brest-2024-euro-bv.csv', sep=";").astype({'Code BV': 'int32'}).set_index('Code BV')

municipales = pd.read_csv('brest-2026-municipales-bv.csv.csv', sep=";").astype({'Code BV': 'int32'}).set_index('Code BV')


#df = municipales.merge(euro, how="left", on="Code BV", lsuffix='.euro', rsuffix='.muni')[['Inscrits.euro', 'Inscrits.muni']]

df = pd.merge(euro, municipales, how='right', left_index=True, right_index=True, suffixes=['.euro', '.muni'])[['Inscrits.euro', 'Inscrits.muni']].fillna(0)

df['Inscrits.delta'] = df['Inscrits.muni'] - df['Inscrits.euro']
df.loc['Total']= df.sum()

print(df.columns)

df.to_csv('brest_delta_inscrits.csv', sep=";")