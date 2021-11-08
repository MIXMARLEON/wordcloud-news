from GoogleNews import GoogleNews
import wordcloud
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image


def get_news(search, lang='en', region='US', period_days=30):
    # Returns pandas dataframe with data

    gn = GoogleNews(region=region)
    gn.set_lang(lang)
    gn.set_encode('utf-8')
    gn.set_period(str(period_days) + 'd')  # 30d
    gn.get_news(search)
    search_result = gn.results()
    data = pd.DataFrame(search_result)
    gn.clear()
    return data


russia = get_news("Russia")

titles = ''
for row in russia['title']:
    titles += str(row) + "; "

stopwords = set(wordcloud.STOPWORDS)

#  Excludes the given words from the result
custom_stopwords = ["CNN", "BBC", "New", "York", "Times", "Russia", "Russian",
                    "Wall", "Street", "Journal", "Reuters", "U", "S", "Say",
                    "Says", "Bloomberg", "report", "News", "Radio", "Free", "TASS"]

for string in custom_stopwords:
    stopwords.add(string)

mask = np.array(Image.open('flag_map_of_russia.png'))
wc = wordcloud.WordCloud(stopwords=stopwords, background_color='white', mask=mask,
                         width=1224, height=612, contour_color='black')
wc.generate(titles)
image_colors = wordcloud.ImageColorGenerator(mask)
wc.recolor(color_func=image_colors)

plt.imshow(wc)
plt.xticks([])
plt.yticks([])
plt.show()

