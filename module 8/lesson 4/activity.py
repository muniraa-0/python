import seaborn as sns
import matplotlib.pyplot as plt

df = sns.load_dataset('titanic')
df.dropna()
print(df.head())
print(df.info())
print(df.describe())
print("survived:",df['survived'].value_counts())
print("pclass:",df['pclass'].value_counts())

sns.histplot(data=df, x='age',bins=30, color='blue',)
plt.title('Distribution of Age')
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()

sns.kdeplot(data=df, x='age', hue='survived', fill=True)
plt.title('Kernel Density Estimate of Age by Survival Status')
plt.xlabel('Age')
plt.ylabel('Density')
plt.show()

sns.scatterplot(data=df, x='age', y='fare', hue='survived')
plt.title('Scatter Plot of Age vs Fare by Survival Status')
plt.xlabel('Age')
plt.ylabel('Fare')
plt.show()

corr = df.corr(numeric_only=True)
print(corr)
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()