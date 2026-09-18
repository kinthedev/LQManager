import customtkinter as ctk
from typing import Callable, Optional

class Toolbar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Buttons
        self.btn_open = ctk.CTkButton(self, text="📂 Chọn File", command=self._on_open, width=120)
        self.btn_open.pack(side="left", padx=5, pady=10)
        
        self.btn_start = ctk.CTkButton(self, text="▶ Bắt đầu Kiểm tra", fg_color="green", hover_color="darkgreen", command=self._on_start, width=150)
        self.btn_start.pack(side="left", padx=5, pady=10)
        
        self.btn_pause = ctk.CTkButton(self, text="⏸ Tạm dừng", fg_color="#B8860B", hover_color="#8B6508", command=self._on_pause, width=120)
        self.btn_pause.pack(side="left", padx=5, pady=10)
        self.btn_pause.configure(state="disabled")
        
        self.btn_stop = ctk.CTkButton(self, text="⏹ Dừng", fg_color="red", hover_color="darkred", command=self._on_stop, width=100)
        self.btn_stop.pack(side="left", padx=5, pady=10)
        self.btn_stop.configure(state="disabled")
        
        self.btn_export_live = ctk.CTkButton(self, text="💾 Xuất Live", command=self._on_export_live, width=120)
        self.btn_export_live.pack(side="left", padx=5, pady=10)
        
        self.btn_export_csv = ctk.CTkButton(self, text="📊 Xuất CSV", command=self._on_export_csv, width=120)
        self.btn_export_csv.pack(side="left", padx=5, pady=10)
        
        # Delay slider
        self.delay_var = ctk.DoubleVar(value=2)
        
        self.delay_label = ctk.CTkLabel(self, text="Delay: 2s")
        self.delay_label.pack(side="left", padx=(15, 5), pady=10)
        
        self.delay_slider = ctk.CTkSlider(self, from_=1, to=10, number_of_steps=9, variable=self.delay_var, command=self._on_delay_change, width=120)
        self.delay_slider.pack(side="left", padx=5, pady=10)
        
        self.callbacks = {}
        self.is_paused = False

    def set_callbacks(self, on_open=None, on_start=None, on_pause=None, on_resume=None, on_stop=None, on_export_live=None, on_export_csv=None, on_delay_change=None):
        self.callbacks['on_open'] = on_open
        self.callbacks['on_start'] = on_start
        self.callbacks['on_pause'] = on_pause
        self.callbacks['on_resume'] = on_resume
        self.callbacks['on_stop'] = on_stop
        self.callbacks['on_export_live'] = on_export_live
        self.callbacks['on_export_csv'] = on_export_csv
        self.callbacks['on_delay_change'] = on_delay_change

    def _on_open(self):
        if self.callbacks.get('on_open'): self.callbacks['on_open']()
        
    def _on_start(self):
        self.btn_start.configure(state="disabled")
        self.btn_pause.configure(state="normal", text="⏸ Tạm dừng", fg_color="#B8860B")
        self.btn_stop.configure(state="normal")
        self.btn_open.configure(state="disabled")
        self.is_paused = False
        if self.callbacks.get('on_start'): self.callbacks['on_start']()
        
    def _on_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_pause.configure(text="▶ Tiếp tục", fg_color="green")
            if self.callbacks.get('on_pause'): self.callbacks['on_pause']()
        else:
            self.btn_pause.configure(text="⏸ Tạm dừng", fg_color="#B8860B")
            if self.callbacks.get('on_resume'): self.callbacks['on_resume']()
            
    def _on_stop(self):
        self.btn_start.configure(state="normal")
        self.btn_pause.configure(state="disabled", text="⏸ Tạm dừng", fg_color="#B8860B")
        self.btn_stop.configure(state="disabled")
        self.btn_open.configure(state="normal")
        self.is_paused = False
        if self.callbacks.get('on_stop'): self.callbacks['on_stop']()
        
    def reset_buttons(self):
        self.btn_start.configure(state="normal")
        self.btn_pause.configure(state="disabled", text="⏸ Tạm dừng", fg_color="#B8860B")
        self.btn_stop.configure(state="disabled")
        self.btn_open.configure(state="normal")
        self.is_paused = False
        
    def _on_export_live(self):
        if self.callbacks.get('on_export_live'): self.callbacks['on_export_live']()
        
    def _on_export_csv(self):
        if self.callbacks.get('on_export_csv'): self.callbacks['on_export_csv']()
        
    def _on_delay_change(self, value):
        val = int(value)
        self.delay_label.configure(text=f"Delay: {val}s")
        if self.callbacks.get('on_delay_change'): self.callbacks['on_delay_change'](val)
