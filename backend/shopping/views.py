from .models import *
from .serializer import *
from rest_framework import status
from django.shortcuts import render
from users.models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from shopping.utils.sacraping_scripts import scrap_tiendas_exito
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.views.generic import TemplateView


def category_map(category):
    categories_map = {
        "bebidas": ["Jugos", "Bebidas de cereal", "Agua y té", "Hidratantes y energizantes", "Gaseosas y sodas"],
        "frutas-y-verduras": ["Frutas y verduras"],
        "carnes": ["Pollo, carne y pescado"],
        "vinos-y-licores": ["Ginebra", "Brandy", "Coctelería", "Vodka", "Tequila", "Ron", "Vinos", "Whisky", "Cerveza", "Aguardiente"],
        "lacteos-huevos-y-refrigerados": ["Lácteos, huevos y refrigerados"]
    }
    subcategories = categories_map.get(category, [])
    return subcategories


class SupermarketScrapingView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        query = request.GET.get("category")
        subcategories = category_map(query)
        check_products = Product.objects.filter(category__name__in=subcategories)
        
        product_variant = []
        
        for item in check_products:
            variants = ProductVariant.objects.filter(product=item.id)
            for variant in variants:
                product_variant.append(variant)
            
        
            
        
        if check_products:
            serializers = ProductVariantSerializer(product_variant, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            new_supermarket = scrap_tiendas_exito(query)
            if len(new_supermarket) == 0:
                serializers = ProductVariantSerializer(product_variant, many=True)
                return Response(serializers.data, status=status.HTTP_200_OK)
            else:
                products = new_supermarket
                return Response(products, status=status.HTTP_200_OK)
    
    
class SupermarketSelectView(TemplateView):
    template_name = "supermarket_select.html"
    
    