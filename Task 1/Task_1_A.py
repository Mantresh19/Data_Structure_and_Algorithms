import pandas as pd

# Read Excel file
df = pd.read_excel('../Libraries/London Underground data.xlsx')

# View the data
print(df.head())

# (Optional) Convert to CSV and save
df.to_csv('data.csv', index=False)
