import pandas as pd


def csv_saver(product_dict, csv_file):
    products_df = pd.DataFrame(product_dict)
    products_df.to_csv(csv_file, encoding='utf-8', index=False)

