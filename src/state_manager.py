"""
Lưu và khôi phục trạng thái tài khoản đã check.
File state được lưu cùng thư mục với file accounts gốc, 
với đuôi .lqm.json (ví dụ: accounts.txt → accounts.lqm.json)
"""
import json
import os
from typing import List

from models import Account, AccountStatus, SecurityInfo, RankTier


def _get_state_filepath(accounts_filepath: str) -> str:
    """Tạo đường dẫn file state từ đường dẫn file accounts."""
    base, _ = os.path.splitext(accounts_filepath)
    return base + ".lqm.json"


def save_state(accounts: List[Account], accounts_filepath: str) -> None:
    """Lưu trạng thái tất cả tài khoản ra file JSON."""
    state_path = _get_state_filepath(accounts_filepath)
    data = []
    for acc in accounts:
        data.append({
            "index": acc.index,
            "username": acc.username,
            "password": acc.password,
            "status": acc.status.value if acc.status else None,
            "security": acc.security.value if acc.security else None,
            "heroes_count": acc.heroes_count,
            "skins_count": acc.skins_count,
            "gold": acc.gold,
            "military_medals": acc.military_medals,
            "rank": acc.rank.value if acc.rank else None,
            "credibility_score": acc.credibility_score,
        })
    
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_state(accounts_filepath: str) -> List[Account] | None:
    """
    Khôi phục trạng thái tài khoản từ file JSON.
    Trả về None nếu không tìm thấy file state.
    """
    state_path = _get_state_filepath(accounts_filepath)
    
    if not os.path.exists(state_path):
        return None
    
    try:
        with open(state_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    
    # Map string values back to enums
    status_map = {s.value: s for s in AccountStatus}
    security_map = {s.value: s for s in SecurityInfo}
    rank_map = {r.value: r for r in RankTier}
    
    accounts = []
    for item in data:
        acc = Account(
            index=item.get("index", 0),
            username=item.get("username", ""),
            password=item.get("password", ""),
            status=status_map.get(item.get("status"), AccountStatus.UNCHECKED),
            security=security_map.get(item.get("security"), SecurityInfo.NONE),
            heroes_count=item.get("heroes_count", 0),
            skins_count=item.get("skins_count", 0),
            gold=item.get("gold", 0),
            military_medals=item.get("military_medals", 0),
            rank=rank_map.get(item.get("rank")),
            credibility_score=item.get("credibility_score", 0),
        )
        accounts.append(acc)
    
    return accounts


def has_saved_state(accounts_filepath: str) -> bool:
    """Kiểm tra xem file accounts có state đã lưu không."""
    return os.path.exists(_get_state_filepath(accounts_filepath))

