import csv, matplotlib.pyplot as plt, numpy as np

file = open("results.txt","r")
csvreader = csv.reader(file)

header = []
header = next(csvreader)
print(header)

sizes = []
timesLocal =[]
timesOff1 =[]
timesOff3 =[]

for row in csvreader:
    sizes.append(row[0])
    timesLocal.append(row[1])
    timesOff1.append(row[2])
    timesOff3.append(row[3])
file.close()

ypoints = np.array(sizes)

default_x_ticks = range(0,30,5)

fig, ax = plt.subplots()


plt.title("")
ax.set_xticks(default_x_ticks)
ax.plot(timesLocal,sizes, label="Local")
ax.plot(timesOff1,sizes, label="Offload 1")
ax.plot(timesOff3,sizes, label="Offload 3")

ax.legend()
plt.show()
