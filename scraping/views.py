from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from django.template import loader

import requests
from bs4 import BeautifulSoup
import re

# url = "https://www.gumtree.com/for-sale/video-games-consoles"


def index(request):

    if request.method == "POST":
        url = request.POST.get("website")
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        products = []
        print("**** Response ***")
        print(response)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
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
        context = {'products': products}
        print(products)
        return render(request, "index.html", context)
    else:
        return render(request, "index.html", {})
        
        