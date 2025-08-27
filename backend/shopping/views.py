from .models import *
from .serializer import *
from rest_framework import status
from django.shortcuts import render
from users.models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from shopping.serializer import SupermarketSerializer
from shopping.utils.sacraping_scripts import scrap_tiendas_exito
from rest_framework.permissions import IsAuthenticated, AllowAny


class SupermarketScrapingView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """ user = request.user
        try:
            profile = user.userprofile
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND) """
        query1 = "bebidas"
        query2 = "frutas-y-verduras"
        new_supermarket = scrap_tiendas_exito(query1)
        if len(new_supermarket) == 0:
            products = ProductVariant.objects.all()
            serializers = ProductVariantSerializer(products, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            products = new_supermarket
        return Response(products, status=status.HTTP_200_OK)