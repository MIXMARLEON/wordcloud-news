from GoogleNews import GoogleNews
import wordcloud
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

"""

This code collecting news from news.google.com and use titles for generate 
word cloud. In this code I collected data about Russia from US region and 
made cloud from conture of Russia in tricolor.

"""


def get_news(search):

    """
    This function returns data frame with columns:
    title, desc, date, datetime, link, img, media, site

    :param str search: String by which you want to search for news.

    :return pd.DataFrame: Pandas data frame.
    """

    gn = GoogleNews(region='US')
    gn.set_lang('en')
    gn.set_encode('utf-8')
    gn.set_period('30d')
    gn.get_news(search)
    search_result = gn.results()
    data = pd.DataFrame(search_result)
    gn.clear()
    return data


russia = get_news("Russia")

#  Collecting titles
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

mask = np.array(Image.open('flag_map_of_russia.png'))  # image for mask
wc = wordcloud.WordCloud(stopwords=stopwords, background_color='white', mask=mask,
                         width=1224, height=612, contour_color=None)

# Generates colors for text using image color
wc.generate(titles)
image_colors = wordcloud.ImageColorGenerator(mask)
wc.recolor(color_func=image_colors)
wc.to_file("result.png")

plt.imshow(wc)
plt.xticks([])
plt.yticks([])
plt.show()

