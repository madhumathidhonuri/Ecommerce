from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from Rogue.models import Order,TShirts,Shirts,Jeans,Jackets,Formals,Cargos,Hoodies,Trousers,Watches,Footwear,Glasses,Cart
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
PRODUCT_MODELS = {
    'tshirt': 'TShirts',
    'shirt': 'Shirts',
    'jeans': 'Jeans',
    'jacket': 'Jackets',
    'formal': 'Formals',
    'cargo': 'Cargos',
    'hoodie': 'Hoodies',
    'trouser': 'Trousers',
    'watch': 'Watches',
    'footwear': 'Footwear',
    'glass': 'Glasses'
}

@login_required
def add_to_cart(request, product_id, product_type):
    product_type = product_type.lower()  # Ensure product type is lowercase
    print(f"Product Type: {product_type}, Product ID: {product_id}")  # Debugging

    model_name = PRODUCT_MODELS.get(product_type)
    if model_name is None:
        print("Invalid product type")  # Debugging
        messages.error(request, 'Invalid product type')
        return redirect('home')

    try:
        ProductModel = apps.get_model('Rogue', model_name)
        product = get_object_or_404(ProductModel, id=product_id)
    except Exception as e:
        print(f"Error fetching product: {e}")  # Debugging
        messages.error(request, 'Error fetching product')
        return redirect('home')

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product_id=product.id,
        product_type=product_type,
    )

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    print(f"Added to cart: {product.brandname}")  # Debugging
    messages.success(request, f'{product.brandname} added to cart')
    return redirect('cart')

def website(request):
    return render(request,"website.html")
def register(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            if User.objects.filter(username=username).exists():
                messages.error(request,'This username is already taken.Please choose a different one')
                return redirect('register')
            User.objects.create_user(username=username,email=email,password=password)
            messages.success(request,'Registration Successful! Please Login')
            return redirect('login')
    else:
        form=RegisterForm()          
    return render(request,'register.html',{'form':form})
def user_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('website')
        else:
            messages.error(request,'Invalid username or password')
            return render(request,'login.html')
    return render(request,'login.html')
def account(request):
    return render(request,'account.html')
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total=0
    for item in cart_items:
        model_name = PRODUCT_MODELS.get(item.product_type.lower())
        if model_name:
            ProductModel = apps.get_model('Rogue', model_name)
            product = ProductModel.objects.get(id=item.product_id)
            item.product = product
            item.total_price = product.price * item.quantity
            total+=item.total_price

    return render(request, 'cart.html', {'cart_items': cart_items})

def contact(request):
    return render(request,'contact.html')

def home(request):
    return render(request,'website.html')

def navbar(request):
    return render(request,'navbar.html')

def all_tshirts(request):
    tshirts=TShirts.objects.all()
    for tshirt in tshirts:
        print(tshirt.image.url) 
    return render(request,'tshirts.html',{'tshirts':tshirts})

def all_shirts(request):
    shirts=Shirts.objects.all()
    return render(request,'shirts.html',{'shirts':shirts})

def all_jeans(request):
    jeans=Jeans.objects.all()
    return render(request,'jeans.html',{'jeans':jeans})

def all_jackets(request):
    jackets=Jackets.objects.all()
    return render(request,'jackets.html',{'jackets':jackets})

def all_formals(request):
    formals=Formals.objects.all()
    return render(request,'formals.html',{'formals':formals})

def all_cargos(request):
    cargos=Cargos.objects.all()
    return render(request,'cargos.html',{'cargos':cargos})

def all_hoodies(request):
    hoodies=Hoodies.objects.all()
    return render(request,'hoodies.html',{'hoodies':hoodies})

def all_trousers(request):
    trousers=Trousers.objects.all()
    return render(request,'trousers.html',{'trousers':trousers})

def all_watches(request):
    watches=Watches.objects.all()
    return render(request,'watches.html',{'watches':watches})

def all_footwear(request):
    footwear=Footwear.objects.all()
    return render(request,'footwear.html',{'footwear':footwear})

def all_glasses(request):
    glasses=Glasses.objects.all()
    return render(request,'glasses.html',{'glasses':glasses})

def addtocart(request):
    return render(request,'addtocart.html')

def profile(request):
    return render(request,'profile.html')

def logout_view(request):
    logout(request)
    return redirect('website')

def search_results(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        tshirts = list(TShirts.objects.filter(brandname__icontains=query))
        shirts = list(Shirts.objects.filter(brandname__icontains=query))
        jeans = list(Jeans.objects.filter(brandname__icontains=query))
        formals = list(Formals.objects.filter(brandname__icontains=query))
        jackets = list(Jackets.objects.filter(brandname__icontains=query))
        hoodies = list(Hoodies.objects.filter(brandname__icontains=query))
        cargos = list(Cargos.objects.filter(brandname__icontains=query))
        trousers = list(Trousers.objects.filter(brandname__icontains=query))
        footwear = list(Footwear.objects.filter(brandname__icontains=query))
        watches = list(Watches.objects.filter(brandname__icontains=query))
        glasses = list(Glasses.objects.filter(brandname__icontains=query))

        for product in tshirts:
            results.append({'product': product, 'product_type': 'tshirts'})
        for product in shirts:
            results.append({'product': product, 'product_type': 'shirts'})
        for product in jeans:
            results.append({'product': product, 'product_type': 'jeans'})
        for product in formals:
            results.append({'product': product, 'product_type': 'formals'})
        for product in jackets:
            results.append({'product': product, 'product_type': 'jackets'})
        for product in hoodies:
            results.append({'product': product, 'product_type': 'hoodies'})
        for product in cargos:
            results.append({'product': product, 'product_type': 'cargos'})
        for product in trousers:
            results.append({'product': product, 'product_type': 'trousers'})
        for product in footwear:
            results.append({'product': product, 'product_type': 'footwear'})
        for product in watches:
            results.append({'product': product, 'product_type': 'watches'})
        for product in glasses:
            results.append({'product': product, 'product_type': 'glasses'})

    return render(request, 'search_results.html', {'results': results, 'query': query})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('cart')

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        model_name = PRODUCT_MODELS.get(item.product_type.lower())
        if model_name:
            ProductModel = apps.get_model('Rogue', model_name)
            product = ProductModel.objects.get(id=item.product_id)
            item.product = product
            item.total_price = product.price * item.quantity
            total += item.total_price

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    for item in cart_items:
        model_name = PRODUCT_MODELS.get(item.product_type.lower())
        if model_name:
            ProductModel = apps.get_model('Rogue', model_name)
            product = ProductModel.objects.get(id=item.product_id)
            total_price = product.price * item.quantity

            order = Order.objects.create(
                user=request.user,
                product_type=ContentType.objects.get_for_model(ProductModel),
                product_id=product.id,
                quantity=item.quantity,
                total_price=total_price
            )
            item.delete()

    messages.success(request, "Your order has been placed!")
    return redirect('order_confirmation')


@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')

def product_detail(request, product_type, id):
    model_name = PRODUCT_MODELS.get(product_type.lower())
    if not model_name:
        return render(request, '404.html') 

    ProductModel = apps.get_model('Rogue', model_name) 
    product = get_object_or_404(ProductModel, id=id)

    return render(request, 'product_detail.html', {
        'product': product,
        'product_type': product_type
    })
    
@login_required
def orders(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.quantity * apps.get_model('Rogue', PRODUCT_MODELS[item.product_type.lower()]).objects.get(id=item.product_id).price for item in cart_items)

    for item in cart_items:
        model_name = PRODUCT_MODELS.get(item.product_type.lower())
        if model_name:
            ProductModel = apps.get_model('Rogue', model_name)
            product = ProductModel.objects.get(id=item.product_id)
            item.product = product
            item.total_price = product.price * item.quantity
    orders = Order.objects.filter(user=request.user).order_by('-order_date')

    return render(request, 'orders.html', {'cart_items': cart_items, 'total_price': total_price, 'orders': orders})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'orders.html', {'orders': orders})
