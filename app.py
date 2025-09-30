import streamlit as st

from apputil import *

# Load Titanic dataset
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write(
'''
# Titanic Visualization 1: Did children have better survival chances compared to adults or seniors?

'''
)

# Step 2: Prepare data
summary = survival_demographics()

# Step 3: Show summary table
st.dataframe(summary)

# Generate and display the figure
fig1 = visualize_demographic(summary)
st.plotly_chart(fig1, use_container_width=True)


st.write(
'''
# Titanic Visualization 2: 
'''
)
# Generate and display the figure
fig2 = visualize_families()
st.plotly_chart(fig2, use_container_width=True)

st.write(
'''
# Titanic Visualization Bonus
'''
)
# Generate and display the figure
fig3 = visualize_family_size()
st.plotly_chart(fig3, use_container_width=True)