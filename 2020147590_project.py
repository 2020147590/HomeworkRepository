import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import MatplotlibDeprecationWarning
import warnings
warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning)


# Reading data from CSV files
data = pd.read_csv('WHR20_DataForFigure.csv')
top_3_countries = data.nlargest(3, 'Ladder score')
bottom_3_countries = data.nsmallest(3, 'Ladder score')
selected_countries = pd.concat([top_3_countries, bottom_3_countries])

plt.figure(figsize=(10, 6))
sns.barplot(x='Country name', y='Ladder score', data=selected_countries, palette='viridis')
plt.title('Top 3 and Bottom 3 Countries by Happiness Index')
plt.xlabel('Country')
plt.ylabel('Happiness Index')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 2. Bar chart of the number of countries in each happiness range
data['Happiness Range'] = pd.cut(data['Ladder score'],
                                 bins=[0, 4, 5, 6, 7, float('inf')],
                                 labels=['<4', '4-5', '5-6', '6-7', '>7'])
# Create dictionaries to store the names of countries within different happiness index intervals
happiness_groups = {}
for group_name, group_data in data.groupby('Happiness Range'):
    happiness_groups[group_name] = list(group_data['Country name'])
# Counting the number of countries in each interval
happiness_counts = data['Happiness Range'].value_counts().sort_index()
plt.figure(figsize=(10, 8))
bars = plt.bar(happiness_counts.index, happiness_counts, color='skyblue')
plt.title('Number of Countries in Each Happiness Range')
plt.xlabel('Happiness Range')
plt.ylabel('Number of Countries')
plt.xticks(rotation=0)
plt.tight_layout()

for i, bar in enumerate(bars):
    height = bar.get_height()
    country_list = happiness_groups[happiness_counts.index[i]]
    formatted_text = ',\n'.join(', '.join(country_list[j:j+4]) for j in range(0, len(country_list), 4))
    plt.text(bar.get_x() + bar.get_width() / 2, height, formatted_text, ha='center', va='bottom',fontsize=8)
plt.show()


#3. Heatmap of correlations between factors influencing the happiness index
core_factors = ['Logged GDP per capita', 'Healthy life expectancy', 'Social support',
                'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']

plt.figure(figsize=(8, 6))
sns.heatmap(data[core_factors].corr(), annot=True, cmap='coolwarm')
plt.title('Correlation between Core Factors of Happiness Index')
plt.tight_layout()
plt.show()



#4. radiographic bar chart
variables = ['Explained by: Log GDP per capita', 'Explained by: Social support', 'Explained by: Healthy life expectancy', 'Explained by: Freedom to make life choices', 'Explained by: Generosity', 'Explained by: Perceptions of corruption']
#Close the graph
values = data.loc[0, variables].values.tolist()
values += values[:1]
#Create Chart
angles = [n / float(len(variables)) * 2 * 3.14159 for n in range(len(variables))]
angles += angles[:1]
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
plt.xticks(angles[:-1], variables, color='black', size=10)
ax.plot(angles, values, linewidth=1, linestyle='solid')
ax.fill(angles, values, 'skyblue', alpha=0.4)
plt.title('Contributions to Ladder Score by Key Variables')
plt.show()

#5. Scatterplot of each key variable vs. happiness index
fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(17, 8))
axes = axes.flatten()
variables = ['Explained by: Log GDP per capita', 'Explained by: Social support', 'Explained by: Healthy life expectancy', 'Explained by: Freedom to make life choices', 'Explained by: Generosity', 'Explained by: Perceptions of corruption', 'Dystopia + residual']

for i, var in enumerate(variables):
    ax = axes[i]
    ax.scatter(data[var], data['Ladder score'])
    ax.set_title(f'{var} vs Ladder Score')
    ax.set_xlabel(var)
    ax.set_ylabel('Ladder Score')
    ax.grid(True)
# Delete blank subgraphs
for i in range(len(variables), len(axes)):
    fig.delaxes(axes[i])
plt.tight_layout()
plt.show()