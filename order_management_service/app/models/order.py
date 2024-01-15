from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    # Define other user attributes (e.g., name, email)

    # Define one-to-many relationship with orders
    orders = relationship('Order', back_populates='user')


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Add user_id field
    status = Column(Enum('pending', 'processing', 'shipped', 'delivered'), default='pending')
    order_date = Column(DateTime, nullable=False)
    item_description = Column(String, nullable=False)  # Add item description field
    quantity = Column(Integer, nullable=False)  # Add quantity field
    total_price = Column(Float, nullable=False)  # Add total price field
    shipping_address = Column(String, nullable=False)  # Add shipping address field

    # Define many-to-one relationship with users
    user = relationship('User', back_populates='orders')

    # Define one-to-one relationship with shipment
    shipment = relationship('Shipment', uselist=False, back_populates='order')


class Shipment(Base):
    __tablename__ = 'shipments'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    status = Column(Enum('processing', 'shipped', 'delivered'), default='processing')
    tracking_number = Column(String, unique=True)
    estimated_delivery_date = Column(DateTime)
    # Define other shipment attributes

    # Define one-to-one relationship with order
    order = relationship('Order', back_populates='shipment')


class InventoryItem(Base):
    __tablename__ = 'inventory_items'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    item_type = Column(Enum('product', 'part'), default='product')
    # Define other item attributes (e.g., description)

    # Define many-to-many relationship with orders
    orders = relationship('Order', secondary='order_inventory_item_association', back_populates='inventory_items')


class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    calculated_price = Column(Float, nullable=False)
    quote_date = Column(DateTime, nullable=False)
    # Define other quote attributes

    # Define many-to-one relationship with order
    order = relationship('Order', back_populates='quote')


# Define additional tables and relationships for feedback, pricing, reports, etc.

# Create an association table for the many-to-many relationship between orders and inventory items
order_inventory_item_association = Table('order_inventory_item_association', Base.metadata,
                                         Column('order_id', Integer, ForeignKey('orders.id')),
                                         Column('inventory_item_id', Integer, ForeignKey('inventory_items.id'))
                                         )

