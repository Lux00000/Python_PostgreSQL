from typing import List
from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey

engine = create_engine("postgresql+psycopg2://postgres:99910999danil@localhost:5432/python_db")
conn = engine.connect()

class Base(DeclarativeBase):
    __table__: Table
    meta = MetaData()

class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]

    def __repr__(self) -> str:

        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r})"

class Product(Base):
    __tablename__ = "product"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(String(500))
    price: Mapped[int] = mapped_column(Integer)

    def __repr__(self) -> str:

        return f"Product(id={self.id!r}, name={self.name!r}, description={self.description!r}, price={self.price!r})"


class ProductPhoto(Base):
    __tablename__ = "product_photo"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(100))
    pr_id: Mapped[int] = mapped_column(ForeignKey("product.id"))


class Cart(Base):
    __tablename__ = "cart"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))

class CartProduct(Base):
    __tablename__ = "cart_product"
    __table_args__ = {"extend_existing": True}

    cart_id: Mapped[int] = mapped_column(ForeignKey("cart.id"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)

Base.metadata.create_all(engine)
print("well")

with Session(engine) as session:
    spongebob = Customer(
        name = "spongebob",
        email="spongebob@sqlalchemy.org"
    )

    sandy = Customer(
    name = "sandy",
    email ="sandy@sqlalchemy.org"

    )
session.add_all([spongebob, sandy])
session.commit()






print("well")