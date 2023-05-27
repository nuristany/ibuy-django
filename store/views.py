from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from orders.admin import OrderProductInline
from orders.models import OrderProduct
from .forms import ReviewForm
from.models import ReviewRating, ProductGallery
from carts.models import CartItem
from carts.views import _cart_id
from .models import Product, Catagory
from django.core.paginator import Paginator



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
    if request.user.is_authenticated:
        
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None
        
       # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)
    product_gallery = ProductGallery.objects.filter(product_id=single_product.id)

   

    
    context = {
        'single_product':single_product,
        'in_cart':in_cart,
        'orderproduct':orderproduct,
        'reviews': reviews,
        'product_gallery': product_gallery
       
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


def submitReview(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
      
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
    