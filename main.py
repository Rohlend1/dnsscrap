from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import json
from selenium_stealth import stealth
import itertools


yan_drive = ""

options = webdriver.ChromeOptions()
options.add_argument(f"user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 RuxitSynthetic/1.0 v3573683183 t3362054828373752722 athfa3c3975 altpub cvcv=2 smf=0")
options.add_argument("--disable-blink-features=AutomatuonControlled")
# options.add_argument("--headless")

driver = webdriver.Chrome(yan_drive,options=options)
stealth(driver,
        languages=["en-US","en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.get(url="https://www.dns-shop.ru/catalog/17a8932c16404e77/personalnye-kompyutery/?f[lrp]=81r7")
time.sleep(10)
with open("index.html", "w", encoding="utf-8") as file:
    file.write(driver.page_source)


def get_data(url):

     try:
        with open("index.html", "r", encoding="utf-8") as file:
            src = file.read()
        soup = BeautifulSoup(src, "lxml")
        maxpage = soup.find_all(class_="pagination-widget__page")


        for page in range(1,len(maxpage)-3):
            driver.get(url=f"https://www.dns-shop.ru/catalog/17a8932c16404e77/personalnye-kompyutery/?f[lrp]=81r7&p={page}")
            time.sleep(10)
            src = driver.page_source
            soup = BeautifulSoup(src,"lxml")
            catalogproducts = soup.find_all(class_="catalog-products view-simple")

            with open("final.json", "a", encoding="utf-8") as file:
                for i in catalogproducts:

                    for j in i:
                        try:
                            if "от" not in (j.find(class_="product-buy__price-wrap product-buy__price-wrap_interactive").text.split("₽"))[1]:

                                d = {
                                    "Name" : j.find(class_="catalog-product__name ui-link ui-link_black").text,
                                    "Old_price": ''.join(itertools.filterfalse(str.isalpha, (((j.find(class_="product-buy__price-wrap product-buy__price-wrap_interactive").text.split("₽"))[1]).split("или")[0]))).strip()+"₽",
                                    "New_price":((j.find(class_="product-buy__price-wrap product-buy__price-wrap_interactive").text.split("₽"))[0].strip(" ")+"₽").replace(" ",".")
                                    }
                            else:
                                d = {
                                    "Name": j.find(class_="catalog-product__name ui-link ui-link_black").text,
                                    "Price": ''.join(itertools.filterfalse(str.isalpha, (((j.find(class_="product-buy__price-wrap product-buy__price-wrap_interactive").text.split("₽"))[0]).split("или")[0]))).strip()+"₽"
                                }

                            json.dump(d,file,indent=4,ensure_ascii=False)
                        except:
                            pass
     except Exception as ex:
        print(ex)
     finally:
        driver.close()
        driver.quit

#subcategory__content





def main():
    get_data(111)




if __name__ == "__main__":
    main()



