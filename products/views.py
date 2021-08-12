import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from products.models  import Option, Product, Category, Concept, Item, Review
from users.utils      import login


class PageView(View):
     def get(self, request):
        try:
            product_id  = request.GET.get('product_id', None)
            category_id = request.GET.get('category_id', None)
            option_id   = request.GET.get('option_id', None)
            main        = request.GET.get('main', None)

            if not main and (not Product.objects.filter(id=product_id).exists() or not Category.objects.filter(id=category_id).exists() or not Option.objects.filter(id=option_id)):
                return JsonResponse({'MESSAGE':'NO_MENU'}, status=400)

            concepts = Concept.objects.filter(item__category_id = category_id) if not main else Item.objects.order_by('-order_quantity')[:8] 
            
            results = [
                {
                        'concept'             : concept.name if not main else None,
                        'concept_description' : concept.content if not main else None,
                        'concept_id'          : concept.id if not main else None,
                        'information'         : [
                            {
                                'id'       : item.id,
                                'name'     : item.name,
                                'price'    : item.price,
                                'discount' : item.discount,
                                'stock'    : item.stock,
                                'color'    : item.color.name if not item.color is None else None,
                                'image'    : item.image_set.get(main=1).image_url
                            } for item in (Item.objects.filter(Q(concept_id=concept.id)&Q(option_id=option_id)) if not main else [concept])]
                } for concept in concepts]

            return JsonResponse({'RESULTS': results}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class DetailPageView(View):
    def get(self, request, item_id):
        if not Item.objects.filter(id=item_id).exists():
            return JsonResponse({"MESSAGE":"NO_MENU"}, status=400)
        
        item   = Item.objects.get(id=item_id)
        
        result = {
            "name"           : item.name,
            "price"          : item.price,
            "discount"       : item.discount,
            "discount_price" : item.price-item.discount,
            "image"          : [image.image_url for image in item.image_set.all()]
        }

        return JsonResponse({'RESULT':result}, status=200)

class ReviewView(View):
    @login
    def post(self, request, item_id):
        try:
            content = request.POST.get("content", None)
            grade   = request.POST.get("grade", None)
            image   = request.FILES.get('image', None)
            
            if not Item.objects.filter(id=item_id).exists():
                return JsonResponse({"MESSAGE":"NO_ITEM"}, status=400)
            
            Review.objects.create(
                member_id = request.user.id,
                item_id   = item_id,
                image_url = image,
                content   = content,
                grade     = grade
            )
            return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)