import customtkinter as ctk
import tkinter.ttk as ttk
import tkinter as tk
from typing import List, Optional

from models import Account, AccountStatus, SecurityInfo, RankTier, CheckResult
from utils import copy_to_clipboard, mask_password, format_number

class AccountTable(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.accounts: List[Account] = []
        self.displayed_accounts: List[Account] = []
        self._master = master
        
        # Style Treeview for dark theme
        self.style = ttk.Style()
        self.style.theme_use("default")
        self.style.configure(
            "Treeview",
            background="#2b2b2b",
            foreground="white",
            rowheight=28,
            fieldbackground="#2b2b2b",
            borderwidth=0
        )
        self.style.map('Treeview', background=[('selected', '#1f538d')])
        self.style.configure(
            "Treeview.Heading",
            background="#1f538d",
            foreground="white",
            relief="flat",
            font=("Arial", 10, "bold")
        )
        self.style.map("Treeview.Heading", background=[('active', '#14375e')])

        # Columns
        self.columns = ("STT", "Tài khoản", "Mật khẩu", "Trạng thái", "Bảo mật", "Tướng", "Trang phục", "Vàng", "Quân huy", "Bậc Rank", "Điểm uy tín")
        
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings", selectmode="browse")
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Configure Columns
        col_widths = {
            "STT": 50, "Tài khoản": 150, "Mật khẩu": 120, "Trạng thái": 120, 
            "Bảo mật": 130, "Tướng": 60, "Trang phục": 80, "Vàng": 90, 
            "Quân huy": 90, "Bậc Rank": 100, "Điểm uy tín": 80
        }
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=col_widths.get(col, 100), anchor="center")
            
        # Tags for colors
        self.tree.tag_configure("live", foreground="#90EE90")
        self.tree.tag_configure("wrong", foreground="#FF6B6B")
        self.tree.tag_configure("banned", foreground="#FFA500")
        self.tree.tag_configure("captcha", foreground="#FFFF00")
        self.tree.tag_configure("unchecked", foreground="#AAAAAA")
        
        # Context Menu
        self.context_menu = tk.Menu(self, tearoff=0, bg="#2b2b2b", fg="white")
        self.context_menu.add_command(label="📋 Copy Tài khoản", command=self._copy_username)
        self.context_menu.add_command(label="🔑 Copy Mật khẩu", command=self._copy_password)
        self.context_menu.add_command(label="✏️ Đổi mật khẩu", command=self._change_password)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="🔄 Check lại", command=self._recheck)
        self.context_menu.add_command(label="🗑 Xóa", command=self._delete_account)
        
        self.tree.bind("<Button-3>", self._show_context_menu)
        self.tree.bind("<Double-1>", self._on_double_click)
        
        self.show_passwords = {}  # mapping index to boolean
        
        # Callback for recheck
        self.on_recheck_callback = None

    def load_accounts(self, accounts: List[Account]):
        self.accounts = accounts
        self.show_passwords = {i: False for i in range(len(accounts))}
        self.refresh_table()
        
    def _get_tag_for_status(self, status: AccountStatus) -> str:
        if status == AccountStatus.LIVE:
            return "live"
        elif status == AccountStatus.WRONG_PASSWORD:
            return "wrong"
        elif status == AccountStatus.BANNED:
            return "banned"
        elif status == AccountStatus.CAPTCHA:
            return "captcha"
        return "unchecked"
        
    def _build_row_values(self, i: int, acc: Account) -> tuple:
        pwd_display = acc.password if self.show_passwords.get(i, False) else mask_password(acc.password)
        status_text = acc.status.value if acc.status else "Chưa check"
        sec_text = acc.security.value if acc.security else ""
        rank_text = acc.rank.value if acc.rank else ""
        
        return (
            acc.index,
            acc.username,
            pwd_display,
            status_text,
            sec_text,
            acc.heroes_count if acc.heroes_count else "",
            acc.skins_count if acc.skins_count else "",
            format_number(acc.gold) if acc.gold else "",
            format_number(acc.military_medals) if acc.military_medals else "",
            rank_text,
            acc.credibility_score if acc.credibility_score else ""
        )
        
    def refresh_table(self, status_filter="Tất cả", search_text=""):
        self.tree.delete(*self.tree.get_children())
        self.displayed_accounts = []
        
        for i, acc in enumerate(self.accounts):
            # Filter logic
            if search_text and search_text.lower() not in acc.username.lower():
                continue
                
            if status_filter != "Tất cả":
                if status_filter == "Chỉ nick Live" and acc.status != AccountStatus.LIVE:
                    continue
                if status_filter == "Chỉ nick Ban" and acc.status != AccountStatus.BANNED:
                    continue
                if status_filter == "Sai mật khẩu" and acc.status != AccountStatus.WRONG_PASSWORD:
                    continue
                if status_filter == "Trắng thông tin" and acc.security != SecurityInfo.NONE:
                    continue
                if status_filter == "Kẹt Captcha" and acc.status != AccountStatus.CAPTCHA:
                    continue

            self.displayed_accounts.append(acc)
            values = self._build_row_values(i, acc)
            tag = self._get_tag_for_status(acc.status)
            self.tree.insert("", "end", iid=str(i), values=values, tags=(tag,))
            
    def update_account(self, account: Account):
        """Update a single row in the table after check."""
        try:
            i = self.accounts.index(account)
        except ValueError:
            return
            
        if self.tree.exists(str(i)):
            values = self._build_row_values(i, account)
            tag = self._get_tag_for_status(account.status)
            self.tree.item(str(i), values=values, tags=(tag,))
            # Auto-scroll to updated item
            self.tree.see(str(i))
            
    def _on_double_click(self, event):
        region = self.tree.identify_region(event.x, event.y)
        if region != "cell":
            return
        column = self.tree.identify_column(event.x)
        if column == "#3":  # Password column
            item_id = self.tree.focus()
            if item_id:
                idx = int(item_id)
                self.show_passwords[idx] = not self.show_passwords.get(idx, False)
                self.update_account(self.accounts[idx])
                
    def _show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.context_menu.post(event.x_root, event.y_root)
            
    def _get_selected_account(self) -> Optional[Account]:
        selected = self.tree.selection()
        if selected:
            idx = int(selected[0])
            if idx < len(self.accounts):
                return self.accounts[idx]
        return None
        
    def _copy_username(self):
        acc = self._get_selected_account()
        if acc:
            copy_to_clipboard(self._master, acc.username)
            
    def _copy_password(self):
        acc = self._get_selected_account()
        if acc:
            copy_to_clipboard(self._master, acc.password)
            
    def _change_password(self):
        """Mở dialog đổi mật khẩu cho tài khoản đang chọn."""
        acc = self._get_selected_account()
        if not acc:
            return
        
        # Tạo dialog đổi mật khẩu
        dialog = ctk.CTkToplevel(self._master)
        dialog.title(f"Đổi mật khẩu - {acc.username}")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.grab_set()  # Modal
        dialog.transient(self._master)
        
        # Center dialog
        dialog.update_idletasks()
        x = self._master.winfo_x() + (self._master.winfo_width() // 2) - 200
        y = self._master.winfo_y() + (self._master.winfo_height() // 2) - 100
        dialog.geometry(f"400x200+{x}+{y}")
        
        # Content
        ctk.CTkLabel(dialog, text=f"Tài khoản: {acc.username}", font=("Arial", 13, "bold")).pack(pady=(20, 5))
        ctk.CTkLabel(dialog, text=f"Mật khẩu cũ: {acc.password}", font=("Arial", 12), text_color="#AAAAAA").pack(pady=(0, 10))
        
        new_pass_entry = ctk.CTkEntry(dialog, placeholder_text="Nhập mật khẩu mới...", width=300, show="")
        new_pass_entry.pack(pady=5)
        new_pass_entry.focus_set()
        
        def apply_change():
            new_pass = new_pass_entry.get().strip()
            if new_pass:
                acc.password = new_pass
                self.update_account(acc)
            dialog.destroy()
        
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=15)
        ctk.CTkButton(btn_frame, text="✅ Xác nhận", fg_color="green", hover_color="darkgreen", command=apply_change, width=120).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Hủy", fg_color="gray", hover_color="darkgray", command=dialog.destroy, width=120).pack(side="left", padx=10)
        
        # Enter key to confirm
        new_pass_entry.bind("<Return>", lambda e: apply_change())
            
    def _recheck(self):
        acc = self._get_selected_account()
        if acc and self.on_recheck_callback:
            self.on_recheck_callback(acc)
            
    def _delete_account(self):
        selected = self.tree.selection()
        if selected:
            idx = int(selected[0])
            if idx < len(self.accounts):
                self.accounts.pop(idx)
                # Re-index remaining accounts
                for j, a in enumerate(self.accounts):
                    a.index = j + 1
                self.show_passwords = {i: False for i in range(len(self.accounts))}
                self.refresh_table()

    def get_filtered_accounts(self, status_filter: str, search_text: str) -> List[Account]:
        res = []
        for acc in self.accounts:
            if search_text and search_text.lower() not in acc.username.lower():
                continue
            if status_filter != "Tất cả":
                if status_filter == "Chỉ nick Live" and acc.status != AccountStatus.LIVE:
                    continue
                if status_filter == "Chỉ nick Ban" and acc.status != AccountStatus.BANNED:
                    continue
                if status_filter == "Sai mật khẩu" and acc.status != AccountStatus.WRONG_PASSWORD:
                    continue
                if status_filter == "Trắng thông tin" and acc.security != SecurityInfo.NONE:
                    continue
                if status_filter == "Kẹt Captcha" and acc.status != AccountStatus.CAPTCHA:
                    continue
            res.append(acc)
        return res
        
    def get_all_accounts(self) -> List[Account]:
        return self.accounts
