
import pandas as pd


with open('final_product_2.json', encoding='utf-8') as f:
    data = pd.read_json(f)

data.to_csv('products.csv', encoding='utf-8', index=False)


