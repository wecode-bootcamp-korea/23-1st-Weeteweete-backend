import json

from django.http     import JsonResponse
from django.views    import View

from users.models    import *
from orders.models   import *
from products.models import *

class CartView(View):
    def post(self, request, item_id):
        data = json.loads(request.body)
        try:
            cart = Cart.objects.get(item_id = item_id, member_id = data['member_id'])
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                member_id = data['member_id'],
                item_id = item_id,
                quantity = 1
            )
            cart.save()
        
class CartPageView(View):
    def get(self, request):
        data = json.loads(request.body)
        member = request.user

        carts = Cart.objects.filter(member = member)
        results = []

        for cart in carts:
            results.append({
                "item_id"    : cart.item.id,
                "item_image" : cart.item.image.image_url[0],
                "price"      : cart.item.price,
                "discount"   : cart.item.discount,
                "item_name"  : cart.item.name,
                "quantity"   : cart.quantity
            })
    def patch(self, request):
        try:
        
            return JsonResponse({"MESSAGE":"SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"MESSAGE":"KEY_ERROR"}, status=400)
