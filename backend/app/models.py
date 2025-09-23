from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class ToolIssue(Base):
    """
    Таблица для УЧЕТА ВЫДАЧИ инструментов со склада
    Каждая запись - это один заказ на выдачу инструментов сотруднику
    """
    __tablename__ = "tool_issues"  # Таблица выдачи инструментов

    # Основные атрибуты заказа
    IdOrder = Column(Integer, primary_key=True, index=True, autoincrement=True) # ID заказа на выдачу
    IdEmployee = Column(Integer, nullable=False, index=True)  # ID сотрудника
    time = Column(DateTime(timezone=True), server_default=func.now())  # Время выдачи
    station = Column(String(100), nullable=False)  # Станция
    store = Column(String(100), nullable=False)   # Склад/хранилище

    # 11 столбцов для инструментов (количество ВЫДАННОГО)
    screwdriver_minus = Column(Integer, default=0)                     # 1. Отвертка «-»
    screwdriver_plus = Column(Integer, default=0)                      # 2. Отвертка «+»
    screwdriver_on_the_offset_cross = Column(Integer, default=0)       # 3. Отвертка на смещенный крест
    whirlpool = Column(Integer, default=0)                             # 4. Коловорот
    contouring_pliers = Column(Integer, default=0)                     # 5. Пассатижи контровочные
    pliers = Column(Integer, default=0)                                # 6. Пассатижи
    sharnitsa = Column(Integer, default=0)                             # 7. Шэрница
    adjustable_wrench = Column(Integer, default=0)                     # 8. Разводной ключ
    oil_can_opener = Column(Integer, default=0)                        # 9. Открывашка для банок с маслом
    horn_wrench_union = Column(Integer, default=0)                     # 10. Ключ рожковый/накидной ¾
    side_cutters = Column(Integer, default=0)                          # 11. Бокорезы


class ToolReturn(Base):
    """
    Таблица для УЧЕТА СДАЧИ инструментов на склад
    Каждая запись - это один заказ на сдачу инструментов от сотрудника
    """
    __tablename__ = "tool_returns"  # Таблица сдачи инструментов

    # Основные атрибуты заказа (такие же как в выдаче)
    IdOrder = Column(Integer, primary_key=True, index=True, autoincrement=True) # ID заказа на сдачу
    IdEmployee = Column(Integer, nullable=False, index=True)  # ID сотрудника
    time = Column(DateTime(timezone=True), server_default=func.now())  # Время сдачи
    station = Column(String(100), nullable=False)  # Станция
    store = Column(String(100), nullable=False)   # Склад/хранилище

    # 11 столбцов для инструментов (количество ВЫДАННОГО)
    screwdriver_minus = Column(Integer, default=0)                     # 1. Отвертка «-»
    screwdriver_plus = Column(Integer, default=0)                      # 2. Отвертка «+»
    screwdriver_on_the_offset_cross = Column(Integer, default=0)       # 3. Отвертка на смещенный крест
    whirlpool = Column(Integer, default=0)                             # 4. Коловорот
    contouring_pliers = Column(Integer, default=0)                     # 5. Пассатижи контровочные
    pliers = Column(Integer, default=0)                                # 6. Пассатижи
    sharnitsa = Column(Integer, default=0)                             # 7. Шэрница
    adjustable_wrench = Column(Integer, default=0)                     # 8. Разводной ключ
    oil_can_opener = Column(Integer, default=0)                        # 9. Открывашка для банок с маслом
    horn_wrench_union = Column(Integer, default=0)                     # 10. Ключ рожковый/накидной  ¾
    side_cutters = Column(Integer, default=0)                          # 11. Бокорезы