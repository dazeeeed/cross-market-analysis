import os
import json
import utilities

def separate_products(input_file, btc_output_file, eth_output_file):
	"""
	Separates lines with "BTC" or "ETH" product value in a JSON file to different files.

	Args:
	input_file: Path to the input file.
	btc_output_file: Path to the output file for BTC lines.
	eth_output_file: Path to the output file for ETH lines.
	"""
	with open(input_file, "r") as input_f, \
		open(btc_output_file, "w") as btc_f, \
		open(eth_output_file, "w") as eth_f:

		for i, line in enumerate(input_f):
			if i == 0:
				continue # Skip the first line
			try:
				product = json.loads(line)["product_id"]
				if product == "BTC-USD":
					btc_f.write(line)
				elif product == "ETH-USD":
					eth_f.write(line)
				else:
					pass # Handle other products or errors (optional)
			except json.JSONDecodeError:
				pass # Handle invalid JSON lines (optional)

def main():
	basefile = "messages"
	data_path = utilities.get_data_path(tree_level=2)
	messages = os.path.join(data_path, f"{basefile}.txt")
	btc_output_file = os.path.join(data_path, f"{basefile}-btc.txt")
	eth_output_file = os.path.join(data_path, f"{basefile}-eth.txt")

	separate_products(messages, btc_output_file, eth_output_file)
	print("Lines separated successfully!")

if __name__ == "__main__":
	main()
