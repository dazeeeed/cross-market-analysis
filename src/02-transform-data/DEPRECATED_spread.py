import os
import pandas as pd
import matplotlib.pyplot as plt

def calculate_quoted_spread(best_ask, best_bid):
    return best_ask - best_bid

def main():
    src_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.abspath(os.path.join(src_path, '../', 'data'))

    data = pd.read_csv(os.path.join(data_path, "BTCUSDT-bookTicker-2023-10-02-short.csv"))
    data["quoted_spread"] = calculate_quoted_spread(data["best_ask_price"], data["best_bid_price"])

    fig, ax = plt.subplots()
    ax.plot(data["quoted_spread"])
    plt.show()
    print(data)


if __name__ == "__main__":
    main()