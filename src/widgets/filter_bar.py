import customtkinter as ctk
from typing import Callable, Optional

class FilterBar(ctk.CTkFrame):
    def __init__(self, master, on_filter_changed: Optional[Callable] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_filter_changed_callback = on_filter_changed
        
        self.status_var = ctk.StringVar(value="Tất cả")
        self.search_var = ctk.StringVar(value="")
        
        self.status_combo = ctk.CTkComboBox(
            self, 
            values=['Tất cả', 'Chỉ nick Live', 'Chỉ nick Ban', 'Sai mật khẩu', 'Trắng thông tin', 'Kẹt Captcha'],
            variable=self.status_var,
            command=self._on_change
        )
        self.status_combo.pack(side="left", padx=10, pady=10)
        
        self.search_entry = ctk.CTkEntry(
            self, 
            placeholder_text="Tìm kiếm theo tài khoản...",
            textvariable=self.search_var,
            width=250
        )
        self.search_entry.pack(side="left", padx=10, pady=10)
        self.search_entry.bind("<KeyRelease>", self._on_change)
        
    def _on_change(self, *args):
        if self.on_filter_changed_callback:
            self.on_filter_changed_callback()
            
    def get_filter(self) -> tuple[str, str]:
        return (self.status_var.get(), self.search_var.get())
