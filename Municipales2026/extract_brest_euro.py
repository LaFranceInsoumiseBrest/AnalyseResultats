import pandas as pd

df = pd.read_csv('resultats-definitifs-par-bureau-de-vote.csv', sep=";")

print(len(df[df['Code commune'] == "29019"]))

df[df['Code commune'] == "29019"].to_csv('brest-2024-euro-bv.csv', sep=";")