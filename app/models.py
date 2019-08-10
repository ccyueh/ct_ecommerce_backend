from app import app, db

class Product(db.Model):
    __tablename__ = 'product'

    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.String(10))
    description = db.Column(db.String(200))
    image_url = db.Column(db.String(100))

class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'))

    product = db.relationship('Product', backref=db.backref('cart', lazy='joined')) 
