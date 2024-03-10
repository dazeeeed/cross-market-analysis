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

def separate_products_equalize(input_file, btc_output_file, eth_output_file):
	"""
	Separates lines with "BTC" or "ETH" product value in a JSON file to different files,
	ensuring equal row counts by duplicating lines for the product with fewer observations.
	Maintains only the most recent line for each product.
	"""

	with open(input_file, "r") as input_f, \
		 open(btc_output_file, "w") as btc_f, \
		 open(eth_output_file, "w") as eth_f:

		previous_line = {"BTC-USD": None, "ETH-USD": None}

		for i, line in enumerate(input_f):
			if i == 0:
				continue  # Skip the first line

			try:
				data = json.loads(line)
				product = data["product_id"]

				# Write the current line to its respective file
				output_f = btc_f if product == "BTC-USD" else eth_f
				output_f.write(line)

				# Update the previous line for the current product
				previous_line[product] = line

				# Ensure equal row counts
				for other_product in ("BTC-USD", "ETH-USD"):
					if product != other_product:
						other_line = previous_line[other_product]
						if other_line and len(output_f.readlines()) < len(previous_line[product]):
							# Duplicate the current line if necessary
							output_f.write(line)

			except json.JSONDecodeError:
				pass  # Handle invalid JSON lines (optional)

			if i == 20:
				break

def main():
	basefile = "messages"
	data_path = utilities.get_data_path(tree_level=2)
	messages = os.path.join(data_path, f"{basefile}.txt")
	btc_output_file = os.path.join(data_path, f"{basefile}-btc_equalized.txt")
	eth_output_file = os.path.join(data_path, f"{basefile}-eth_equalized.txt")

	# separate_products(messages, btc_output_file, eth_output_file)
	separate_products_equalize(messages, btc_output_file, eth_output_file)

	print("Lines separated successfully!")

if __name__ == "__main__":
	main()
