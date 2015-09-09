import pandas as pd

df = pd.read_csv('/Users/sinanozdemir/Downloads/YEC.csv')

emails = map(lambda x: str(x.lower()), list(df['Email'].dropna()))


emails[1031]

