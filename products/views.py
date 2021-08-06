import json

from django.http     import JsonResponse
from django.views    import View

from products.models import Option, Product, Category, Concept, Item

class PageView(View):
     def get(self, request):
        try:
            product_id  = request.GET.get('product_id', None)
            category_id = request.GET.get('category_id', None)
            option_id   = request.GET.get('option_id', None)

            if not product_id and not category_id and not option_id:
                items = Item.objects.order_by('-order_quantity')[:3]
                main= [
                    {
                        'id'             : item.id,
                        'name'           : item.name,
                        'price'          : item.price,
                        'discount'       : item.price - item.discount,
                        'stock'          : item.stock,
                        'image'          : item.image_set.get(main=1).image_url
                    } for item in items]

                return JsonResponse({'RESULTS': main if True else 'EMPTY'}, status=200)

            if not Product.objects.filter(id=product_id).exists() or not Category.objects.filter(id=category_id).exists() or not Option.objects.filter(id=option_id):
                return JsonResponse({'MESSAGE':'NO_MENU'}, status=400)

            concepts = Concept.objects.filter(category_id = category_id)

            menu = [
                {
                        'concept'             : concept.name,
                        'concept_description' : concept.content,
                        'concpet_id'          : concept.id,
                        'information'         : [
                            {
                                'id'       : item.id,
                                'name'     : item.name,
                                'price'    : item.price,
                                'discount' : item.discount,
                                'stock'    : item.stock,
                                'color'    : item.color.name,
                                'image'    : item.image_set.get(main=1).image_url
                            } for item in Item.objects.filter(concept_id=concept.id, option_id=option_id)]
                } for concept in concepts]
                
            return JsonResponse({'RESULTS': menu if True else 'EMPTY'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)