import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Product, Category, Concept, Item

class MenuPageView(View):
     def get(self, request):
        try:
            product_id  = request.GET.get('product_id', None)
            category_id = request.GET.get('category_id', None)
            option_id   = request.GET.get('option_id', None)

            if not Product.objects.filter(id=product_id).exists() or not Category.objects.filter(id=category_id).exists():
                return JsonResponse({"MESSAGE":"NO_MENU"}, status=400)
            
            concepts = Concept.objects.filter(category_id = category_id)
            results = [
                {
                        "concept"             : concept.name,
                        "concept_description" : concept.content,
                        "concpet_id"          : concept.id,
                        "information"         : [
                            {
                                "id"       : item.id,
                                "name"     : item.name,
                                "price"    : item.price,
                                "discount" : item.discount,
                                "stock"    : item.stock,
                                "color"    : item.color.name,
                                "image"    : item.image_set.get(main=1).image_url
                            } for item in Item.objects.filter(concept_id=concept.id, option_id=option_id)]
                } for concept in concepts]

            return JsonResponse({'RESULTS':results}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':"KEY_ERROR"}, status=400)


class MainPageView(View):
    def get(self, request):
        try:
            items = Item.objects.order_by('-order_quantity')[:3]

            results = [
                {
                    "id"             : item.id,
                    "name"           : item.name,
                    "price"          : item.price,
                    "discount"       : item.price - item.discount,
                    "stock"          : item.stock,
                    "image"          : item.image_set.get(main=1).image_url
                } for item in items]

            return JsonResponse({'RESULTS':results}, status=200)
        except:
            return JsonResponse({'Message':'NOT_ENOUGH_DATA'}, status=400)
