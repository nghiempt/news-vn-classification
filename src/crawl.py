from bs4 import BeautifulSoup
from urllib.request import urlopen
import time
import ssl
import pandas as pd
import re

pattern = r"\d{17}\.chn$"
chrome_url = "https://kenh14.vn"

def exportFileTXT(content):
    with open("path.txt", "a", encoding="utf-8") as file:
        file.write(content + "\n")
    return True


class Crawl:

    @staticmethod
    def load_html_content(url):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        html = urlopen(url, context=ctx).read()
        soup = BeautifulSoup(html, "html.parser")
        return soup

    @staticmethod
    def filter_content(soup, index):
        tags = soup.find_all('a')
        new_data = []
        new_columns = ['id', 'url']
        for tag in tags:
            try:
                link = tag['href']
                if link.endswith(".chn") and re.search(pattern, link):
                    last_32_characters = link[-21:-4]
                    print(last_32_characters)
                    print(link)
                    new_row = [last_32_characters, link]
                    new_data.append(new_row)
            except KeyError as e:
                print(str(e))
                continue
        new_df = pd.DataFrame(new_data, columns=new_columns)
        return new_df

    @staticmethod
    def generate_result():
        df = pd.read_csv("./kenh14Crawl/urls.csv")
        
        for index, row in df.iterrows():
            if index > 400:
                print("Index: " + str(index))
                if row["url"].startswith("https://kenh14.vn"):
                    soup = Crawl.load_html_content(row['url'])
                else:
                    soup = Crawl.load_html_content(chrome_url + row['url'])
                new_df = Crawl.filter_content(soup, index=0)
                new = pd.read_csv("./kenh14Crawl/urls.csv")
                appended_df = pd.concat([new, new_df], ignore_index=True)
                appended_df.to_csv("./kenh14Crawl/urls.csv", index=False)
            if index > 800:
                break

if __name__ == "__main__":
    validator = Crawl()
    validator.generate_result()
    print("Done")