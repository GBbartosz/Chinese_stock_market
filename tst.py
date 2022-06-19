# ktore sprawozdanai nie są w yuanach
# porównać kapitalizację
# barchart dla dat


import matplotlib.pyplot as plt

#data = {'apples': 10, 'oranges': 15, 'lemons': 5, 'limes': 20}
#names = list(data.keys())
#values = list(data.values())
#
#fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
#axs[0].bar(names, values)
#axs[1].scatter(names, values)
#axs[2].plot(names, values)
#fig.suptitle('Categorical Plotting')


fig, axs = plt.subplots(1, 2)
#plt.subplot(1,1,1)
#axs[0] = fig.add_axes([0,0,1,1])
name = ['a', 'b']
val = [5, 7]
axs[0].bar(name, val)

#plt.subplot(1,2,2)
#axs[1] = fig.add_axes([0,0,1,1])
langs = ['C', 'C++', 'Java', 'Python', 'PHP']
students = [23,17,35,29,12]
axs[1].bar(langs, students)

plt.show()


