import streamlit as st

from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

# Prepare data
summary = survival_demographics()

#Display summary table
st.subheader("Survival Rate by Passenger Class, Sex, and Age Group")
st.dataframe(summary)

st.write(
'''
# Titanic Visualization 1: Did children have better survival chances compared to adults or seniors?
'''
)
# Generate and display the bargraph
fig1 = visualize_demographic(summary)
st.plotly_chart(fig1, use_container_width=True)

#exercise 2
# Questions 1–3: Grouping by family size and class
grouped_df = family_groups(df)
st.subheader("Here is the grouped summary table showing average, min, and max fares by family size and class:")
st.dataframe(grouped_df)

#4. Most Common Last Names
st.header("Most Common Last Names on the Titanic")
last_name_counts = last_names(df)

last_name_df = last_name_counts.head().reset_index()
last_name_df.columns = ['Last Name', 'Count']

#CSS to customise count column
st.dataframe(
    last_name_df,
    use_container_width=False,
    column_config={
        "Count": st.column_config.NumberColumn(
            width="small",
            format="%d"
        )
    },
    hide_index=True
)

#st.table(last_name_df)
st.markdown("""
**Findings:**  
We noticed that some last names, like Andersson and Sage, show up many times in the data.
This suggests that those people were part of big families. When we look at the family size 
table, we can also see large groups of passengers with the same last name, which means they 
likely traveled together as a family.""")

st.write(
'''
# Titanic Visualization 2: Were larger families more likely to travel in 3rd class, possibly due to lower fares?
'''
)
# Generate and display the figure
fig2 = visualize_families(df)
st.plotly_chart(fig2, use_container_width=True)
st.write(
    "The chart shows that most large families were indeed in 3rd class, while smaller families "
    "or solo travelers were more common in 1st and 2nd class. This supports the idea that wealthier " \
    "passengers likely traveled in smaller groups."
)
st.write(
'''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
#fig3 = visualize_family_size()
#st.plotly_chart(fig3, use_container_width=True)