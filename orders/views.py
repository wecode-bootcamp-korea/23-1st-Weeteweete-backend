 for order_item in order_items:
            informations = []
            items        = [order_item.item for order_item in order_items]

             for item in items:
                informations.append(
                    {
                    "product_name"     : item.name,
                    "product_image"    : item.image_set.get(main=1).image_url,
                    "product_price"    : item.price,
                    "product_discount" : item.discount
                    }
                )
            result.append(
                {
                "order_number" : order_item.order_id,
                "quantity"     : order_item.quantity,
                "information"  : informations,
                "name"         : request.user.name,
                "phone_number" : request.user.phone_number,
                "address"      : request.user.address
                }
            )
        return JsonResponse({'RESULT': result}, status=200)


result  = [ 
    {
    "order_number" : order_item.order_id,
    "quantity"     : order_item.quantity,    
    "name"         : request.user.name,
    "phone_number" : request.user.phone_number,
    "address"      : request.user.address,
    "information"  : [{
                    "product_name"     : item.name,
                    "product_image"    : item.image_set.get(main=1).image_url,
                    "product_price"    : item.price,
                    "product_discount" : item.discount
    }for item in order_item.item for order_item in order_items]  
    }for order_item in order_items
]