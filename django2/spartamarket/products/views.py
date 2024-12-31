from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product

# Create your views here.
def product_list_view(request):
    products = Product.objects.all()
    render(request, 'products/product_list.html', {'products': products})

@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, user = request.user)
        if form.is_valid():
            form.save()
            return redirect('products:product_list')
    else:
        form = ProductForm()
        
    return render(request, 'products/product_form.html', {'form' : form})

@login_required
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.views += 1
    product.save()
    return render(request, 'products/product_detail.html', {'product': product})

@login_required
def product_update_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user != request.user:
        return redirect('products:product_detail', pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance= product)
        if form.is_valid():
            form.save()
            return redirect('products:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product, initial= {'hashtags_str': ' '.join(ht.name for ht in product.hashtag.all())})
    return render(requestm, 'products/product_form.html', {'form' : form, 'product' : product})

@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.user != request.user:
        return redirect('products:product_detail', pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('products:product_list')
    return render(request, 'products/product_detail.html', {'product':product})

@login_required
def product_like_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user in product.likes.all():
        product.like.remove(request.user)
    else:
        product.likes.add(request.user)
    return redirect('products:product_detail', pk=pk)
