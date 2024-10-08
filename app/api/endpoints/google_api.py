from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (create_tables, set_user_permissions,
                                     fill_the_table_with_data)

router = APIRouter()


@router.get("/", dependencies=[Depends(current_superuser)])
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    """Создание отчета Google Sheets."""
    projects = await charity_project_crud.get_projects_by_completion_rate(session)
    spreadsheetid = await create_tables(wrapper_services)
    await set_user_permissions(spreadsheetid, wrapper_services)
    await fill_the_table_with_data(spreadsheetid, projects, wrapper_services)
    return projects
