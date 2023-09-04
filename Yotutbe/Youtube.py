#importing the necessary libraries
import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
import mysql.connector as sql
import pymongo
import datetime
import isodate
from googleapiclient.discovery import build

# SETTING PAGE CONFIGURATIONS

st.set_page_config(page_title= "Youtube Data Harvesting and Warehousing ",
                   
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={'About': """# This app is analysis youtube channel"""})

# CREATING OPTION MENU
with st.sidebar:
    selected = option_menu(None, ["Extract and Transform","View"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#C80101"},
                                   "icon": {"font-size": "30px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#F44336"}})

# Bridging a connection with MongoDB Atlas and Creating a new database(youtube_data)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['youtube_data']

# CONNECTING WITH MYSQL DATABASE
mydb = sql.connect(host="localhost",
                   user="root",
                   password="123456",
                   database= "youtube_db"
                  )
mycursor = mydb.cursor(buffered=True)

# BUILDING CONNECTION WITH YOUTUBE API
api_key = "AIzaSyDwRTgFFHmLkPbRWsNQFRxWKfJ3LO77rzk"
youtube = build('youtube','v3',developerKey=api_key)

#Function to duration
   

# FUNCTION TO GET CHANNEL DETAILS
def get_channel_details(channel_id):
    ch_data = []
    response = youtube.channels().list(part = 'snippet,contentDetails,statistics',
                                     id= channel_id).execute()

    for i in range(len(response['items'])):
        data = dict(Channel_id = channel_id[i],
                    Channel_name = response['items'][i]['snippet']['title'],
                    Playlist_id = response['items'][i]['contentDetails']['relatedPlaylists']['uploads'],
                    Subscribers = response['items'][i]['statistics']['subscriberCount'],
                    Views = response['items'][i]['statistics']['viewCount'],
                    Total_videos = response['items'][i]['statistics']['videoCount'],
                    Description = response['items'][i]['snippet']['description']
                    )
        ch_data.append(data)
    return ch_data


# FUNCTION TO GET VIDEO IDS
def get_channel_videos(channel_id):
    video_ids = []
    # get Uploads playlist id
    res = youtube.channels().list(id=channel_id, 
                                  part='contentDetails').execute()
    playlist_id = res['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token = None
    
    while True:
        res = youtube.playlistItems().list(playlistId=playlist_id, 
                                           part='snippet', 
                                           maxResults=50,
                                           pageToken=next_page_token).execute()
        
        for i in range(len(res['items'])):
            video_ids.append(res['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token = res.get('nextPageToken')
        
        if next_page_token is None:
            break
    return video_ids


# FUNCTION TO GET VIDEO DETAILS
def get_video_details(v_ids):
    video_stats = []
    
    for i in range(0, len(v_ids), 50):
        response = youtube.videos().list(
                    part="snippet,contentDetails,statistics",
                    id=','.join(v_ids[i:i+50])).execute()
        for video in response['items']:
            video_details = dict(Channel_name = video['snippet']['channelTitle'],
                                Channel_id = video['snippet']['channelId'],
                                Video_id = video['id'],
                                Title = video['snippet']['title'],
                                Tags = video['snippet'].get('tags'),
                                Thumbnail = video['snippet']['thumbnails']['default']['url'],
                                Description = video['snippet']['description'],
                                Published_date = video['snippet']['publishedAt'],
                                Duration =isodate.parse_duration((video['contentDetails']['duration'])).total_seconds(),
                                Views = video['statistics']['viewCount'],
                                Likes = video['statistics'].get('likeCount'),
                                Comments = video['statistics'].get('commentCount'),
                                Favorite_count = video['statistics']['favoriteCount'],
                                Dislike_count=video['statistics'].get('dislikeCount'),
                                Caption_status = video['contentDetails']['caption'] )
            video_stats.append(video_details)
    return video_stats


# FUNCTION TO GET COMMENT DETAILS
def get_comments_details(v_id):
    comment_data = []
    try:
        next_page_token = None
        while True:
            response = youtube.commentThreads().list(part="snippet,replies",
                                                    videoId=v_id,
                                                    maxResults=100,
                                                    pageToken=next_page_token).execute()
            for cmt in response['items']:
                data = dict(Comment_id = cmt['id'],
                            Video_id = cmt['snippet']['videoId'],
                            Comment_text = cmt['snippet']['topLevelComment']['snippet']['textDisplay'],
                            Comment_author = cmt['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                            Comment_posted_date = cmt['snippet']['topLevelComment']['snippet']['publishedAt'],
                            #Like_count = cmt['snippet']['topLevelComment']['snippet']['likeCount'],
                            #Reply_count = cmt['snippet']['totalReplyCount']
                           )
                comment_data.append(data)
            next_page_token = response.get('nextPageToken')
            if next_page_token is None:
                break
    except:
        pass
    return comment_data


# FUNCTION TO GET CHANNEL NAMES FROM MONGODB
def channel_names():   
    ch_name = []
    for i in db.channel_details.find():
        ch_name.append(i['Channel_name'])
    return ch_name


    
    
# EXTRACT and TRANSFORM PAGE
if selected == "Extract and Transform":
    tab1,tab2 = st.tabs(["$\huge EXTRACT $", "$\huge TRANSFORM $"])
    
    # EXTRACT TAB
    with tab1:
        st.markdown("#    ")
        st.write("### Enter YouTube Channel_ID below :")
        ch_id = st.text_input(" ").split(',')

        if ch_id and st.button("Extract Data"):
            ch_details = get_channel_details(ch_id)
            st.write(f'#### Extracted data from :red["{ch_details[0]["Channel_name"]}"] channel')
            st.table(ch_details)

        if st.button("Upload to MongoDB"):
            with st.spinner('Please Wait for it...'):
                ch_details = get_channel_details(ch_id)
                v_ids = get_channel_videos(ch_id)
                vid_details = get_video_details(v_ids)
                
                def comments():
                    com_d = []
                    for i in v_ids:
                        com_d+= get_comments_details(i)
                    return com_d
                comm_details = comments()

                collections1 = db.channel_details
                collections1.insert_many(ch_details)

                collections2 = db.video_details
                collections2.insert_many(vid_details)

                collections3 = db.comments_details
                collections3.insert_many(comm_details)
                st.success("Upload to MogoDB successful !!")
      
    # TRANSFORM TAB
    with tab2:     
        st.markdown("#   ")
        st.markdown("#### Select a channel to begin Transformation to SQL")
        
        ch_names = channel_names()
        user_inp = st.selectbox("Select channel",options= ch_names)
        
        def insert_into_channels():
                collections = db.channel_details
                mycursor = mydb.cursor()
                #CREATE TABLE for channelsdetails
                channeltable = f"""CREATE TABLE IF NOT EXISTS channelsdetails
                        (
                        Channel_name VARCHAR(255),
                        Channel_ID VARCHAR(255),
                        Playlist_ID VARCHAR(255),
                        Subscribers INT,
                        Views INT,
                        Totalvideos INT,
                        Description TEXT
                       )"""

                mycursor.execute(channeltable)
                mydb.commit()

                query = """INSERT INTO channelsdetails VALUES(%s,%s,%s,%s,%s,%s,%s)"""
                
                for i in collections.find({"Channel_name" : user_inp},{'_id':0}):
                    mycursor.execute(query,tuple(i.values()))
                    mydb.commit()
                
        def insert_into_videos():
            collectionss = db.video_details
          #CREATE TABLE for video
            chan = f"""CREATE TABLE IF NOT EXISTS videodatass 
            (
                  Channel_name VARCHAR(255),
                  Channel_id  VARCHAR(255),
                  Video_id VARCHAR(255),
                  Title TEXT,
                  Thumbnail VARCHAR(255),
                  Description TEXT,
                  Published_date VARCHAR(255),
                  Duration TIME,
                  Views INT,
                  Likes INT,
                  Comments INT,
                  Favorite_count INT,
                  Dislike_count INT,
                  Caption_status VARCHAR(255)
           )"""
            mycursor.execute(chan)
            mydb.commit()
    

            query1 = """INSERT INTO videodatass VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""


            for i in collectionss.find({"Channel_name" : user_inp},{"_id":0,"Tags":0}):
                t=tuple(i.values())
                mycursor.execute(query1,t)
                mydb.commit()

        def insert_into_comments():
            collections1 = db.video_details
            collections2 = db.comments_details
            #CREATE TABLE ccomment
            chan2= f"""CREATE TABLE IF NOT EXISTS comments
            (
            Video_id VARCHAR(255),
            Comment_id VARCHAR(255),
            Comment_text TEXT,
            Comment_author VARCHAR(255),
            Comment_PublishedAt VARCHAR(255)
            )"""

            mycursor.execute(chan2)
            mydb.commit()

            query2 = """INSERT INTO comments VALUES(%s,%s,%s,%s,%s)"""

            for vid in collections1.find({"Channel_name" :user_inp},{'_id' : 0}):
                for i in collections2.find({'Video_id': vid['Video_id']},{'_id' : 0}):
                    t=tuple(i.values())
                    mycursor.execute(query2,t)
                    mydb.commit()

        if st.button("Submit"):
                insert_into_channels()
                insert_into_videos()
                insert_into_comments()
                st.success("Transformation to MySQL Successful!!!")
            
            
# VIEW PAGE
if selected == "View":
    
    st.write("## :orange[Select any question to get Insights]")
    questions = st.selectbox('Questions',
    ['Click the question that you would like to query',
    '1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top 10 most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in the year 2022?',
    '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])
    
    if questions == '1. What are the names of all the videos and their corresponding channels?':
        mycursor.execute("""SELECT Title AS Video_Title, Channel_name AS Channel_Name FROM videodatass ORDER BY Channel_name""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        mycursor.execute("""SELECT channel_name 
        AS Channel_Name, Totalvideos AS Totalvideos
                            FROM channelsdetails
                            ORDER BY Totalvideos DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Number of videos in each channel :]")
        #st.bar_chart(df,x= mycursor.column_names[0],y= mycursor.column_names[1])
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, Title AS Video_Title, Views AS Views 
                            FROM videodatass
                            ORDER BY Views DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :red[Top 10 most viewed videos :]")
        fig = px.bar(df,
                     x=mycursor.column_names[2],
                     y=mycursor.column_names[1],
                     orientation='h',
                     color=mycursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT a.Video_id AS Video_id, a.Title AS Video_Title,a.Comments
                            FROM videodatass AS a
                            LEFT JOIN (SELECT Video_id,COUNT(Comment_id) AS Total_Comments
                            FROM comments GROUP BY Video_id) AS b
                            ON a.Video_id = b.Video_id
                            ORDER BY a.Comments DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
          
    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        mycursor.execute("""SELECT Channel_name AS Channel_Name,Title AS Title,Likes AS Likes_Count 
                            FROM videodatass
                            ORDER BY Likes DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :blue[Top 10 most liked videos :]")
        fig = px.bar(df,
                     x=mycursor.column_names[2],
                     y=mycursor.column_names[1],
                     orientation='h',
                     color=mycursor.column_names[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT Title AS Title, Likes AS Likes_Count
                            FROM videodatass
                            ORDER BY Likes DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
         
    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT Channel_name AS Channel_Name, Views AS Views
                            FROM channelsdetails
                            ORDER BY Views DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :red[Channels vs Views :]")
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                    )
        fig.update_traces(marker_color='green')
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        mycursor.execute("""SELECT Channel_name AS Channel_Name
                            FROM videodatass
                            WHERE Published_date LIKE '2022%'
                            GROUP BY Channel_name
                            ORDER BY Channel_name""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        
    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT Channel_name AS Channel_Name,
                            AVG(Duration)/60 AS "Average_Video_Duration (secs)"
                            FROM videodatass
                            GROUP BY Channel_name
                            ORDER BY AVG(Duration)/60 DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Avg video duration for channels :]")
        fig = px.bar(df,
                     x=mycursor.column_names[0],
                     y=mycursor.column_names[1],
                     orientation='v',
                     color=mycursor.column_names[0]
                    )
        fig.update_traces(marker_color='red')
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name,Video_id AS Video_ID,Comments AS Comments
                            FROM videodatass
                            ORDER BY Comments DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(),columns=mycursor.column_names)
        st.write(df)
        st.write("### :green[Videos with most comments :]")
        fig = px.bar(df,
                     x=mycursor.column_names[1],
                     y=mycursor.column_names[2],
                     orientation='v',
                     color=mycursor.column_names[0]
                    )
        fig.update_traces(marker_color='green')
        st.plotly_chart(fig,use_container_width=True)

