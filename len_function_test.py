from selenium import webdriver

browser = webdriver.Chrome(executable_path="C:/Users/Kazut/Desktop/chromedriver_win32/chromedriver.exe")
url = 'http://wav.tv/actresses/'

PAGER_NEXT = "a.m-pagination--next.is-last.step"  # Next button
POSTS = "div.m-actress-wrap"  # このdivは名前と画像をまとめたもの
ACTRESS_NAME = ".m-actress--title"  # actresses' names
IMAGE = ".m-actress--thumbnail-img img"  # actresses' images

browser.get(url)
posts = browser.find_elements_by_css_selector(POSTS)  # 女優divのエレメントを探す
print(posts)