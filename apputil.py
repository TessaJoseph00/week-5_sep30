import pandas as pd
import plotly.express as px


def survival_demographics():
    """
    Categorizes passengers by age group,and calculates survival 
    statistics grouped by class, sex, and age group.

    Returns:
        Summary with total passengers, survivors, and survival rate.
    """
    url = 'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv'
    df = pd.read_csv(url)

    # Rename the columns in lowercase
    df.rename(columns={'Pclass': 'pclass', 'Sex': 'sex', 'Age': 'age', 'PassengerId': 'passengerid', 'Survived': 'survived'}, inplace=True)

    # Define age bins and labels
    bins = [0, 12, 19, 59, 120]
    labels = ['Child', 'Teen', 'Adult', 'Senior']

    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=True)
    df['age_group'] = df['age_group'].astype('category')

    # Generate all combinations
    all_combinations = pd.MultiIndex.from_product(
        [sorted(df['pclass'].unique()), df['sex'].unique(), df['age_group'].cat.categories],
        names=['pclass', 'sex', 'age_group']
    )

    summary = df.groupby(['pclass', 'sex', 'age_group'], observed=False).agg(
        n_passengers=('passengerid', 'count'),
        n_survivors=('survived', 'sum')
    )

    # To include all combinations, fill missing with 0
    summary = summary.reindex(all_combinations, fill_value=0).reset_index()

    # Calculate survival rate
    summary['survival_rate'] = summary['n_survivors'] / summary['n_passengers']
    summary['survival_rate'] = summary['survival_rate'].fillna(0)
    return summary


def visualize_demographic(summary_df):
    """
    Creates a bar chart showing survival rate by age group, sex, and class.

    Args:
        Summary table from survival_demographics()

    Returns:
        Plotly bar chart figure
    """
    fig = px.bar(
        summary_df,
        x='age_group',
        y='survival_rate',
        color='Sex',
        barmode='group',
        facet_col='Pclass',
        title='Survival Rate by Age Group, Sex, and Class',
        labels={
            'survival_rate': 'Survival Rate',
            'age_group': 'Age Group'
        },
        color_discrete_sequence=['#1f77b4', "#8db3de"]
    )

    fig.update_layout(
        yaxis=dict(tickformat=".0%"),
        bargap=0.15
    )

    return fig

#EXERCISE 2

def family_groups():
    """
    Adds 'family_size' and returns a table grouped by Pclass and family size, 
    showing passenger count and fare statistics.
    """
    df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")
    
    df['family_size'] = df['SibSp'] + df['Parch'] + 1
    grouped = (
        df.groupby(['Pclass', 'family_size'])
        .agg(
            n_passengers=('PassengerId', 'count'),
            avg_fare=('Fare', 'mean'),
            min_fare=('Fare', 'min'),
            max_fare=('Fare', 'max')
        )
        .reset_index()
        .sort_values(by=['Pclass', 'family_size'])[
        ['Pclass', 'family_size', 'n_passengers', 'avg_fare', 'min_fare', 'max_fare']
        ]
    )
    return grouped

def last_names():
    """
    Extracts last names from the Name column and returning the count
    """
    df = pd.read_csv("https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv")

    last_names = df['Name'].apply(lambda x: x.split(',')[0].strip())
    return last_names.value_counts()

def visualize_families(df):
    """
    Visualizing the number of passengers by family size and class, to check if larger families mostly traveled in 3rd class.
    """
    grouped = family_groups(df)

    fig = px.bar(
    grouped,
    x='family_size',
    y='n_passengers',
    color='Pclass',
    barmode='group',
    title='Number of Passengers by Family Size and Class',
    labels={'family_size': 'Family Size', 'n_passengers': 'Passenger Count', 'Pclass': 'Class'},
)
    fig.update_layout(
    xaxis=dict(
        tickmode='linear',
        dtick=1
    )
)
    return fig

if __name__ == "__main__":
    # Loading data
    url = 'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv'
    df = pd.read_csv(url)

    print("\nSurvival Demographics Summary:")
    summary = survival_demographics()
    print(summary.head())

    print("\nFamily Groups Summary:")
    family_summary = family_groups(df)
    print(family_summary.head())

    print("\nLast Names Count (Top 10):")
    last_name_counts = last_names(df)
    print(last_name_counts.head(10))

    print("\nDisplaying Family Groups Visualization:")
    fig = visualize_families(df)
    fig.show()
