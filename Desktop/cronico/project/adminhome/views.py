from django.shortcuts import render,redirect
from home.models import *
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from decimal import Decimal
from django.shortcuts import get_object_or_404

# Create your views here.

#-------------------------------------------admin login-------------------------------------------------------------------------------------------------------
def admin_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=authenticate(request, email=email,password=password)
        if user is not None and user.is_active and user.is_superadmin and user.is_staff and user.is_admin :
            login(request, user)
            messages.success(request, 'Successfully logged in.')
            return redirect('admin_index')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'adminhome/adminlogin.html')
    return render(request, 'adminhome/adminlogin.html')

#------------------------------------------admin index page--------------------------------------------------------------------------------------------------------
def admin_index(request):
    return render(request, 'adminhome/adminindex.html')

#------------------------------------------admin view the category-------------------------------------------------------------------------------------------
def admin_category(request):
    data=category.objects.all()
    context={
        'data':data
    }
    return render(request, 'adminhome/category.html', context)

#------------------------------------------admin add new category---------------------------------------------------------------------------------------------------
def admin_category_insert(request):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        slug = request.POST.get('slug')
        new_cat = category(category_name=category_name, slug=slug)
        new_cat.save()
        return redirect('admin_category')
    return render(request,'adminhome/category.html')

#------------------------------------------admin can edit the category-------------------------------------------------------------------------------------------
def admin_category_edit(request,id):
    if request.method == 'POST':
        category_name = request.POST.get('name')
        slug = request.POST.get('slug')
        edit=category.objects.get(id=id)
        edit.category_name = category_name
        edit.slug = slug
        edit.save()
        return redirect('admin_category')
    obj = category.objects.get(id=id)
    context = {
        "obj":obj
    }
    return render(request,'adminhome/category_edit.html', context)

#-------------------------------------------admin can view the product list---------------------------------------------------------------------------------------
def admin_product(request):
    # item = Product.objects.all()
    item = Product.objects.filter(is_deleted=False)
    context = {
        "item":item
    }
    return render(request,'adminhome/product.html', context)

#-------------------------------------------admin can add new product----------------------------------------------------------------------------------------------------
def admin_product_add(request):
    if request.method == 'POST':
        product_name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        price = Decimal(request.POST.get('price', 0))
        image = request.FILES.get('image1')
        # product_image1 = request.FILES.get('image2')
        # product_image2 = request.FILES.get('image3')
        stock = request.POST.get('stock')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        is_available = request.POST.get('is_available') == 'on'
        is_deleted = request.POST.get('is_deleted') == 'on'

        brand = Brand.objects.get(id=brand_id)
        category_obj = category.objects.get(id=category_id)
        new_product = Product(product_name=product_name,slug=slug,description=description,price=price,image=image,stock=stock,is_available=is_available,brand=brand,category=category_obj,is_deleted=is_deleted)
        new_product.save()
        images = request.FILES.getlist('images')
        for img in images:
            ProductImages.objects.create(product=new_product, images=img)
        return redirect('admin_product')
    brands = Brand.objects.all()
    categories = category.objects.all()
    context = {
        'brands': brands,
        'categories': categories,
        
    }
    return render(request,'adminhome/product_add.html',context)

#-------------------------------------------admin can edit the product--------------------------------------------------------------------------------------------
def admin_product_edit(request,id):
    product = get_object_or_404(Product, id=id)
    images = product.product_image.all()

    if request.method == 'POST':
        is_deleted = request.POST.get('is_deleted') == 'on'
        # Soft delete if is_deleted is True
        if is_deleted:
            product.soft_delete()
            return redirect("admin_product")
        # if is_deleted:
        #     product.is_deleted = True
        #     product.save()
        #     return redirect("admin_product")
        
        product_name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        price = Decimal(request.POST.get('price', 0))
        stock = request.POST.get('stock')
        is_available = request.POST.get('is_available')
        brand_id = request.POST.get('brand')
        category_id = request.POST.get('category')
        is_deleted = request.POST.get('is_deleted') == 'on'
        brand = Brand.objects.get(id=brand_id)
        category_obj = category.objects.get(id=category_id)
        # product = Product.objects.get(id=id)
        product.product_name = product_name
        product.slug = slug
        product.description = description
        product.price = price
        product.stock = stock
        product.is_available = is_available
        product.brand = brand
        product.category = category_obj
        product.is_deleted = is_deleted
         # Update image fields only if new files are provided
        if request.FILES.get('image'):
            product.image = request.FILES.get('image')
        # if request.FILES.get('image2'):
        #     product.product_image1 = request.FILES.get('image2')
        # if request.FILES.get('image3'):
        #     product.product_image2 = request.FILES.get('image3')
        images = request.FILES.getlist('images')
        for img in images:
            ProductImages.objects.create(product=product, images=img)
        
        # Handle deletion of images
        deleted_image_ids = request.POST.getlist('delete_image')
        ProductImages.objects.filter(id__in=deleted_image_ids).delete()

        # Handle modification of existing images
        for img in images:
            img_file = request.FILES.get(f'image_{img.id}')
            if img_file:
                img.images = img_file
                img.save()
         # Handle addition of new images
        new_images = request.FILES.getlist('images')
        for img_file in new_images:
            ProductImages.objects.create(product=product, images=img_file)


        product.save()
        return redirect("admin_product") 
    # product = Product.objects.get(id=id)
    brands = Brand.objects.all()
    categories = category.objects.all()
    context={
        'product':product,
        'brands': brands,
        'categories': categories,
        'images': images,
    }
    return render(request,'adminhome/product_edit.html', context)

#---------------------------------------admin can view the customers list-----------------------------------------------------------------------------------------
def customers(request):
    user = User.objects.all()
    context = {
        'user':user
    }
    return render(request, 'adminhome/customers.html',context)


#---------------------------------------admin can block and unblock the user--------------------------------------------------------------------------------------------
def block_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    blocked_users = request.session.get('blocked_users', [])
    if user.id not in blocked_users:
        blocked_users.append(user.id)
        messages.success(request, f'{user.username} has been blocked.')
    else:
        blocked_users.remove(user.id)
        messages.success(request, f'{user.username} has been unblocked.')

    request.session['blocked_users'] = blocked_users
    return redirect('customers')  




