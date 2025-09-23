from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, models
from ..dependencies import get_database_session

router = APIRouter()

# ЭНДПОИНТЫ ДЛЯ ВЫДАЧИ ИНСТРУМЕНТОВ
@router.post("/issue-tools/", response_model=schemas.ToolOrderResponse)
def create_tool_issue(
    tool_issue: schemas.ToolIssueCreate,
    db: Session = Depends(get_database_session)
):
    """
    СОЗДАТЬ заказ на ВЫДАЧУ инструментов со склада
    - IdOrder создается автоматически
    - time устанавливается автоматически (текущее время)
    """
    try:
        # Создаем новую запись в таблице выдачи
        db_issue = models.ToolIssue(
            IdEmployee=tool_issue.IdEmployee,
            station=tool_issue.station,
            store=tool_issue.store,

            screwdriver_minus=tool_issue.screwdriver_minus,
            screwdriver_plus=tool_issue.screwdriver_plus,
            screwdriver_on_the_offset_cross=tool_issue.screwdriver_on_the_offset_cross,
            whirlpool=tool_issue.whirlpool,
            scontouring_pliersaw=tool_issue.contouring_pliers,
            pliers=tool_issue.pliers,
            sharnitsa=tool_issue.sharnitsa,
            adjustable_wrench=tool_issue.adjustable_wrench,
            oil_can_opener=tool_issue.oil_can_opener,
            horn_wrench_union=tool_issue.horn_wrench_union,
            side_cutters=tool_issue.side_cutters
        )
        
        db.add(db_issue)
        db.commit()
        db.refresh(db_issue)
        
        return db_issue
        
    except Exception as e:
        db.rollback()  # Откатываем изменения в случае ошибки
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании заказа на выдачу: {str(e)}"
        )


@router.get("/issue-tools/", response_model=List[schemas.ToolOrderResponse])
def get_tool_issues(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_database_session)
):
    """
    ПОЛУЧИТЬ список всех заказов на ВЫДАЧУ инструментов
    """
    issues = db.query(models.ToolIssue).offset(skip).limit(limit).all()
    return issues


# ЭНДПОИНТЫ ДЛЯ СДАЧИ ИНСТРУМЕНТОВ
@router.post("/return-tools/", response_model=schemas.ToolOrderResponse)
def create_tool_return(
    tool_return: schemas.ToolReturnCreate,
    db: Session = Depends(get_database_session)
):
    """
    СОЗДАТЬ заказ на СДАЧУ инструментов на склад
    - IdOrder создается автоматически
    - time устанавливается автоматически (текущее время)
    """
    try:
        # Создаем новую запись в таблице сдачи
        db_return = models.ToolReturn(
            IdEmployee=tool_return.IdEmployee,
            station=tool_return.station,
            store=tool_return.store,
            screwdriver_minus=tool_return.screwdriver_minus,
            screwdriver_plus=tool_return.screwdriver_plus,
            screwdriver_on_the_offset_cross=tool_return.screwdriver_on_the_offset_cross,
            whirlpool=tool_return.whirlpool,
            scontouring_pliersaw=tool_return.contouring_pliers,
            pliers=tool_return.pliers,
            sharnitsa=tool_return.sharnitsa,
            adjustable_wrench=tool_return.adjustable_wrench,
            oil_can_opener=tool_return.oil_can_opener,
            horn_wrench_union=tool_return.horn_wrench_union,
            side_cutters=tool_return.side_cutters
        )
        
        db.add(db_return)
        db.commit()
        db.refresh(db_return)
        
        return db_return
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании заказа на сдачу: {str(e)}"
        )


@router.get("/return-tools/", response_model=List[schemas.ToolOrderResponse])
def get_tool_returns(
    skip: int = 0, 
    limit: int = 100,
    db: Session = Depends(get_database_session)
):
    """
    ПОЛУЧИТЬ список всех заказов на СДАЧУ инструментов
    """
    returns = db.query(models.ToolReturn).offset(skip).limit(limit).all()
    return returns


# ДОПОЛНИТЕЛЬНЫЕ ЭНДПОИНТЫ
@router.get("/employee-history/{employee_id}")
def get_employee_history(
    employee_id: int,
    db: Session = Depends(get_database_session)
):
    """
    ПОЛУЧИТЬ всю историю по сотруднику (и выдачу, и сдачу)
    """
    # Получаем все выдачи инструментов сотруднику
    issues = db.query(models.ToolIssue).filter(
        models.ToolIssue.IdEmployee == employee_id
    ).all()
    
    # Получаем все сдачи инструментов от сотрудника
    returns = db.query(models.ToolReturn).filter(
        models.ToolReturn.IdEmployee == employee_id
    ).all()
    
    return {
        "employee_id": employee_id,
        "tool_issues": issues,   # История выдач
        "tool_returns": returns  # История сдач
    }