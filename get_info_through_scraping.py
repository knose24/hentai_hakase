from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas

# General Setting
chrome_options = Options()
chrome_options.add_argument("--lang=ja")
browser = webdriver.Chrome(executable_path='C:/Users/Kazut/Desktop/chromedriver_win32/chromedriver.exe',
                           chrome_options=chrome_options)
df = pandas.read_csv('/Users/Kazut/PycharmProjects/test2/HH/default.csv', index_col=0)  # CSVファイルを読み込む
url = 'http://wav.tv/actresses/'  # DMMのウェブサイトのURL

# setting of CSS selector
PAGER_NEXT = "a.m-pagination--next.is-last.step"  # Next button
POSTS = "div.m-actress-wrap"  # このdivは名前と画像をまとめたもの
ACTRESS_NAME = ".m-actress--title"  # actresses' names
IMAGE = ".m-actress--thumbnail-img img"  # actresses' images

# performing
browser.get(url)
while True:
    if len(browser.find_elements_by_css_selector(PAGER_NEXT)) > 0:  # if the next button exists
        print("starting to get posts...")
        posts = browser.find_elements_by_css_selector(POSTS)  # 女優divのエレメントを探す
        print(len(posts))  # 女優の数をプリント
        for post in posts:  # 各女優divに以下の動作を行う
            try:
                name = post.find_element_by_css_selector(ACTRESS_NAME).text
                print(name)  # print the names of the actresses
                thumnailURL = post.find_element_by_css_selector(IMAGE).get_attribute("src")
                print(thumnailURL)  # print the images of the actresses
                se = pandas.Series([name, thumnailURL], ["name", "image"])  # input the names and images as series
                df = df.append(se, ignore_index=True)
            except Exception as e:
                print(e)  # print the error message
        btn = browser.find_element_by_css_selector(PAGER_NEXT).get_attribute("href")
        print("next url:{}".format(btn))
        browser.get(btn)
        print('Moving to next page.....')
    else:
        print("no page exist anymore")
        break
print("Finished Scraping. Writing CSV...")
df.to_csv("output.csv")  # 新しくCSVファイルを作る

print("DONE")
