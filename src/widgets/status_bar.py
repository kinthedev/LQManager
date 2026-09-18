import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=40, **kwargs)
        
        self.current = 0
        self.total = 0
        
        self.progress_bar = ctk.CTkProgressBar(self, width=400)
        self.progress_bar.pack(side="left", padx=20, pady=10)
        self.progress_bar.set(0)
        
        self.stats_label = ctk.CTkLabel(self, text="Đã check 0/0 | Live: 0 | Ban: 0 | Sai MK: 0 | Captcha: 0", font=("Arial", 12))
        self.stats_label.pack(side="right", padx=20, pady=10)
        
    def update_progress(self, current: int, total: int):
        self.current = current
        self.total = total
        if total > 0:
            self.progress_bar.set(current / total)
        else:
            self.progress_bar.set(0)
            
    def update_stats(self, live: int, ban: int, wrong: int, captcha: int):
        self.stats_label.configure(text=f"Đã check {self.current}/{self.total} | Live: {live} | Ban: {ban} | Sai MK: {wrong} | Captcha: {captcha}")
        
    def reset(self):
        self.current = 0
        self.total = 0
        self.progress_bar.set(0)
        self.stats_label.configure(text="Đã check 0/0 | Live: 0 | Ban: 0 | Sai MK: 0 | Captcha: 0")
