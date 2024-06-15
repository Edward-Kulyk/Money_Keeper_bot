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
    payment_mode:Mapped[str] = mapped_column(String,nullable=False,default="Remember")

    operations: Mapped[List["Operation"]] = relationship("Operation", back_populates="owner")
    credit_cards: Mapped[List["CreditCard"]] = relationship("CreditCard", back_populates="owner")
    regular_operations: Mapped[List["RegularOperation"]] = relationship("RegularOperation", back_populates="owner")
    categories: Mapped[List["Category"]] = relationship("Category", back_populates="owner")


class Operation(Base):
    __tablename__ = "operation"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    time: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)
    card: Mapped[int] = mapped_column(ForeignKey("credit_card.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="operations")
    credit_card: Mapped["CreditCard"] = relationship("CreditCard", back_populates="operations")
    category: Mapped["Category"] = relationship("Category", back_populates="operations")


class CreditCard(Base):
    __tablename__ = "credit_card"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    last_4_digits: Mapped[str] = mapped_column(String(4), nullable=False)
    balance: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="credit_cards")
    operations: Mapped[List["Operation"]] = relationship("Operation", back_populates="credit_card")


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
