from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ToolOrderBase(BaseModel):
    """Базовая схема для заказа инструментов (общие поля для выдачи и сдачи)"""
    IdEmployee: int = Field(..., description="ID сотрудника")
    station: str = Field(..., max_length=100, description="Станция/участок")
    store: str = Field(..., max_length=100, description="Склад/хранилище")
    
    # 11 инструментов с значениями по умолчанию 0
    screwdriver_minus: int = Field(0, ge=0, description="Количество отверток «-»")
    screwdriver_plus: int = Field(0, ge=0, description="Количество отверток «+»")
    screwdriver_on_the_offset_cross: int = Field(0, ge=0, description="Количество отверток на смещеный крест")
    whirlpool: int = Field(0, ge=0, description="Количество коловоротов")
    contouring_pliers: int = Field(0, ge=0, description="Количество пассатижи контровочные")
    pliers: int = Field(0, ge=0, description="Количество пассатижи")
    sharnitsa: int = Field(0, ge=0, description="Количество шэрниц")
    adjustable_wrench: int = Field(0, ge=0, description="Количество разводных ключей")
    oil_can_opener: int = Field(0, ge=0, description="Количество открывашек для банок с маслом")
    horn_wrench_union: int = Field(0, ge=0, description="Количество ключей рожковый/накидной ¾")
    side_cutters: int = Field(0, ge=0, description="Количество бокорезов")


class ToolIssueCreate(ToolOrderBase):
    """Схема для СОЗДАНИЯ заказа на ВЫДАЧУ инструментов"""
    pass  # Все поля наследуются от ToolOrderBase


class ToolReturnCreate(ToolOrderBase):
    """Схема для СОЗДАНИЯ заказа на СДАЧУ инструментов"""
    pass  # Все поля наследуются от ToolOrderBase


class ToolOrderResponse(ToolOrderBase):
    """Схема для ОТВЕТА API (и для выдачи, и для сдачи)"""
    IdOrder: int = Field(..., description="Номер заказа")
    time: datetime = Field(..., description="Время создания заказа")

    class Config:
        from_attributes = True  # Для работы с ORM-объектами SQLAlchemy