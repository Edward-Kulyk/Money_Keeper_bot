from typing import List

from sqlalchemy import BigInteger, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    tg_user_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    tg_chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True, nullable=False)
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    payment_mode: Mapped[str] = mapped_column(String, nullable=False, default="remember")

    operations: Mapped[List["Operation"]] = relationship("Operation", back_populates="owner")
    regular_operations: Mapped[List["RegularOperation"]] = relationship("RegularOperation", back_populates="owner")
    categories: Mapped[List["Category"]] = relationship("Category", back_populates="owner")


class Operation(Base):
    __tablename__ = "operation"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    shop: Mapped[str] = mapped_column(String)
    time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    card: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=True)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="operations")
    category: Mapped["Category"] = relationship("Category", back_populates="operations")


class RegularOperation(Base):
    __tablename__ = "regular_operation"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    regularity: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="regular_operations")


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="categories")
    operations: Mapped[List["Operation"]] = relationship("Operation", back_populates="category")
    shops: Mapped[List["ShopCategory"]] = relationship("ShopCategory", back_populates="category")


class ShopCategory(Base):
    __tablename__ = "shop_category"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    shop_name: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)

    category: Mapped["Category"] = relationship("Category", back_populates="shops")
