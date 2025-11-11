import pandas as pd

# Check the output file
df = pd.read_excel('test_data/bench/cutting_plan_output_1.xlsx')
print("Columns:", df.columns.tolist())
print("\nShape:", df.shape)
print("\nFirst 20 rows:")
print(df.head(20))
