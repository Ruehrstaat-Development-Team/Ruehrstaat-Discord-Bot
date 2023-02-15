from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    __allow_unmapped__ = True
    pass


class Discord_Guild(Base):
    __tablename__ = "discord_guilds"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    roles: List["Discord_Role"] = relationship(
        "Discord_Role", back_populates="guild", cascade="all, delete-orphan")

    channels: List["Discord_Channel"] = relationship(
        "Discord_Channel", back_populates="guild", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Discord_Guild(id={self.id}, name={self.name})"


class Discord_Role(Base):
    __tablename__ = "discord_roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    mention: Mapped[str] = mapped_column(String(32))
    managed: Mapped[bool] = mapped_column()

    guild_id: Mapped[int] = mapped_column(ForeignKey("discord_guilds.id"))

    guild: Mapped[Discord_Guild] = relationship(
        "Discord_Guild", back_populates="roles")
    
    carrier_discord_channels: List["Carrier_Discord_Channel"] = relationship(
        "Carrier_Discord_Channel", back_populates="role", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Discord_Role(id={self.id}, name={self.name}, mention={self.mention}, managed={self.managed}, guild_id={self.guild_id})"


class Discord_Channel(Base):
    __tablename__ = "discord_channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    jump_url: Mapped[str] = mapped_column(String(255))
    mention: Mapped[str] = mapped_column(String(32))

    guild_id: Mapped[int] = mapped_column(ForeignKey("discord_guilds.id"))

    guild: Mapped[Discord_Guild] = relationship(
        "Discord_Guild", back_populates="channels")

    carrier_discord_channels: List["Carrier_Discord_Channel"] = relationship(
        "Carrier_Discord_Channel", back_populates="channel", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Discord_Channel(id={self.id}, name={self.name}, jump_url={self.jump_url}, mention={self.mention}, guild_id={self.guild_id})"


class Carrier_Discord_Channel(Base):
    __tablename__ = "carrier_discord_channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    carrier_market_id: Mapped[int] = mapped_column()
    type: Mapped[str] = mapped_column(String(255))

    channel_id: Mapped[int] = mapped_column(ForeignKey("discord_channels.id"))
    role_id: Mapped[int] = mapped_column(ForeignKey("discord_roles.id"))
    
    channel: Mapped[Discord_Channel] = relationship(
        "Discord_Channel", back_populates="carrier_discord_channels")
    
    role: Mapped[Discord_Role] = relationship(
        "Discord_Role", back_populates="carrier_discord_channels")
