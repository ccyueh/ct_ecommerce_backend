from app import app, db
from flask import request, jsonify
from app.models import Product, Cart

# set index route to return nothing, just so no error occurs
@app.route('/')
def index():
    return ''

@app.route('/api/add', methods=['POST'])
def add():
    try:
        # get headers first
        name = request.headers.get('name')
        price = request.headers.get('price')
        description = request.headers.get('description')
        image_url = request.headers.get('image_url')
        product_id = request.headers.get('product_id')

        # different combinations of data will be provided 
        # depending on whether a product is being added to the inventory or an item is being added to the cart
        # must follow either of these patterns
        if product_id and not name and not price and not description and not image_url:
            cart = Cart(product_id=product_id)
            
            db.session.add(cart)
            db.session.commit()
            
            return jsonify({ 'success': 'Added item to cart' })
        elif name and price and description and image_url and not product_id:
            product = Product(name=name, price=price, description=description, image_url=image_url)
            
            db.session.add(product)
            db.session.commit()
            
            return jsonify({ 'success': 'Added product to inventory' })
        else:
            return jsonify({ 'error': 'Error #001: Invalid parameters' })
    except:
        return jsonify({ 'error': 'Error #002: Could not add item/product' })

@app.route('/api/retrieve', methods=['GET'])
def retrieve():
    try:
        table = request.headers.get('table')

        if table:
            if table == 'products':
                results = Product.query.all()
                
                products = []
                for result in results:
                    product = {
                        'product_id': result.product_id,
                        'name': result.name,
                        'price': result.price,
                        'description': result.description,
                        'image_url': result.image_url
                    }
                    products.append(product)
                
                return jsonify({ 'success': 'Retrieved products list', 'products': products }); 
            elif table == 'cart':
                results = db.session.query(Cart.cart_id, Product.product_id, Product.name, Product.price).join(Product).all()
                cart = []
                for result in results:
                    item = {
                        'cart_id': result.cart_id,
                        'product_id': result.product_id,
                        'name': result.name,   
                        'price': result.price
                    }
                    cart.append(item)
            
                return jsonify({ 'success': 'Retrieved cart', 'cart': cart }); 

        return jsonify({ 'error': 'Error #003: Could not retrieve cart/products' })
    except:
        return jsonify({ 'error': 'Error #004: Could not retrieve cart/products' })

@app.route('/api/delete', methods=['DELETE'])
def delete():
    try:
        product_id = request.headers.get('product_id')
        cart_id = request.headers.get('cart_id')
        if not product_id and not cart_id:
            return jsonify({ 'error': 'Error #005: Product/Cart ID required for deletion' })
        elif product_id and not cart_id:
            product = Product.query.filter_by(product_id=product_id).first()

            db.session.delete(product)
            db.session.commit()

            return jsonify({ 'success': 'Product deleted' })
        elif cart_id and not product_id:
            item = Cart.query.filter_by(cart_id=cart_id).first()

            db.session.delete(item)
            db.session.commit()

            return jsonify({ 'success': 'Item deleted' })
        else:
            return jsonify({ 'error': 'Error #006: Could not delete item/product' })
    except:
        return jsonify({ 'error': 'Error #007: Could not delete item/product' })
