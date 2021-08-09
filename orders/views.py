import json

from django.http     import JsonResponse
from django.views    import View
from django.db       import transaction

from products.models import Item
from orders.models   import Order, OrderItem, Location
from users.models    import Member
from users.utils     import login

class OrderView(View):
    @login
    @transaction.atomic
    def post(self, request, item_id):
        data = json.loads(request.body)
        
        if Order.objects.filter(member_id = request.user.id, status_id = 1).exists():
            Order.objects.filter(member_id = request.user.id, status_id = 1).delete()

        order = Order.objects.create(member_id = request.user.id, status_id = 1, location_id = None)

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
            "product_name"     : order_item.item.name,
            "product_image"    : order_item.item.image_set.get(main=1).image_url,
            "product_price"    : order_item.item.price,
            "product_discount" : order_item.item.discount   
            }
            ]
        }
        for order_item in order_items]
        
        return JsonResponse({'RESULT': result}, status=200)


class PurchaseView(View):
    @login
    @transaction.atomic
    def post(self, request):
        try:
            data   = json.loads(request.body)
            member = Member.objects.get(id=request.user.id)
            if member.points < data['total_price']:
                return JsonResponse({"MESSAGE":"INSUFFICIENT_POINTS"}, status=400)

            location=Location.objects.create(
                name         = data['name'],
                phone_number = data['phone_number'],
                email        = data.get('email', None),
                address      = data['address'],
                content      = data.get('content', None)
            )
            
            member.points = member.points - data['total_price']
            member.save()            

            order             = Order.objects.get(id=data['order_id'])
            order.location_id = location.id
            order.status_id   = 2
            order.save()

            order_items = OrderItem.objects.filter(order_id=data['order_id']) 
            for order_item in order_items:
                order_item.order_item_status_id = 2
                item                            = Item.objects.get(id=order_item.item_id)
                item.order_quantity             += order_item.quantity
                item.stock                      -= order_item.quantity               
                order_item.save()
                item.save()

            return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)