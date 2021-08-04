import json

from django.http     import JsonResponse
from django.views    import View

from users.models    import *
from products.models import *
from orders.models   import *

class MenuPageView(View):
     def get(self, request, product_id, category_id, option_id):
        try:
            if not Product.objects.filter(id=product_id).exists() or not Category.filter(id=category_id).exists():
                return JsonResponse({"MESSAGE":"No_Menu"}, status=400)
        
            concepts = Concept.objects.filter(category_id = category_id)
            results = []

            for concept in concepts:
                informations = []
                items = Item.objects.filter(concept_id=concept.id, option_id=option_id)
                for item in items:
                    images = []
                    informations.append(
                        {
                            "id"       : item.id,
                            "name"     : item.name,
                            "price"    : item.price,
                            "discount" : item.price - item.discount,
                            "stock"    : item.option,
                            "color"    : item.color,
                            "image"    : [images.append(image.image_url) for image in item.image]
                        }
                    )
                results.append(
                    {
                        "concept"     : concept.name,
                        "concpet_id"  : concept.id,
                        "information" : informations
                    }
                )
            return JsonResponse({'results':results}, status=200)      
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)

class MainPageView(View):
    def get(self, request):
        bests = Order.objects.filter