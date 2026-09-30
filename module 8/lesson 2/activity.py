import matplotlib.pyplot as plt

day = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
scores = [70, 85, 90, 75, 80, 95, 100]

plt.plot(day, scores)
plt.show()

plt.plot(day, scores)
plt.title('Scores by Day of the Week')
plt.xlabel('Day of the Week')
plt.ylabel('Scores')
plt.grid(True)
plt.ylim(0, 100)
plt.show()

plt.plot(day, scores, color='blue', marker='o', linestyle='dashed', linewidth=2)
plt.title('My quiz score tracker')
plt.xlabel('Day of the Week')
plt.ylabel('Scores')
plt.grid(True)
plt.ylim(0, 100)
plt.show()

plt.bar(day, scores, color='purple')
plt.title('My quiz score tracker')
plt.xlabel('Day of the Week')
plt.ylabel('Scores')
plt.ylim(0, 100)
plt.show()