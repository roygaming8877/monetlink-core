# app/crud/crud_referral.py
from app.crud.base import CRUDBase
from app.models.referral import Referral
from app.schemas.referral import ReferralCreate, ReferralBase

class CRUDReferral(CRUDBase[Referral, ReferralCreate, ReferralBase]):
    pass

referral = CRUDReferral(Referral)

# ==========================================
# app/crud/crud_page.py
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.page import CustomPage
from pydantic import BaseModel

class PageCreate(BaseModel): pass
class PageUpdate(BaseModel): pass

class CRUDCustomPage(CRUDBase[CustomPage, PageCreate, PageUpdate]):
    async def get_by_slug(self, db: AsyncSession, *, slug: str) -> Optional[CustomPage]:
        query = select(CustomPage).where(CustomPage.slug == slug)
        result = await db.execute(query)
        return result.scalar_one_or_none()

custom_page = CRUDCustomPage(CustomPage)

# ==========================================
# app/crud/crud_setting.py
from app.crud.base import CRUDBase
from app.models.setting import SystemSetting
from app.schemas.admin import SystemSettingCreate, SystemSettingUpdate

class CRUDSystemSetting(CRUDBase[SystemSetting, SystemSettingCreate, SystemSettingUpdate]):
    pass

system_setting = CRUDSystemSetting(SystemSetting)
