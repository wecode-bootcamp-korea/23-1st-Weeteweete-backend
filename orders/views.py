import json

from django.http     import JsonResponse
from django.views    import View

from orders.models   import Order, OrderItem
from users.utils     import login

class OrderView(View):
    @login
    def post(self, request, item_id):
        data=json.loads(request.body)

        order=Order.objects.create(
            member_id   = request.user.id,
            status_id   = 1,
            location_id = None
        )

        OrderItem.objects.create(
            item_id              = item_id,
            order_id             = order.id,
            order_item_status_id = 1,
            quantity             = data['quantity']
        )
        return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)

    @login
    def get(self, request):
        order_id    = Order.objects.get(member_id=request.user.id, status_id =1).id
        order_items = OrderItem.objects.filter(order_id=order_id) 
        
        result = [
            {
        "order_number" : order_item.order_id,
        "quantity"     : order_item.quantity,
        "name"         : request.user.name,
        "phone_number" : request.user.phone_number,
        "address"      : request.user.address,
        "information"  : [
            {
            "product_name"     : item.name,
            "product_image"    : item.image_set.get(main=1).image_url,
            "product_price"    : item.price,
            "product_discount" : item.discount   
            }
            for item in [order_item.item for order_item in order_items]
            ]
        }
        for order_item in order_items]
        
        return JsonResponse({'RESULT': result}, status=200)
