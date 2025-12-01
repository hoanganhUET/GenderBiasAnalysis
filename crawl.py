import googleapiclient.discovery
import googleapiclient.errors
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = os.getenv('YOUTUBE_API_KEY')

if not DEVELOPER_KEY:
    raise ValueError("Không tìm thấy API key. Vui lòng kiểm tra file .env")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)

request = youtube.commentThreads().list(
    part="snippet",
    videoId="bycK3ikXjQ0",
    maxResults=100
)
response = request.execute()

comments = []

for item in response['items']:
    comment = item['snippet']['topLevelComment']['snippet']
    comments.append([
        comment['authorDisplayName'],
        comment['publishedAt'],
        comment['updatedAt'],
        comment['likeCount'],
        comment['textDisplay']
    ])

df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])

print(df.head(10))

file_exists = os.path.isfile('youtube_comments.csv')

df.to_csv('youtube_comments.csv', 
          mode='a',  
          header=not file_exists, 
          index=False, 
          encoding='utf-8-sig')

print("Đã thêm dữ liệu vào youtube_comments.csv")