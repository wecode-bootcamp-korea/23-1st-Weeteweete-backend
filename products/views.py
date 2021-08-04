import json

from django.http     import JsonResponse
from django.views    import View

from users.models    import *
from orders.models   import *
from products.models import *

class MainPageView(View):
    def get(self, request):
        # 90일 이내에 주문된 Order_Item QuerySet  (Order_status에 대한 정보는 추가하지 않음. 추가 가능)
        # orders = OrderItem.objects.filter(order.ordered_at__lt = timezone.now() - datetime.timedelta(days=90))
        # 90일 이내 주문된 상품의 item id에 대한 수량 합  구하기
        # order_count= orders.values('item_id').annotate(quntity_sum=Sum('quantity'))
        #
        # order_dic = {}
        # for order in order_count:
        #    order[item_id], order[quantity_sum)
        try:
            items = Item.objects.order_by('-order_quantity')[:8]
            results = []
            
            for item in items:
                images = []
                results.append(
                    {
                        "id"             : item.id,
                        "name"           : item.name,
                        "price"          : item.price,
                        "discount"       : item.price - item.discount,
                        "stock"          : item.option,
                        "color"          : item.color,
                        "image"          : [images.append(image.image_url) for image in item.image],
                        "order_quantity" : item.order_quantity
                    }
                )
            return JsonResponse({'results':results}, status=200) 
        except:
            return JsonResponse({'Message':'No Data'}, status=400) 



        

