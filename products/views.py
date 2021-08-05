import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product, Category, Concept, Item

class MenuPageView(View):
     def get(self, request, product_id, category_id, option_id):
        try:
            if not Product.objects.filter(id=product_id).exists() or not Category.objects.filter(id=category_id).exists():
                return JsonResponse({"MESSAGE":"NO_MENU"}, status=400)
            
            concepts = Concept.objects.filter(category_id = category_id)
            results = []
            for concept in concepts:
                informations = []
                items = Item.objects.filter(concept_id=concept.id, option_id=option_id)
                for item in items:
                    informations.append(
                        {
                            "id"       : item.id,
                            "name"     : item.name,
                            "price"    : item.price,
                            "discount" : item.discount,
                            "stock"    : item.stock,
                            "color"    : item.color.name,
                            "image"    : item.image_set.get(main=1).image_url
                        }
                    )
                results.append(
                    {
                        "concept"             : concept.name,
                        "concept_description" : concept.content,
                        "concpet_id"          : concept.id,
                        "information"         : informations
                    }
                )
            return JsonResponse({'results':results}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': "KEY_ERROR"}, status=400)
