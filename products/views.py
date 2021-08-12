import socket

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from users.utils      import login
from products.models  import Option, Product, Category, Concept, Item, Review
from orders.models    import Order


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
                                'price'    : float(item.price),
                                'discount' : float(item.discount),
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
        grade = request.GET.get("grade", None)
        
        if not Item.objects.filter(id=item_id).exists():
            return JsonResponse({"MESSAGE":"NO_MENU"}, status=400)
        
        item = Item.objects.get(id=item_id)
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        IP = s.getsockname()[0]

        result = {
            "name"           : item.name,
            "price"          : float(item.price),
            "discount"       : float(item.discount),
            "discount_price" : float(item.price-item.discount),
            "stock"          : item.stock,
            "image"          : [image.image_url for image in item.image_set.all()],
            "review"         : [
                {
                    "name"      : review.member.name, 
                    "image"     : "http://"+IP+":8000/media/"+review.image_url.name,
                    "review_id" : review.id,
                    "content"   : review.content,
                    "grade"     : review.grade,
                    "create_at" : review.create_at
                }
            for review in Review.objects.filter(item_id=item_id).order_by("-grade" if grade else "-create_at")]
        }
        return JsonResponse({'RESULT':result}, status=200)

    @login
    def post(self, request, item_id):
        if not Order.objects.filter(member = request.user, orderitem__item_id = item_id, status_id=2).exists():
            return JsonResponse({"MESSAGE": "UNATHORIZED"}, status=400)
            
        if Review.objects.filter(member = request.user, item_id = item_id).exists():
            return JsonResponse({"MESSAGE": "EXIST"}, status=400)
        
        return JsonResponse({'MESSAGE': "SUCCESS"}, status=200)

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