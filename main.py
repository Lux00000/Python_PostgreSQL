
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)

class Product(Base):
    __tablename__ = 'product'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)

class ProductPhoto(Base):
    __tablename__ = 'product_photo'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    url = Column(String(200), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship(Product)

class Cart(Base):
    __tablename__ = 'cart'
    __table_args__ = {"extend_existing": True}
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship(Customer)

class CartProduct(Base):
    __tablename__ = 'cart_product'
    __table_args__ = {"extend_existing": True}
    cart_id = Column(Integer, ForeignKey('cart.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('product.id'), primary_key=True)


engine = create_engine('postgresql://username:password@localhost/mydatabase')
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()


customer1 = Customer(name='John Doe', phone='1234567890', email='john@example.com')
customer2 = Customer(name='Jane Smith', phone='0987654321', email='jane@example.com')
session.add_all([customer1, customer2])
session.commit()

product1 = Product(name='Product 1', description='Description 1', price=9.99)
product2 = Product(name='Product 2', description='Description 2', price=19.99)
session.add_all([product1, product2])
session.commit()

product_photo1 = ProductPhoto(url='http://example.com/photo1.jpg', product=product1)
product_photo2 = ProductPhoto(url='http://example.com/photo2.jpg', product=product2)
session.add_all([product_photo1, product_photo2])
session.commit()

cart1 = Cart(customer=customer1)
cart2 = Cart(customer=customer2)
session.add_all([cart1, cart2])
session.commit()

cart_product1 = CartProduct(cart=cart1, product=product1)
cart_product2 = CartProduct(cart=cart2, product=product2)
session.add_all([cart_product1, cart_product2])
session.commit()



# Select
customers = session.query(Customer).all()
for customer in customers:
    print(customer.name)

# Group
from sqlalchemy import func
products_count = session.query(Product.name, func.count(CartProduct.product_id)).join(CartProduct).group_by(Product.name).all()
for product_name, count in products_count:
    print(product_name, count)

# Join
cart_products = session.query(CartProduct).join(Cart).join(Product).all()
for cart_product in cart_products:
    print(cart_product.cart.customer.name, cart_product.product.name)

# Having
products_count = session.query(Product.name, func.count(CartProduct.product_id)).join(CartProduct).group_by(Product.name).having(func.count(CartProduct.product_id) > 1).all()
for product_name, count in products_count:
    print(product_name, count)
