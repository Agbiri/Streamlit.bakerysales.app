import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt




@st.cache_data
def load_data():
    
    df= pd.read_csv('dataset/Bakery sales.csv')
    df.drop(columns=['Unnamed: 0'], inplace=True) 
    df['unit_price2']=df.unit_price.str.replace('€','')
    df['unit_price2']=df.unit_price2.str.replace(',','.')
    df['unit_price2']=df.unit_price2.str.strip()
    df['unit_price2']=df.unit_price2.astype('float')
    df['sales'] = df.Quantity* df.unit_price2 #calculation
    df.drop('unit_price', axis=1, inplace=True)
    st.write(df.shape)
    df.drop(df[df.sales == 0].index, inplace = True) # drop sales with sales
    # convert data to date and time type
    df['date2'] = pd.to_datetime(df.date)
   
    
   # df.to_csv() to save the cleaned data
    
    return df
    
    return df.head(10)

st.title('Bakery Sales Data')


try:
    df= load_data()
    articles= df.article.unique()
    articles_selection = st.multiselect(
        'choose product',articles, [articles[0],articles[1]]
    )

    articles_selected= df[df['article'].isin(articles_selection)]
    st.write(articles_selected.head())
    
    # bar chart
    st.write("""### Total Sales of Selected Products(s)""")
    bar1 = articles_selected.groupby(['article'])['sales'].sum().sort_values(ascending=True)
    st.bar_chart(bar1)
 
    #line
    st.write("""### Sales over Time""")
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(articles_selected['date2'], articles_selected['sales'])
    st.pyplot(fig)
    
    # pie chart
    st.write("""### percentage of selected product(s) sold""")
    pie_data = articles_selected['article'].value_counts()
    fig2, ax2= plt.subplots(figsize=(7,7))
    ax2.pie(pie_data, labels=pie_data.index,autopct='%1.1f%%',shadow = True)
    ax2.axis('equal') # give equal aspect ratio 
    st.write('Note: this is showing percentages for only the values selected')
    st.pyplot(fig2)
except ValueError as e:
        st.error("""
                Error:
            """ % e.reason)
            
    
#st.write(df.dtypes)


