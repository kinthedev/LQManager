from dataclasses import dataclass
from enum import Enum
from typing import Optional

class AccountStatus(Enum):
    UNCHECKED = 'Chưa check'
    LIVE = 'Hoạt động'
    WRONG_PASSWORD = 'Sai mật khẩu'
    BANNED = 'Bị khóa'
    CAPTCHA = 'Kẹt Captcha'

class SecurityInfo(Enum):
    NONE = 'Trắng thông tin'
    PHONE = 'Đã gắn SĐT'
    EMAIL = 'Đã gắn Email'

class RankTier(Enum):
    DONG = 'Đồng'
    BAC = 'Bạc'
    VANG = 'Vàng'
    BACH_KIM = 'Bạch Kim'
    KIM_CUONG = 'Kim Cương'
    TINH_ANH = 'Tinh Anh'
    CAO_THU = 'Cao Thủ'
    DAI_CAO_THU = 'Đại Cao Thủ'

@dataclass
class Account:
    index: int
    username: str
    password: str
    status: AccountStatus = AccountStatus.UNCHECKED
    security: SecurityInfo = SecurityInfo.NONE
    heroes_count: int = 0
    skins_count: int = 0
    gold: int = 0
    military_medals: int = 0
    rank: Optional[RankTier] = None
    credibility_score: int = 0

@dataclass
class CheckResult:
    success: bool
    status: AccountStatus
    security: SecurityInfo
    heroes_count: int
    skins_count: int
    gold: int
    military_medals: int
    rank: RankTier
    credibility_score: int
