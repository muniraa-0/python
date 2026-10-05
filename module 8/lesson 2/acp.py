import matplotlib.pyplot as plt


weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Week 5']
savings = [20, 45, 70, 110, 150]


plt.plot(weeks, savings)
plt.show()


plt.plot(weeks, savings)
plt.title('My Savings Progress Chart')
plt.xlabel('Week')
plt.ylabel('Savings Amount')
plt.grid(True)
plt.ylim(0, 180)
plt.show()

plt.plot(weeks, savings, color='blue', marker='o',
         linestyle='dashed', linewidth=2)

plt.title('My Savings Progress Chart')
plt.xlabel('Week')
plt.ylabel('Savings Amount')
plt.grid(True)
plt.ylim(0, 180)
plt.show()


plt.bar(weeks, savings, color='orange')

plt.title('My Savings Bar Chart')
plt.xlabel('Week')
plt.ylabel('Savings Amount')
plt.ylim(0, 180)
plt.show()
