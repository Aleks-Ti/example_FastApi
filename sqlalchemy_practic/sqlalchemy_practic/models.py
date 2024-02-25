from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

metadata = MetaData()


@as_declarative(metadata=metadata)
class Base:
    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __allow_unmapped__ = False


#####
# up settings


# class PodGroup(Base):
#     __tablename__ = "pod_group"

#     id: Mapped[int] = mapped_column(
#         sa.BigInteger, primary_key=True, nullable=False, unique=True
#     )
#     name: Mapped[str] = mapped_column(
#         sa.String(256), nullable=False, unique=True
#     )
#     group = relationship("Group", back_populates="pod_group", uselist=False)

#     def __repr__(self) -> str:
#         return f"PodGroup(id={self.id!r}, name={self.name!r})"


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(
        sa.BigInteger, primary_key=True, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        sa.String(256), nullable=False, unique=True
    )
    # pod_group_id: Mapped[int] = mapped_column(
    #     sa.ForeignKey("pod_group.id"),
    #     primary_key=True,
    #     unique=True,
    #     nullable=False,
    # )

    # pod_group = relationship("PodGroup", back_populates="group", uselist=True)
    user = relationship("UserGroup", back_populates="group", uselist=True)

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, name={self.name!r})"


class UserGroup(Base):
    __tablename__ = "user_group"
    __table_args__ = (
        sa.UniqueConstraint(
            "user_id", "group_id", name="unique_for_user_one_unique_group"
        ),
    )

    id: Mapped[int] = mapped_column(
        sa.BigInteger, primary_key=True, nullable=False, unique=True
    )
    group_id: Mapped[int] = mapped_column(
        sa.ForeignKey("group.id"), nullable=False, unique=False
    )
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id"), nullable=False, unique=False
    )

    group = relationship(
        "Group", back_populates="user", uselist=False, lazy=False
    )
    user = relationship(
        "User", back_populates="group", uselist=False, lazy=False
    )

    def __repr__(self) -> str:
        return f"UserGroup(id={self.id!r}, group_id={self.group_id!r}, user_id={self.user_id!r})"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        sa.BigInteger, primary_key=True, nullable=False, unique=True
    )
    name: Mapped[str] = mapped_column(
        sa.String(30), nullable=True, unique=False
    )
    fullname: Mapped[str] = mapped_column(
        sa.String(256), nullable=True, unique=False
    )
    """случай когда можно указать стратегию загрузки сразу, но тут нужно знать наперед,
    какие обращения могут быть, и не будет ли избыточным обращаться к User и все время делать
    доп запросы в БД на связанные таблицы!
    """
    # addresses = relationship(
    #     "Address", back_populates="user", uselist=False, lazy="selectin"
    # )
    # group = relationship("UserGroup", back_populates="user", uselist=True, lazy="selectin")
    # profile = relationship("ProfileUser", back_populates="user", uselist=False, lazy="selectin")
    addresses = relationship(
        "Address", back_populates="user", uselist=False, lazy=False
    )
    group = relationship(
        "UserGroup", back_populates="user", uselist=True, lazy=False
    )
    profile = relationship(
        "ProfileUser", back_populates="user", uselist=False, lazy=False
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(
        sa.BigInteger, primary_key=True, nullable=False, unique=True
    )
    email_address: Mapped[str] = mapped_column(
        sa.String(256), nullable=False, unique=False
    )

    user_id = mapped_column(
        sa.ForeignKey("user.id"), nullable=False, unique=True
    )
    user = relationship("User", back_populates="addresses", uselist=False)


class ProfileUser(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(
        sa.BigInteger, primary_key=True, nullable=False, unique=True
    )
    date: Mapped[datetime] = mapped_column(
        sa.DateTime(timezone=False),
        nullable=False,
        unique=False,
        default=datetime.now,
    )
    zodiac: Mapped[str] = mapped_column(
        sa.String(64), nullable=True, unique=False
    )
    user_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id"), nullable=False, unique=True
    )

    user = relationship("User", back_populates="profile", uselist=False)
