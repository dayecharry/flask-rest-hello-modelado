from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()  # crear una instancia de SQlAlchemy

# POO programacion, orientada a objeto, clases (template), propiedades,  objetos, instancias


class Pet(db.Model):
    __tablename__ = "pet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    race: Mapped[str] = mapped_column(String(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "weight": self.weight,
            "race": self.race
        }


class Doctor(db.Model):
    __tablename__ = "doctor"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    speciality: Mapped[str] = mapped_column(
        String(100), nullable=False, unique=True)

    def serialize(self):
        return {
            "id": self.id,
            "speciality": self.speciality,
            "name": self.name
        }


class Owner(db.Model):
    __tablename__ = "owner"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(String(50), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone
        }

# CRUD--> crear, leer, actualizar, eliminar (datos). 
# guardar info de las mascotas,  info de los dueños de las mascotas, medicos  cual medico atendio a una mascota
# Modelo medico (especialidad, id, nombre).  RELACION M..N
# Modelo mascota (raza, peso, id, nombre, fk_Dueño) Modelo dueño(id, nombre, email, telefono) --> 1..M
