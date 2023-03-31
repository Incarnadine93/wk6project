from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from werkzeug.security import check_password_hash

from .forms import productForm
from ..models import Product, User
from ..services import findproduct

products = Blueprint('products', __name__, template_folder='products_templates')

@products.route('/products', methods=['GET', 'POST'])
def product():
    form = productForm()
    my_list = range(1, 11)
    product_list = []
    for i in my_list:
        product_list.append(findproduct(i))
    if 'more_info' in request.form:
        product = findproduct(request.form['more_info'])
        return render_template('single_product.html', form=form, product=product)
    elif 'add_to_cart' in request.form:        
        product = findproduct(request.form['add_to_cart'])
        name = product['Name']
        price = product['Price']
        description = product['Description']
        img_url = product['img_url']
        category = product['Category']
        rating = product['Rating']
        user_id = current_user.id
        item = Product(name, price, description, img_url, category, rating, user_id)
        item.saveProduct()
        flash(f'{product["Name"]} added to cart')
    return render_template('products.html', form=form, product_list=product_list)