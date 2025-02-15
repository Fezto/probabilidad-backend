from typing import List, Optional
from sqlalchemy import CheckConstraint, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .extensions import db


class Student(db.Model):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    ap: Mapped[str] = mapped_column(nullable=False)
    am: Mapped[str] = mapped_column(nullable=False)
    period: Mapped[str] = mapped_column(nullable=False)

class Asignature(db.Model):
    __tablename__ = "asignatures"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

class StudentAsignature(db.Model):
    __tablename__ = "students_asignatures"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    asignature_id: Mapped[int] = mapped_column(ForeignKey("asignatures.id"), nullable=False)
    first_partial: Mapped[Optional[float]] = mapped_column(nullable=True)
    second_partial: Mapped[Optional[float]] = mapped_column(nullable=True)
    third_partial: Mapped[Optional[float]] = mapped_column(nullable=True)
    average: Mapped[Optional[float]] = mapped_column(nullable=True)
    final_flag: Mapped[Optional[bool]] = mapped_column(nullable=True)
    student: Mapped[Student] = relationship("Student")
    asignature: Mapped[Asignature] = relationship("Asignature")