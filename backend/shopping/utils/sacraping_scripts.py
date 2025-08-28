import json
import requests, re
from ..serializer import *
from bs4 import BeautifulSoup
from unidecode import unidecode
from django.utils import timezone 
from shopping.utils.scraping_data import *
from ..models import Supermarket, Product, ProductVariant, Brand, Category


def scrap_tiendas_exito(query):
    products = get_products_by_graphql(query)
    products_created = []
    """ Create Supermarket """
    serializer_supermarket = SupermarketSerializer(data={"name": "Exito", "url": "https://www.exito.com/"})
    if serializer_supermarket.is_valid():
            serializer_supermarket.save()
    for items in products:
        """ Create Brands """
        serializer_brand = BrandSerializer(data={"name": items['brand']})
        if serializer_brand.is_valid():
            serializer_brand.save()
        """ Create Categories """
        get_category = items['category'].split('/')
        for cat in get_category:
            if cat != '':
                serializer_category = CategorySerializer(data={"name": cat})
                if serializer_category.is_valid():
                    serializer_category.save()
        """ Create Products """
        serializer_product = ProductSerializer(data={"name": items['name'], "category": serializer_category.data, "category_id": serializer_category.data['id'], })
        if serializer_product.is_valid():
            serializer_product.save()
        """ Create Product Variants """
        serializer_product_variant = ProductVariantSerializer(
            data={
                "supermarket": serializer_supermarket.data,
                "supermarket_id": serializer_supermarket.data['id'],
                "brand": serializer_brand.data,
                "brand_id": serializer_brand.data['id'],
                "product": serializer_product.data,
                "product_id": serializer_product.data.get("id"),
                "price": items['price'],
            }
        )
        if serializer_product_variant.is_valid():
            serializer_product_variant.save()
        products_created.append(serializer_product_variant.data)
    return products_created


def interface(category):
    if category == "carnes":
        selectedFacets =  [
            {"key":"productClusterIds","value":"30507"},
            {"key":"channel","value":"{\"salesChannel\":\"1\",\"regionId\":\"\"}"},
            {"key":"locale","value":"es-CO"}
        ]
    if category == "bebidas" or category == "frutas-y-verduras":
        selectedFacets =  [
            {"key":"category-1","value":"mercado"},
            {"key":"category-2","value":category},
            {"key":"channel","value":"{\"salesChannel\":\"1\",\"regionId\":\"\"}"},
            {"key":"locale","value":"es-CO"}
        ]
    if  category == "vinos-y-licores":
        selectedFacets =  [
            {"key":"category-1","value":category},
            {"key":"channel","value":"{\"salesChannel\":\"1\",\"regionId\":\"\"}"},
            {"key":"locale","value":"es-CO"}
        ]
    return selectedFacets 


def get_products_by_graphql(category):
    get_category = interface(category)
    after = ""
    term = ""
    total = ""
    if category == "bebidas":
        term = category
    all_products  = []
    while True:
        variables = {
            "first": 16,
            "after": after,
            "sort": "score_desc",
            "term": term,
            "selectedFacets": get_category
        }
        payload = {"operationName": "SearchQuery", "variables": variables, "query": QUERY}
        res = requests.post(GRAPHQL_URL, json=payload, headers=HEADERS)
        res.raise_for_status()
        data = res.json().get("data", {}).get("search", {})
        products = data.get("products") or []
        for item in products["edges"]:
            if category == "bebidas":
                category_product = item.get("node")["breadcrumbList"]["itemListElement"][0]["name"]
            elif category == "frutas-y-verduras"  or category =="carnes" or category == "vinos-y-licores":
                category_product = item.get("node")["breadcrumbList"]["itemListElement"][1]["name"]     
            product = {
                "id": item.get("node")["id"],
                "name": item.get("node")["items"][0]["complementName"],
                "brand": item.get("node")['brand']["brandName"],
                "category": category_product,
                "price": item.get("node")['items'][0]['sellers'][0]['commertialOffer']['Price'],
                "image": item.get("node")['items'][0]['images'][0]['imageUrl'],
            }
            all_products.append(product)
        if not products:
            break
        after = str(len(all_products))
        total = products["pageInfo"]["totalCount"]
        if total > 200:
            total = 200
        if len(all_products) >= total:
            break
    return all_products