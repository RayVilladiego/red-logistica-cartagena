from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

DATABASE_URL = "sqlite:///logistica.db"  # Cambia a tu URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, index=True)
    estado = Column(String, default="activo")
    tiempo_estimado = Column(Float)
    fecha_creacion = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)

# Uso:
# init_db()
# session = SessionLocal()
# nuevo_pedido = Pedido(cliente="Empresa X", tiempo_estimado=45.5)
# session.add(nuevo_pedido)
# session.commit()
