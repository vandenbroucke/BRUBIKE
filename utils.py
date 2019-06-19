import pandas as pd
def check_if_the_tsv_hot_file_already_has_processed_columns(csv_file_path):
	df = pd.read_csv(csv_file_path,delimiter="\t")
	try:
		total_rows=len(df.Rain)
		return True
	except Exception as e:
		return False	