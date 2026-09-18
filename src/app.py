import customtkinter as ctk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import threading
from typing import List

from models import Account, AccountStatus, SecurityInfo, RankTier, CheckResult
from account_parser import parse_accounts_file
from check_engine import MockCheckEngine
from exporter import export_live_accounts, export_report_csv
from state_manager import save_state, load_state, has_saved_state
from utils import copy_to_clipboard, mask_password, format_number

from widgets.status_bar import StatusBar
from widgets.filter_bar import FilterBar
from widgets.toolbar import Toolbar
from widgets.account_table import AccountTable

class LQManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.title("LQManager - Quản lý Tài khoản Liên Quân Mobile")
        self.geometry("1280x720")
        
        # Center on screen
        self.update_idletasks()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        x = (screen_w // 2) - (1280 // 2)
        y = (screen_h // 2) - (720 // 2)
        self.geometry(f"1280x720+{x}+{y}")
        
        # State
        self.accounts: List[Account] = []
        self.current_filepath: str | None = None  # Đường dẫn file đang mở
        self.check_thread: threading.Thread | None = None
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        self.pause_event.set()  # SET = running (not paused)
        self.engine = MockCheckEngine(delay_min=1.0, delay_max=3.0)
        self._checked_count = 0
        
        # Layout
        self.toolbar = Toolbar(self)
        self.toolbar.pack(side="top", fill="x", padx=10, pady=(10, 5))
        
        self.filter_bar = FilterBar(self, on_filter_changed=self.on_filter_changed)
        self.filter_bar.pack(side="top", fill="x", padx=10, pady=2)
        
        self.account_table = AccountTable(self)
        self.account_table.pack(side="top", fill="both", expand=True, padx=10, pady=5)
        self.account_table.on_recheck_callback = self._recheck_single
        
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side="bottom", fill="x", padx=10, pady=(5, 10))
        
        # Callbacks
        self.toolbar.set_callbacks(
            on_open=self.open_file,
            on_start=self.start_checking,
            on_pause=self.pause_checking,
            on_resume=self.resume_checking,
            on_stop=self.stop_checking,
            on_export_live=self.export_live,
            on_export_csv=self.export_csv,
            on_delay_change=self.change_delay
        )
        
        # Auto-save khi đóng app
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
    def open_file(self):
        file_path = filedialog.askopenfilename(
            title="Chọn file tài khoản",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            self.current_filepath = file_path
            
            # Kiểm tra có state đã lưu không
            if has_saved_state(file_path):
                saved = load_state(file_path)
                if saved:
                    self.accounts = saved
                    self.account_table.load_accounts(self.accounts)
                    # Đếm số acc đã check
                    self._checked_count = sum(
                        1 for a in self.accounts 
                        if a.status != AccountStatus.UNCHECKED
                    )
                    self.status_bar.reset()
                    self.status_bar.update_progress(self._checked_count, len(self.accounts))
                    self._update_stats()
                    return
            
            # Không có state → parse từ file txt
            self.accounts = parse_accounts_file(file_path)
            self.account_table.load_accounts(self.accounts)
            self._checked_count = 0
            self.status_bar.reset()
            self.status_bar.update_progress(0, len(self.accounts))
            
    def start_checking(self):
        if not self.accounts:
            self.toolbar.reset_buttons()
            return
        
        # Chỉ check những acc chưa check
        unchecked = [a for a in self.accounts if a.status == AccountStatus.UNCHECKED]
        if not unchecked:
            # Tất cả đã check, hỏi có muốn check lại không
            self._checked_count = 0
            for a in self.accounts:
                a.status = AccountStatus.UNCHECKED
                a.heroes_count = 0
                a.skins_count = 0
                a.gold = 0
                a.military_medals = 0
                a.rank = None
                a.credibility_score = 0
                a.security = SecurityInfo.NONE
            self.account_table.refresh_table()
            unchecked = self.accounts
        
        self.stop_event.clear()
        self.pause_event.set()
        
        self.check_thread = threading.Thread(
            target=self._check_worker, args=(unchecked,), daemon=True
        )
        self.check_thread.start()
        
    def pause_checking(self):
        self.pause_event.clear()
        
    def resume_checking(self):
        self.pause_event.set()
        
    def stop_checking(self):
        self.stop_event.set()
        self.pause_event.set()  # Unblock if paused so thread can exit
        
    def export_live(self):
        file_path = filedialog.asksaveasfilename(
            title="Lưu file Live",
            defaultextension=".txt",
            initialfile="live_accounts.txt",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if file_path:
            export_live_accounts(self.accounts, file_path)
            
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            title="Lưu file báo cáo CSV",
            defaultextension=".csv",
            initialfile="report.csv",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if file_path:
            export_report_csv(self.accounts, file_path)
            
    def on_filter_changed(self):
        status_filter, search_text = self.filter_bar.get_filter()
        self.account_table.refresh_table(status_filter, search_text)
        
    def change_delay(self, val):
        self.engine.delay = float(val)
        
    def _update_stats(self):
        live = sum(1 for a in self.accounts if a.status == AccountStatus.LIVE)
        ban = sum(1 for a in self.accounts if a.status == AccountStatus.BANNED)
        wrong = sum(1 for a in self.accounts if a.status == AccountStatus.WRONG_PASSWORD)
        captcha = sum(1 for a in self.accounts if a.status == AccountStatus.CAPTCHA)
        self.status_bar.update_progress(self._checked_count, len(self.accounts))
        self.status_bar.update_stats(live, ban, wrong, captcha)
        
    def _save_current_state(self):
        """Lưu trạng thái hiện tại ra file JSON."""
        if self.current_filepath and self.accounts:
            try:
                save_state(self.accounts, self.current_filepath)
            except Exception:
                pass  # Silent fail on save
        
    def _check_worker(self, accounts_to_check: List[Account]):
        self.engine.check_accounts(
            accounts=accounts_to_check,
            callback=self._on_account_checked,
            stop_event=self.stop_event,
            pause_event=self.pause_event
        )
        self.after(0, self._on_check_complete)
        
    def _on_account_checked(self, acc: Account, result: CheckResult):
        """Called from check thread — must use after() to update GUI."""
        self.after(0, self._update_gui_after_check, acc)
        
    def _update_gui_after_check(self, acc: Account):
        self._checked_count += 1
        self.account_table.update_account(acc)
        self._update_stats()
        
        # Auto-save mỗi 5 acc hoặc khi check xong
        if self._checked_count % 5 == 0:
            self._save_current_state()
        
    def _on_check_complete(self):
        """Called when all accounts have been checked or stopped."""
        self.toolbar.reset_buttons()
        self._update_stats()
        self._save_current_state()  # Lưu khi check xong
        
    def _recheck_single(self, acc: Account):
        """Re-check a single account in a background thread."""
        def _worker():
            result = self.engine.check(acc)
            acc.status = result.status
            acc.security = result.security
            acc.heroes_count = result.heroes_count
            acc.skins_count = result.skins_count
            acc.gold = result.gold
            acc.military_medals = result.military_medals
            acc.rank = result.rank
            acc.credibility_score = result.credibility_score
            self.after(0, self._update_gui_after_check, acc)
        
        threading.Thread(target=_worker, daemon=True).start()
        
    def _on_close(self):
        """Xử lý khi đóng app — lưu state trước khi thoát."""
        # Dừng check nếu đang chạy
        self.stop_event.set()
        self.pause_event.set()
        
        # Lưu state
        self._save_current_state()
        
        self.destroy()
