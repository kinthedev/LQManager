import csv
from models import Account, AccountStatus

def export_live_accounts(accounts: list[Account], filepath: str):
    live_accounts = [acc for acc in accounts if acc.status == AccountStatus.LIVE]
    with open(filepath, 'w', encoding='utf-8') as f:
        for acc in live_accounts:
            f.write(f"{acc.username}|{acc.password}\n")

def export_report_csv(accounts: list[Account], filepath: str):
    headers = [
        'STT', 'Tài khoản', 'Mật khẩu', 'Trạng thái', 'Bảo mật', 
        'Tướng', 'Trang phục', 'Vàng', 'Quân huy', 'Bậc Rank', 'Điểm uy tín'
    ]
    
    with open(filepath, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        
        for acc in accounts:
            rank_str = acc.rank.value if acc.rank else ''
            security_str = acc.security.value if acc.security else ''
            
            row = [
                acc.index,
                acc.username,
                acc.password,
                acc.status.value,
                security_str,
                acc.heroes_count,
                acc.skins_count,
                acc.gold,
                acc.military_medals,
                rank_str,
                acc.credibility_score
            ]
            writer.writerow(row)
