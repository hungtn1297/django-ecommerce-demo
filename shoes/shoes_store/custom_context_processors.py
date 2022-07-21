from .models import Customer

def base(request):
    if 'customer_id' in request.session:
        current_customer = Customer.objects.get(id=request.session['customer_id'])
        print(current_customer)
        return {'current_customer': current_customer}
    return {'current_customer': ''}

