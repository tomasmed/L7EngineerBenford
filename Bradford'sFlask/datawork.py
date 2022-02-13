import pandas as pd
import altair as alt

df = pd.read_csv("census_2009b.csv", sep ='\t')

chosen_col = '7_2009'

df['First_Digit'] = df[chosen_col].astype(str).str[0]

print(df[df['First_Digit'] == '0'])

sfg = pd.DataFrame({'Count' : df.groupby( [ 'First_Digit'] ).size()}).reset_index()
dfg = df.groupby(['First_Digit']).size()
dfg.add_suffix('_Count').reset_index()


chart = alt.Chart(sfg).mark_bar().encode(
            x = alt.X("First_Digit:N"),
            y= "Count:Q",
        )

print("\n")
print("\n")
print("\n")
print("\n")
print(sfg)
print(sfg.columns)


# ##Altair Graphing
# alt.renderers.enable('mimetype')
# chart = alt.Chart(df).mark_bar().encode(
#     x = alt.X("First_Digit:N"),
#     y= 'count()',
# )

chart.save('test.html')
# chart.save('test.json')
# print(df.columns)
# print(df.head())