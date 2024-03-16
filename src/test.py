import numpy as np

x = np.chararray(shape=(10), itemsize=5)

for i in range(10):
    x[i] = "".join(np.random.choice(["a", "b", "c", "d", "e"], size=5))

print(x.decode("utf-8")[1])