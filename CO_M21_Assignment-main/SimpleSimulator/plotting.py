from main import Cycle_number
from main import memory_address_accessed
from matplotlib import pyplot as plt
plt.scatter(Cycle_number,memory_address_accessed,s=120,marker="o",color="cyan",edgecolor='black',linewidths=1.5,hatch='//////')
plt.title=("Cycle vs Memory Address")
plt.xlabel("Cycle Number")
plt.ylabel("Memory Address Accessed")
plt.show()