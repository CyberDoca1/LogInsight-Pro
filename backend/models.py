"""
Modelos SQLAlchemy para LogInsight Pro
"""

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, Date, Boolean, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import JSONB, TSVECTOR
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy import func, cast, Index

from .database import Base

# Tabla de asociación muchos a muchos entre URLs y cuentas
url_account = Table(
    "url_account_mappings",
    Base.metadata,
    Column("url_id", Integer, ForeignKey("urls.id", ondelete="CASCADE"), primary_key=True),
    Column("account_id", Integer, ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True),
    Column("last_used", Date, nullable=True),
    Column("frequency", Integer, default=1),
)

# Tabla de asociación muchos a muchos entre cuentas y contraseñas
account_password = Table(
    "account_password_mappings",
    Base.metadata,
    Column("account_id", Integer, ForeignKey("accounts.id", ondelete="CASCADE"), primary_key=True),
    Column("password_id", Integer, ForeignKey("passwords.id", ondelete="CASCADE"), primary_key=True),
    Column("is_current", Boolean, default=True),
    Column("last_used", Date, nullable=True),
)

# Tabla de asociación entre URLs y grupos de URLs
url_group_mapping = Table(
    "url_group_mappings",
    Base.metadata,
    Column("url_id", Integer, ForeignKey("urls.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", Integer, ForeignKey("url_groups.id", ondelete="CASCADE"), primary_key=True),
    Column("similarity", Float, nullable=False),
)


class URL(Base):
    """
    Modelo para URLs únicas
    """
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, nullable=False, index=True)
    url_normalized = Column(String, nullable=False, index=True)
    domain = Column(String, nullable=False, index=True)
    
    # Relaciones
    accounts = relationship("Account", secondary=url_account, back_populates="urls")
    groups = relationship("URLGroup", secondary=url_group_mapping, back_populates="urls")
    
    # Búsqueda de texto completo
    search_vector = Column(TSVECTOR)
    
    # Índices
    __table_args__ = (
        Index('idx_urls_trgm', url, postgresql_using='gin', postgresql_ops={'url': 'gin_trgm_ops'}),
        Index('idx_urls_search_vector', search_vector, postgresql_using='gin'),
    )


class Account(Base):
    """
    Modelo para cuentas de usuario
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=True, index=True)
    
    # Relaciones
    urls = relationship("URL", secondary=url_account, back_populates="accounts")
    passwords = relationship("Password", secondary=account_password, back_populates="accounts")


class Password(Base):
    """
    Modelo para contraseñas únicas
    """
    __tablename__ = "passwords"

    id = Column(Integer, primary_key=True, index=True)
    password_hash = Column(String, unique=True, nullable=False)
    password_strength = Column(Integer, nullable=False)
    
    # Relaciones
    accounts = relationship("Account", secondary=account_password, back_populates="passwords")


class URLGroup(Base):
    """
    Modelo para grupos de URLs similares
    """
    __tablename__ = "url_groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    pattern = Column(String, nullable=False, index=True)
    
    # Relaciones
    urls = relationship("URL", secondary=url_group_mapping, back_populates="groups")
    
    @hybrid_property
    def url_count(self):
        """
        Propiedad híbrida que devuelve el número de URLs en el grupo
        """
        return len(self.urls)