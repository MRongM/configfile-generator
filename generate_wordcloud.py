import os
from wordcloud import WordCloud

FILE_DIR = './public/files'
OUTPUT_IMAGE = './public/banner.png'

if not os.path.exists(FILE_DIR):
    exit(1)

filenames = os.listdir(FILE_DIR)
words = ' '.join(filenames)

wordcloud = WordCloud(
    width=600,
    height=200,
    background_color='white',
    colormap='tab10',
    font_path=None,
    prefer_horizontal=0.9
).generate(words)

wordcloud.to_file(OUTPUT_IMAGE)
print(f"word cloud saved===>> {OUTPUT_IMAGE}")

