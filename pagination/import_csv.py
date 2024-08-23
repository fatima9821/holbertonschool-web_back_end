import pandas as pd

file_path = 'Popular_Baby_Names.csv'

# read the file CSV
df = pd.read_csv(file_path)

# display 20 first lines
print(df.head(20))
