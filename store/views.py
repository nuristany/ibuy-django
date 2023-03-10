from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from carts.models import CartItem
from carts.views import _cart_id
from .models import Product, Catagory
from django.core.paginator import EmptyPage,  PageNotAnInteger, Paginator



# Create your views here.
    
def store(request, catagory_slug=None):
    catagories = None
    products = None
    
    if catagory_slug != None:
        catagories = get_object_or_404(Catagory, slug=catagory_slug)
        products = Product.objects.filter(catagory=catagories, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        
        products = Product.objects.all().filter(is_available = True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = Product.objects.all().count()
    context = {
        'products': paged_products,
        'product_count':product_count , 
        
    }
    
    return render(request, 'store/store.html', context)

def product_detail(request, catagory_slug, product_slug ):
    try:
        single_product = Product.objects.get(catagory__slug=catagory_slug,slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        # return HttpResponse(in_cart)
        # exit()
        
    except Exception as e:
        
        raise e
    
    context = {
        'single_product':single_product,
        'in_cart':in_cart
    }

    return render(request, 'store/product_detail.html', context )



def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        products = Product.objects.filter(is_available = False)
        
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(product_name__icontains = keyword) | Q(description__icontains = keyword) | Q(stock__icontains = keyword))
            product_count = products.count()
    context = {
        'products':products,
        'product_count':product_count
        
        
            
    }    
            
    return render(request, 'store/store.html',context )
    
    