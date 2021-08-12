import json

from django.http      import JsonResponse
from django.views     import View
from django.db        import transaction
from django.db.models import Q, F

from products.models  import Item
from orders.models    import Order, OrderItem, Location, Cart, OrderItemStatus, OrderStatus
from users.models     import Member
from users.utils      import login

class OrderView(View):
    @login
    @transaction.atomic
    def post(self, request):
        item_id = request.GET.get("item_id", None)
        data    = json.loads(request.body)      
                
        if Order.objects.filter(member_id = request.user.id, status_id = OrderStatus.Status.WAITING.value).exists():
            Order.objects.filter(member_id = request.user.id, status_id = OrderStatus.Status.WAITING.value).delete()

        order = Order.objects.create(member_id = request.user.id, status_id = OrderStatus.Status.WAITING.value, location_id = None)
        
        OrderItem.objects.bulk_create(
            [OrderItem
            (item_id             = cart.item_id if not item_id else item_id, 
            order_id             = order.id,  
            quantity             = cart.quantity if not item_id else data['quantity'],
            order_item_status_id = OrderItemStatus.ItemStatus.WAITING.value,
            ) for cart in (Cart.objects.filter(member_id = request.user.id) if not item_id else range(1))]
        )
        return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)


    @login
    def get(self, request):
        order_items = OrderItem.objects.filter(order_id=Order.objects.get(member_id=request.user.id, status_id = OrderStatus.Status.WAITING.value).id) 
        
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
            "product_price"    : float(order_item.item.price),
            "product_discount" : float(order_item.item.discount)   
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
            order.status_id   = OrderStatus.Status.COMPLETED.value
            order.save()

            order_items = OrderItem.objects.filter(order_id=data['order_id']) 
            for order_item in order_items:
                order_item.order_item_status_id = OrderItemStatus.ItemStatus.COMPLETED.value
                item                            = Item.objects.get(id=order_item.item_id)
                item.order_quantity             += order_item.quantity
                item.stock                      -= order_item.quantity               
                
                if Cart.objects.filter(Q(member_id=request.user.id) & Q(item_id = order_item.item_id)).exists():
                    Cart.objects.filter(Q(member_id=request.user.id) & Q(item_id = order_item.item_id)).delete()

                order_item.save()
                item.save()

            return JsonResponse({'MESSAGE': "SUCCESS"}, status=201)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


class CartView(View):
    @login
    def post(self, request):
        try:
            data = json.loads(request.body)

            if Cart.objects.filter(Q(item_id = data['item_id']) & Q(member_id=request.user.id)).exists():
                return CartView.patch(self, request)
            
            if data['quantities'] > Item.objects.get(id = data['item_id']).stock:
                return JsonResponse({"MESSAGE":"NO_STOCK"}, status=400)
                
            Cart.objects.create(
                item_id=data['item_id'], 
                member_id = request.user.id, 
                quantity = data['quantities']
            )
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)

    @login
    def get(self, request):

        if not Cart.objects.filter(member_id=request.user.id).exists():
                return JsonResponse({"MESSAGE":"EMPTY_CART"}, status=400)

        results = [
            {
            "cart_id"  : cart.id,
            "item_id"  : cart.item.id,
            "quantity" : cart.quantity,
            "name"     : cart.item.name,
            "image"    : cart.item.image_set.get(main=1).image_url,
            "price"    : float(cart.item.price),
            "discount" : float(cart.item.discount)
            } 
        for cart in Cart.objects.filter(member_id=request.user.id)]

        return JsonResponse({"RESULT" : results}, status=200)

    @login
    def patch(self, request):
        try:
            is_cart = request.GET.get("is_cart", None)
            data    = json.loads(request.body)

            if not is_cart:
                cart = Cart.objects.get(Q(item_id = data['item_id']) & Q(member_id=request.user.id))
                if cart.item.stock < cart.quantity + data['quantities']:
                    return JsonResponse({"MESSAGE":"NO_STOCK"}, status=400)

                cart.quantity = F('quantity') + data['quantities']
                cart.save()
                return JsonResponse({"MESSAGE" : "ADD_CART"}, status=200)

            cart = Cart.objects.get(member_id=request.user.id, item_id=data['item_id'])
            if cart.item.stock < data['quantities']:
                return JsonResponse({"MESSAGE":"NO_STOCK"}, status=400)
            
            cart.quantity = data['quantities']
            cart.save()
            
            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=200)
        
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)


    @login
    def delete(self, request):
        item_id = request.GET.getlist("item_id",None)
        
        for item in item_id:
            Cart.objects.get(member_id=request.user.id, item_id=item).delete()
        return JsonResponse({"MESSAGE" : "NO_CONTENT"}, status=204)