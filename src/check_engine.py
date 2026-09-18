import time
import random
import threading
from abc import ABC, abstractmethod
from typing import Callable, List

from models import Account, AccountStatus, SecurityInfo, RankTier, CheckResult

class BaseCheckEngine(ABC):
    @abstractmethod
    def check(self, account: Account) -> CheckResult:
        pass

class MockCheckEngine(BaseCheckEngine):
    def __init__(self, delay_min: float = 1.0, delay_max: float = 3.0):
        self.delay_min = delay_min
        self.delay_max = delay_max

    @property
    def delay(self):
        return self.delay_min

    @delay.setter
    def delay(self, val: float):
        """Set both min and max delay. Max = min + 1."""
        self.delay_min = max(0.5, val)
        self.delay_max = self.delay_min + 1.0

    def check(self, account: Account) -> CheckResult:
        # Simulate network delay
        time.sleep(random.uniform(self.delay_min, self.delay_max))
        
        status_roll = random.random()
        if status_roll < 0.60:
            status = AccountStatus.LIVE
        elif status_roll < 0.80:
            status = AccountStatus.WRONG_PASSWORD
        elif status_roll < 0.90:
            status = AccountStatus.BANNED
        else:
            status = AccountStatus.CAPTCHA

        if status == AccountStatus.LIVE:
            success = True
            heroes = random.randint(10, 100)
            skins = random.randint(5, 200)
            gold = random.randint(1000, 999999)
            medals = random.randint(100, 99999)
            rank = random.choice(list(RankTier))
            credibility = random.randint(60, 100)
            security = random.choice(list(SecurityInfo))
        else:
            success = False
            heroes = 0
            skins = 0
            gold = 0
            medals = 0
            rank = RankTier.DONG
            credibility = 0
            security = SecurityInfo.NONE

        return CheckResult(
            success=success,
            status=status,
            security=security,
            heroes_count=heroes,
            skins_count=skins,
            gold=gold,
            military_medals=medals,
            rank=rank,
            credibility_score=credibility
        )

    def check_accounts(self, accounts: List[Account], callback: Callable[[Account, CheckResult], None], stop_event: threading.Event, pause_event: threading.Event):
        """
        Check all accounts sequentially.
        - pause_event: SET = running, CLEAR = paused
        - stop_event: SET = stop immediately
        """
        for account in accounts:
            if stop_event.is_set():
                break
                
            # Block while paused (pause_event is CLEAR when paused)
            while not pause_event.is_set():
                if stop_event.is_set():
                    return
                time.sleep(0.2)
                
            result = self.check(account)
            
            # Update account object
            account.status = result.status
            account.security = result.security
            account.heroes_count = result.heroes_count
            account.skins_count = result.skins_count
            account.gold = result.gold
            account.military_medals = result.military_medals
            account.rank = result.rank
            account.credibility_score = result.credibility_score
            
            callback(account, result)
