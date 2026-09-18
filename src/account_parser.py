import os
from models import Account, AccountStatus, SecurityInfo

def parse_accounts_file(filepath: str) -> list[Account]:
    accounts = []
    
    if not os.path.exists(filepath):
        return accounts

    lines = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        except Exception:
            pass

    idx = 1
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        parts = line.split('|')
        if len(parts) >= 2:
            username = parts[0].strip()
            password = parts[1].strip()
            if username and password:
                accounts.append(Account(
                    index=idx,
                    username=username,
                    password=password
                ))
                idx += 1
                
    return accounts
