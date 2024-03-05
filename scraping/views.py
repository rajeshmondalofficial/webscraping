from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template import loader

import requests
from bs4 import BeautifulSoup
import re
import cloudscraper
import json 
from playwright.sync_api import sync_playwright 

# url = "https://www.gumtree.com/for-sale/video-games-consoles"

# Extract Products
def extractProducts(response):
    products = []
    soup = BeautifulSoup(response, 'html.parser')
            
    product_elements = soup.find_all('article', {'data-q': 'search-result'})
    pagination_links = soup.find_all('a', class_=re.compile("pagination-*"))
    pages = []
    for link in pagination_links:
        pages.append(link["href"])
            
    for product in product_elements:
        product_name = product.find('div', {'data-q':'tile-title'})
        product_price = product.find('div', {'data-q': 'tile-price'})
        product_description = product.find('div', {'data-q': 'tile-description'})
                
        product_dict  ={
            'name': product_name.text.strip(),
            'price': product_price.text.strip(),
            'description': product_description.text.strip(),
        }
        products.append(product_dict)
    return products


def index(request):
    if request.method == "POST":
        url = request.POST.get("website")
        products = []
        with sync_playwright() as p: 
            for browser_type in [p.chromium]: 
                browser = browser_type.launch() 
                page = browser.new_page() 
                page.goto(url) 
                print(page.content())
                products.extend(extractProducts(page.content()))
                browser.close() 


        # scraper = cloudscraper.create_scraper()
        # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        # response = requests.get(url, headers=headers)
        # response.raise_for_status()
        # response = scraper.get(url)
        # print("**** Response ***")
        # print(response.text)
        return render(request, "index.html", {'products': products})
    else:
        return render(request, "index.html", {})
        
        