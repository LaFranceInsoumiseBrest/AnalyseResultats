import pandas as pd

#df = pd.read_csv('municipales-2026-resultats-bv-par-communes-2026-03-20.csv', sep=";")
df = pd.read_csv('municipales-2026-bv-tour2.csv', sep=";")

print(len(df[df['Code commune'] == "29019"]))

# df[df['Code commune'] == "29019"].to_csv('brest-2026-municipales-bv-tour1.csv', sep=";")
df[df['Code commune'] == "29019"].to_csv('brest-2026-municipales-bv-tour2.csv', sep=";")