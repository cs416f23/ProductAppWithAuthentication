from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# CRUD Operations: Create, Retrieve, Update, Delete

# @login_required decorator allows to limit access to the index page and check whether the user is authenticated
# if so, index page is rendered. If not, the user is redirected to the login page via login_url
@login_required(login_url='login')
def index(request):
    # Retrieve all the products that are owned by the authenticated user and render products.html with the data
    products = Product.objects.filter(user=request.user)
    context = {'products': products}
    return render(request, 'products/index.html', context)


@login_required(login_url='login')
def create_product(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ProductForm(request.POST, request.FILES) # request.FILES is added for the image field
        # check whether it's valid:
        if form.is_valid():
            # Assign the current user as the user (i.e., owner) for each task
            form.instance.user = request.user
            # save the record into the db
            form.save()
            # after saving redirect to index page
            return redirect('index')
    else:
        # if the request does not have post data, a blank form will be rendered
        form = ProductForm()

    return render(request, 'products/product-form.html', {'form': form})


@login_required(login_url='login')
def update_product(request, product_id):
    # Get the product based on its id
    product = Product.objects.get(id=product_id, user=request.user)

    if request.method == 'POST':
        # populate a form instance with data from the data on the database
        # instance=product allows to update the record rather than creating a new record when save method is called
        form = ProductForm(request.POST, request.FILES, instance=product) # request.FILES is added for the image field
        # check whether it's valid:
        if form.is_valid():
            # Assign the current user as the user (i.e., owner) for each task
            form.instance.user = request.user
            # update the record in the db
            form.save()
            # after updating redirect to index page
            return redirect('index')
    else:
        # if the request does not have post data, render the page with the form containing the product's info
        form = ProductForm(instance=product)

    return render(request, 'products/product-form.html', {'form': form})


@login_required(login_url='login')
def delete_product(request, product_id):
    # Get the product based on its id
    product = Product.objects.get(id=product_id, user=request.user)

    # if this is a POST request, we need to delete the form data
    if request.method == 'POST':
        product.delete()
        # after deleting redirect to view_product page
        return redirect('index')

    # if the request is not post, render the page with the product's info
    return render(request, 'products/delete-confirm.html', {'product': product})


@login_required(login_url='login')
def search_product(request):
    search_term = request.GET['search-term'] or ''
    # query the database to find records that match with two criteria: user (user_id), and contains the search term
    products = Product.objects.filter(user=request.user, description__icontains=search_term)
    context = {'products': products}
    return render(request, 'products/index.html', context)


@login_required(login_url='login')
def delete_product_with_ajax(request):
    # Check if the request method is POST
    if request.method == 'POST':
        # Retrieve the product_id from the POST data.
        product_id = request.POST['product_id']

        # Query the product table with the given product_id and associated with the current user.
        product = Product.objects.get(id=product_id, user=request.user)

        # Delete the retrieved product.
        product.delete()

        # Return a JSON response indicating successful deletion.
        return JsonResponse(
            {
                'deleted': True,
                'message': 'You deleted the item. Yay!'
            }
        )

    # If the request method is not POST, return a JSON response indicating an error.
    return JsonResponse(
        {
            'message': 'Something went wrong!'
        }
    )
