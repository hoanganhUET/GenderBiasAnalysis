import pandas as pd

df = pd.read_csv('youtube_comments.csv')

print(f"Tổng số dòng: {len(df)}")
print(f"Số cột: {len(df.columns)}")
print(f"Tên các cột: {list(df.columns)}")
print("-" * 50)

duplicate_rows = df[df.duplicated()]
print(f"Số dòng duplicate (toàn bộ): {len(duplicate_rows)}")

duplicate_text = df[df.duplicated(subset=['text'], keep=False)]
print(f"Số dòng có text trùng lặp: {len(duplicate_text)}")

duplicate_author_text = df[df.duplicated(subset=['author', 'text'], keep=False)]
print(f"Số dòng có author + text trùng lặp: {len(duplicate_author_text)}")

print("-" * 50)

if len(duplicate_rows) > 0:
    print("\n=== Các dòng duplicate (toàn bộ) ===")
    print(duplicate_rows)

if len(duplicate_text) > 0:
    print("\n=== Các comment có text trùng lặp ===")
    duplicate_text_sorted = duplicate_text.sort_values('text')
    for idx, row in duplicate_text_sorted.iterrows():
        print(f"\nAuthor: {row['author']}")
        print(f"Text: {row['text'][:100]}...")
        print(f"Published: {row['published_at']}")

print("\n" + "=" * 50)
print("=== Thống kê số lần xuất hiện của mỗi text ===")
text_counts = df['text'].value_counts()
duplicated_texts = text_counts[text_counts > 1]
if len(duplicated_texts) > 0:
    print(f"\nCó {len(duplicated_texts)} text xuất hiện nhiều hơn 1 lần:")
    for text, count in duplicated_texts.items():
        print(f"\n- Xuất hiện {count} lần:")
        print(f"  Text: {text[:100]}...")
else:
    print("Không có text nào bị trùng lặp!")

df_no_duplicates = df.drop_duplicates()
df_no_duplicates.to_csv('youtube_comments.csv', index=False)