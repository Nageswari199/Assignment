

import mysql.connector as sql
import pandas as pd
import os
import json
import git
import sqlalchemy
from sqlalchemy import text
import streamlit as st
import plotly.express as px

from streamlit_option_menu import option_menu


#cloning the phonepay github repository
# repo_url='https://github.com/phonepe/pulse.git'

# clone_directory='I:\Projects\Phonepay'

# git.Repo.clone_from(repo_url,clone_directory)



#dataframe for aggr_user

path1 = "I:/Projects/Phonepay/data/aggregated/transaction/country/india/state/"
agg_transaction_list = os.listdir(path1)

data1 = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],
            'Transaction_amount': []}
for state in agg_transaction_list:
    current_state = path1 + state + "/"
    agg_year_list = os.listdir(current_state)
    
    for year in agg_year_list:
        current_year = current_state + year + "/"
        agg_file_list = os.listdir(current_year)
        
        for file in agg_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            A = json.load(data)
            
            for i in A['data']['transactionData']:
                name = i['name']
                count = i['paymentInstruments'][0]['count']
                amount = i['paymentInstruments'][0]['amount']
                data1['Transaction_type'].append(name)
                data1['Transaction_count'].append(count)
                data1['Transaction_amount'].append(amount)
                data1['State'].append(state)
                data1['Year'].append(year)
                data1['Quarter'].append(int(file.strip('.json')))
                
df_agg_trans = pd.DataFrame(data1)

df_agg_trans.drop_duplicates()


#dataframe for aggr_user

path2 = "I:/Projects/Phonepay/data/aggregated/user/country/india/state/"


agg_user_list = os.listdir(path2)

data2 = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'Count': [],
            'Percentage': []}
for state in agg_user_list:
    current_state = path2 + state + "/"
    agg_year_list = os.listdir(current_state)
    
    for year in agg_year_list:
        current_year = current_state + year + "/"
        agg_file_list = os.listdir(current_year)
        
        for file in agg_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            B= json.load(data)
            try:
                for i in B["data"]["usersByDevice"]:
                    brand_name = i["brand"]
                    counts = i["count"]
                    percents = i["percentage"]
                    data2["Brands"].append(brand_name)
                    data2["Count"].append(counts)
                    data2["Percentage"].append(percents)
                    data2["State"].append(state)
                    data2["Year"].append(year)
                    data2["Quarter"].append(int(file.strip('.json')))
            except:
                pass
df_aggr_user = pd.DataFrame(data2)



#dataframe for map_trans

path3 = "I:/Projects/Phonepay/data/map/transaction/hover/country/india/state/"

map_transaction_list = os.listdir(path3)

data3= {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Count': [],
            'Amount': []}

for state in map_transaction_list:
    current_state = path3 + state + "/"
    map_year_list = os.listdir(current_state)
    
    for year in map_year_list:
        current_year = current_state + year + "/"
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            C = json.load(data)
            
            for i in C["data"]["hoverDataList"]:
                district = i["name"]
                count = i["metric"][0]["count"]
                amount = i["metric"][0]["amount"]
                data3["District"].append(district)
                data3["Count"].append(count)
                data3["Amount"].append(amount)
                data3['State'].append(state)
                data3['Year'].append(year)
                data3['Quarter'].append(int(file.strip('.json')))
                
df_map_trans = pd.DataFrame(data3)

df_map_trans.drop_duplicates()


##Data Frame of mapp user
path4 = "I:/Projects/Phonepay/data/map/user/hover/country/india/state/"

map_users_list = os.listdir(path4)

data4= {"State": [], "Year": [], "Quarter": [], "District": [],
            "RegisteredUser": [], "AppOpens": []}

for state in map_users_list:
    current_state = path4 + state + "/"
    map_year_list = os.listdir(current_state)
    
    for year in map_year_list:
        current_year = current_state + year + "/"
        map_file_list = os.listdir(current_year)
        
        for file in map_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            D = json.load(data)
            
            for i in D["data"]["hoverData"].items():
                district = i[0]
                registereduser = i[1]["registeredUsers"]
                appOpens = i[1]['appOpens']
                data4["District"].append(district)
                data4["RegisteredUser"].append(registereduser)
                data4["AppOpens"].append(appOpens)
                data4['State'].append(state)
                data4['Year'].append(year)
                data4['Quarter'].append(int(file.strip('.json')))
                
df_map_user = pd.DataFrame(data4)


df_map_user.drop_duplicates()

#dataframe for top_trans
path5 = "I:/Projects/Phonepay/data/top/transaction/country/india/state/"

top_transaction_list = os.listdir(path5)
data5= {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [], 'Transaction_count': [],
            'Transaction_amount': []}

for state in top_transaction_list:
    current_state = path5 + state + "/"
    top_year_list = os.listdir(current_state)
    
    for year in top_year_list:
        current_year = current_state + year + "/"
        top_file_list = os.listdir(current_year)
        
        for file in top_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            E=json.load(data)
            
            
            for i in E['data']['pincodes']:
                name = i['entityName']
                count = i['metric']['count']
                amount = i['metric']['amount']
                data5['Pincode'].append(name)
                data5['Transaction_count'].append(count)
                data5['Transaction_amount'].append(amount)
                data5['State'].append(state)
                data5['Year'].append(year)
                data5['Quarter'].append(int(file.strip('.json')))
df_top_trans = pd.DataFrame(data5)


#dataframe for top_user

path6 = "I:/Projects/Phonepay/data/top/user/country/india/state/"
top_users_list = os.listdir(path6)
data6 = {'State': [], 'Year': [], 'Quarter': [], 'Pincode': [],
            'RegisteredUsers': []}

for state in top_users_list:
    current_state = path6 + state + "/"
    top_year_list = os.listdir(current_state)
    
    for year in top_year_list:
        current_year = current_state + year + "/"
        top_file_list = os.listdir(current_year)
        
        for file in top_file_list:
            current_file = current_year + file
            data = open(current_file, 'r')
            F=json.load(data)
            
            for i in F['data']['pincodes']:
                name = i['name']
                registeredUsers = i['registeredUsers']
                data6['Pincode'].append(name)
                data6['RegisteredUsers'].append(registeredUsers)
                data6['State'].append(state)
                data6['Year'].append(year)
                data6['Quarter'].append(int(file.strip('.json')))
df_top_user = pd.DataFrame(data6) 


##loading the data to corresponding csv

# df_agg_trans.to_csv('agg_trans.csv',index=False)
# df_aggr_user.to_csv('agg_user.csv',index=False)
# df_map_trans.to_csv('map_trans.csv',index=False)
# df_map_user.to_csv('map_user.csv',index=False)
# df_top_trans.to_csv('top_trans.csv',index=False)
# df_top_user.to_csv('top_user.csv',index=False)

#creating connection for sqlalchemy

user = 'root'
password = '123456'
host = 'localhost'
port = 3306
database = 'Phonepe_pulse'
mydb= sqlalchemy.create_engine("mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        ))


#connection object for mysql
myconn=sql.connect(host="localhost",
                   user="root",
                   password="123456",
                   database= "Phonepe_pulse"
                  )
mycursor = myconn.cursor(buffered=True)


#creating the database
mycursor.execute("CREATE DATABASE Phonepe_pulse")
mycursor.execute("USE Phonepe_pulse")


#creating the aggr_trans table
agg_trans= f"""CREATE TABLE  IF NOT EXISTS aggr_trans(State varchar(100), 
                        Year int, Quarter int, 
                        Transaction_type varchar(100), 
                        Transaction_count int, 
                        Transaction_amount double)
            """
mydb.execute(agg_trans)

#inserting data into table aggr_trans
df = pd.read_csv('C:\\Users\\Admin\\agg_trans.csv')
df.to_sql('aggr_trans',con=mydb, if_exists= "replace",index=False, chunksize=1000)


#creating the table aggr_user
agg_user= f"""CREATE TABLE  IF NOT EXISTS aggr_user(State varchar(100), 
                                    Year int, Quarter int,
                                    Brands varchar(100),
                                    Count int,
                                    Percentage double)
          """
mydb.execute(agg_user)

#inserting datainto aggr_user
df = pd.read_csv('C:\\Users\\Admin\\agg_user.csv')
df.to_sql('aggr_user',con=mydb, if_exists= "replace",index=False, chunksize=1000)


#creating the table map_trans
map_trans= f"""CREATE TABLE  IF NOT EXISTS map_trans(State varchar(100), 
                            Year int, Quarter int,
                            District varchar(100), 
                            Count int, 
                            Amount double)
          """

#Inserting data into table map_trans
mydb.execute(map_trans)
df = pd.read_csv('C:\\Users\\Admin\\map_trans.csv')
df.to_sql('map_trans',con=mydb, if_exists= "replace",index=False, chunksize=1000)


#creating the table map_user
map_user= f"""CREATE TABLE  IF NOT EXISTS map_user(State varchar(100), 
                            Year int, Quarter int,
                            District varchar(100), 
                            Registered_Users int, 
                            App_Open int)
          """
#inserting data into map_user
mydb.execute(map_user)
df = pd.read_csv('C:\\Users\\Admin\\map_user.csv')
df.to_sql('map_user',con=mydb, if_exists= "replace",index=False, chunksize=1000)


#creating table top_tran
top_trans= f"""CREATE TABLE  IF NOT EXISTS top_tran(State varchar(100), 
                                                Year int, Quarter int,
                                                Pincode int,
                                                Transaction_count int, 
                                                Transaction_amount double)
          """

#inserting into top_tran
mydb.execute(top_tran)
df = pd.read_csv('C:\\Users\\Admin\\top_trans.csv')
df.to_sql('top_trans',con=mydb, if_exists= "replace",index=False, chunksize=1000)


#creating table top user
top_user= f"""CREATE TABLE  IF NOT EXISTS top_user(State varchar(100),
                        Year int, Quarter int, 
                        Pincode int, 
                        Registered_users int)
          """

#inserting data into top user
mydb.execute(top_user)
df = pd.read_csv('C:\\Users\\Admin\\top_user.csv')
df.to_sql('top_user',con=mydb, if_exists= "replace",index=False, chunksize=1000)


##streamlit page configurations
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This dashboard app is created by *Nageswari sampath*!
                                        Data has been cloned from Phonepe Pulse Github Repository"""})

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")

#sidebar
with st.sidebar:
    selected = option_menu("Menu", ["Top Charts","Explore Data","About"], 
                icons=["graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

#MENU 1 - TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :red[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    colum1,colum2= st.columns([1,1.5],gap="large")
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with colum2:
        st.info(
                """
                #### From this menu we can get insights like :
                - Overall ranking on a particular Year and Quarter.
                - Top 10 State, District, Pincode based on Total number of transaction and Total amount spent on phonepe.
                - Top 10 State, District, Pincode based on Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="🔍"
                )
#TOP Charts - Transactions
    if Type == "Transactions":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
    with col1:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from aggr_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Peach,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
    with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.pie(df, values='Total_Amount',
                             names='District',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Plasma_r,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
    with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
            fig = px.pie(df, values='Total_Amount',
                             names='Pincode',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Agsunset,
                             hover_data=['Transactions_Count'],
                             labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
# Top Charts - USERS          
    if Type == "Users":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
    with col1:
            st.markdown("### :violet[Brands]")
            if Year == 2023 and Quarter in [3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 3,4")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from aggr_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Mint)
                st.plotly_chart(fig,use_container_width=True)   
    
    with col2:
            st.markdown("### :violet[District]")
            mycursor.execute(f"select district, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.Plasma_r)
            st.plotly_chart(fig,use_container_width=True)
              
    with col3:
            st.markdown("### :violet[Pincode]")
            mycursor.execute(f"select Pincode, sum(RegisteredUsers) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.Agsunset,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
    
    with col4:
            st.markdown("### :violet[State]")
            mycursor.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.Purp,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

if selected == "Explore Data":
    Year = st.sidebar.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
    
# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year =                   {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv("C:\\Users\\Admin\\Statename.csv")
            df1.State = df2
            

            fig=px.choropleth(df1,
                                   geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv("C:\\Users\\Admin\\Statename.csv")
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig=px.choropleth(df1,
                                           geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_Transactions',
                      color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
   
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Peach)
        st.plotly_chart(fig,use_container_width=True)
         
    if Type == "Users":
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select state, sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        df2 = pd.read_csv("C:\\Users\\Admin\\Statename.csv")
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2
        
        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        mycursor.execute(f"select State,year,quarter,District,sum(RegisteredUser) as Total_Users, sum(AppOpens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)
        
        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Mint)
        st.plotly_chart(fig,use_container_width=True)

        
#MENU-ABOUT
if selected == "About":
        col1,col2 = st.columns([3,3],gap="medium")
        with col1:
            st.write(" ")
            st.write(" ")
            st.markdown("### :violet[About PhonePe Pulse:] ")
            st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
            st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        st.write("**:violet[Image and content source]** ⬇️")
        st.write("https://www.prnewswire.com/in/news-releases/phonepe-launches-the-pulse-of-digital-payments-india-s-first-interactive-geospatial-website-888262738.html")
        
        with col2:
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
        












