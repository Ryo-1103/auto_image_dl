# ライブラリのインポート
import os
import time
from urllib import error, request

import tweepy

# 画像の保存先
IMG_DIR = "image/"

# 環境変数
CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN_KEY = os.environ.get("ACCESS_TOKEN_KEY")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS?TOKEN_SECRET")

# キーワード
search_key = "アウラ"

# 検索条件
# 読み込むページ数
search_page = 50
# 1ページあたりのツイート数
search_tweet = 100


class ImageDownload(object):
    # 初期設定
    def __init__(self):
        super(ImageDownload, self).__init__()
        self.set_api()

    def run(self):
        self.max_id = None
        for pages in range(search_page):
            url_list = self.search(search_key, search_tweet)
            for urls in url_list:
                print(f"{urls}をダウンロードします")
                self.download(urls)
                time.sleep(0.2)

    def set_api(self):
        auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def search(self, search_key, rpp):
        url_list = []

        try:
            if self.max_id:
                responce_search = self.api.search(
                    q=search_key, lang="ja", rpp=rpp, max_id=self.max_id
                )
            else:
                responce_search = self.api.search(q=search_key, lang="ja", rpp=rpp)

            for result in responce_search:
                if "media" not in result.entities:
                    continue
                for media in result.entities["media"]:
                    url = media["media_url_https"]
                    if url not in url_list:
                        url_list.append(url)

            self.max_id = result.id
            return url_list
        except Exception as e:
            self.error_catch(e)

    def download(self, url):
        url_orig = "%s:orig" % url
        path = IMG_DIR + url.split("/")[-1]

        try:
            responce = request.urlopen(url=url_orig)
            with open(path, "wb") as f:
                f.write(responce.read())
        except Exception as e:
            self.error_catch(e)

    def error_catch(self, error):
        print(f"予期せぬエラーを検知しました。詳細は{error}をご確認ください")


def main():
    try:
        downloader = ImageDownload()
        downloader.run()

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
