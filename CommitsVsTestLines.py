import json
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

fp = open("retrofit.json", "r")
data = json.load(fp)
fp.close()

for i in data:
    print(i)

xData = []
for i in range(len(data["test_lines_per_commit"])):
    xData.append(i+1)

x = xData
y = data["test_lines_per_commit"]#np.arange(0.0, 2.0, 0.01)

fig, ax = plt.subplots()
ax.scatter(x, y)

ax.set(xlabel="commits", ylabel="Test related LOC", title="Test lines over commits")
ax.grid()
plt.show()
