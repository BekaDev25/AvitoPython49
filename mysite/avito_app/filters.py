from django_filters import FilterSet
from .models import Products

class ProductsFilter(FilterSet):
    class Meta:
        model = Products
        fields ={
            'subcategory': ['exact'],
            'product_price': ['gt', 'lt'],
            'article_number': ['exact'],
        }
