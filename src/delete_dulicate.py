import pandas as pd

df = pd.read_csv('./kenh14Crawl/urls.csv')

df_no_duplicates = df.drop_duplicates()

df_no_duplicates.to_csv('./kenh14Crawl/urls.csv', index=False)