import pandas as pd
import plotly.express as px


def survival_demographics():
    """
    Loads Titanic dataset, categorizes passengers by age group,
    and calculates survival statistics grouped by class, sex, and age group.

    Returns:
        Summary with total passengers, survivors, and survival rate.
    """
    url = 'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv'
    df = pd.read_csv(url)

    # Define age bins and labels
    bins = [0, 12, 19, 59, 120]
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    df['age_group'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

    # Dropping rows with missing age group
    df = df.dropna(subset=['age_group'])

    # Grouping and calculating count
    summary = df.groupby(['Pclass', 'Sex', 'age_group'], observed=False).agg(
        n_passengers=('PassengerId', 'count'),
        n_survivors=('Survived', 'sum')
    ).reset_index()

    # Calculate survival rate
    summary['survival_rate'] = summary['n_survivors'] / summary['n_passengers']

    return summary


def visualize_demographic(summary_df):
    """
    Creates a bar chart showing survival rate by age group, sex, and class.

    Args:
        summary_df (pd.DataFrame): Summary table from survival_demographics()

    Returns:
        plotly.graph_objects.Figure: Plotly bar chart figure
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