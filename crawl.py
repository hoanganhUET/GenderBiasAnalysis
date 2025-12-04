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

comments = []
next_page_token = None

while True:
    request = youtube.commentThreads().list(
        part="snippet",
        videoId="qeJ_i_yOpkM",
        maxResults=100,
        pageToken=next_page_token
    )
    response = request.execute()

    for item in response['items']:
        comment = item['snippet']['topLevelComment']['snippet']
        comments.append([
            comment['authorDisplayName'],
            comment['publishedAt'],
            comment['updatedAt'],
            comment['likeCount'],
            comment['textDisplay']
        ])
    
    next_page_token = response.get('nextPageToken')
    if not next_page_token:
        break
    
    print(f"Đã lấy {len(comments)} comments...")

df = pd.DataFrame(comments, columns=['author', 'published_at', 'updated_at', 'like_count', 'text'])

print(f"\nTổng cộng: {len(df)} comments")
print(df.head(10))

file_exists = os.path.isfile('youtube_comments.csv')

if file_exists:
    existing_df = pd.read_csv('youtube_comments.csv', encoding='utf-8-sig')
    combined_df = pd.concat([existing_df, df], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=['author', 'published_at', 'text'], keep='first')
    combined_df.to_csv('youtube_comments.csv', index=False, encoding='utf-8-sig')
else:
    df.to_csv('youtube_comments.csv', index=False, encoding='utf-8-sig')

print("Đã thêm dữ liệu vào youtube_comments.csv")