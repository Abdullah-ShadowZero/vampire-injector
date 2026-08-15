"""
tab_usb.py - USB Auto-Run Infector Tab
Educational simulation for USB drive infection
"""

import customtkinter as ctk
from tkinter import messagebox
import os
import platform


class USBInfectorTab(ctk.CTkFrame):
    def __init__(self, master, lang_callback):
        super().__init__(master, fg_color="#0f0f0f")
        self.lang_callback = lang_callback
        self.current_lang = "en"
        self.detected_drives = []

        self._build_ui()
        self._refresh_drives()

    def _build_ui(self):
        """بناء واجهة تبويب الفلاشات"""
        
        self.frame = ctk.CTkFrame(self, fg_color="#141414", border_color="#8B0000", border_width=2, corner_radius=10)
        self.frame.pack(fill="both", expand=True, padx=15, pady=15)

        self.lbl_title = ctk.CTkLabel(self.frame, text="🔌 USB Auto-Run & Spread Infector", 
                                     font=("Consolas", 14, "bold"), text_color="#FF1E1E")
        self.lbl_title.pack(pady=15)

        self.lbl_desc = ctk.CTkLabel(self.frame, 
            text="Automatically detects connected flash drives, generates hidden autorun scripts,\nand propagates payloads instantly without user interaction.",
            text_color="#cccccc")
        self.lbl_desc.pack(pady=5)

        self.drive_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.drive_frame.pack(fill="x", padx=30, pady=10)

        self.lbl_drives = ctk.CTkLabel(self.drive_frame, text="📀 Detected USB Drives:", 
                                      font=("Consolas", 11), text_color="white")
        self.lbl_drives.pack(anchor="w")

        self.drive_list = ctk.CTkComboBox(self.drive_frame, values=["No drives detected"],
                                         fg_color="#0a0000", border_color="#8B0000")
        self.drive_list.pack(fill="x", pady=5)

        self.btn_refresh = ctk.CTkButton(self.frame, text="🔄 Refresh Drives",
                                        fg_color="#1a0000", hover_color="#8B0000",
                                        command=self._refresh_drives)
        self.btn_refresh.pack(pady=5)

        self.chk_autorun = ctk.CTkCheckBox(self.frame, text="Generate hidden autorun.inf & LNK hijacking stub", 
                                          fg_color="#8B0000")
        self.chk_autorun.pack(anchor="w", padx=30, pady=10)
        self.chk_autorun.select()

        self.chk_hide = ctk.CTkCheckBox(self.frame, text="Apply Hidden + System attributes to payloads", 
                                       fg_color="#8B0000")
        self.chk_hide.pack(anchor="w", padx=30, pady=10)
        self.chk_hide.select()
        
        self.chk_spread = ctk.CTkCheckBox(self.frame, text="Enable auto-spread to all connected drives", 
                                         fg_color="#8B0000")
        self.chk_spread.pack(anchor="w", padx=30, pady=10)
        self.chk_spread.select()

        self.btn_inject = ctk.CTkButton(self.frame, text="🧛 Infect & Prepare Connected Drive",
                                       fg_color="#8B0000", hover_color="#b30000",
                                       command=self.infect_usb)
        self.btn_inject.pack(fill="x", padx=30, pady=30)

        self.lbl_status = ctk.CTkLabel(self.frame, text="Status: Ready", 
                                      font=("Consolas", 10), text_color="#666666")
        self.lbl_status.pack(pady=5)

    def _refresh_drives(self):
        """تحديث قائمة الفلاشات المتصلة"""
        try:
            self.detected_drives = self._get_removable_drives()
            
            if self.detected_drives:
                self.drive_list.configure(values=self.detected_drives)
                self.drive_list.set(self.detected_drives[0])
                self.lbl_status.configure(text=f"Status: {len(self.detected_drives)} drive(s) detected", 
                                         text_color="#00FF00")
            else:
                self.drive_list.configure(values=["No drives detected"])
                self.drive_list.set("No drives detected")
                self.lbl_status.configure(text="Status: No removable drives found", 
                                         text_color="#FF4444")
        except Exception as e:
            self.lbl_status.configure(text=f"Error: {str(e)}", text_color="#FF4444")

    def _get_removable_drives(self):
        """الحصول على قائمة الفلاشات المتصلة"""
        drives = []
        if platform.system() == "Windows":
            try:
                import win32file
                import win32api
                for drive in win32api.GetLogicalDriveStrings().split('\x00')[:-1]:
                    if win32file.GetDriveType(drive) == win32file.DRIVE_REMOVABLE:
                        drives.append(drive)
            except:
                for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                    drive = f"{letter}:\\"
                    if os.path.exists(drive) and os.path.isdir(drive):
                        drives.append(drive)
        else:
            drives = ["/mnt/usb", "/media/usb"]
        return drives

    def infect_usb(self):
        """محاكاة حقن الفلاشة"""
        selected = self.drive_list.get()
        
        if "No drives" in selected or not selected:
            messagebox.showwarning("Warning", "Please select a valid USB drive!")
            return
        
        self.lbl_status.configure(text="🔄 Infecting drive...", text_color="#FFA500")
        
        import time
        time.sleep(1)
        
        self.lbl_status.configure(text="✅ Drive infected successfully!", text_color="#00FF00")
        
        messagebox.showinfo("USB Injection Success", f"""🧛 USB Drive Successfully Infected!

Drive: {selected}
Autorun: {'Enabled' if self.chk_autorun.get() == 1 else 'Disabled'}
Hide Files: {'Yes' if self.chk_hide.get() == 1 else 'No'}
Auto-Spread: {'Yes' if self.chk_spread.get() == 1 else 'No'}

✅ The drive is now configured for auto-execution.

⚠️ Educational simulation only.
No actual USB infection occurred.""")

    def update_language(self, lang):
        """تحديث اللغة"""
        self.current_lang = lang
        
        if lang == "ar":
            self.lbl_title.configure(text="🔌 حقن الفلاشات والانتشار التلقائي")
            self.lbl_desc.configure(text="يكتشف تلقائياً الفلاشات المتصلة، ويولد نصوص تشغيل تلقائي مخفية،\nوينشر البايلودات فوراً دون تدخل المستخدم.")
            self.lbl_drives.configure(text="📀 الفلاشات المتصلة:")
            self.btn_refresh.configure(text="🔄 تحديث الفلاشات")
            self.chk_autorun.configure(text="توليد ملف autorun.inf مخفي وتقنية اختطاف LNK")
            self.chk_hide.configure(text="تطبيق سمات مخفي + نظام على البايلودات")
            self.chk_spread.configure(text="تفعيل الانتشار التلقائي لجميع الفلاشات المتصلة")
            self.btn_inject.configure(text="🧛 حقن وتجهيز الفلاشة المتصلة")
        else:
            self.lbl_title.configure(text="🔌 USB Auto-Run & Spread Infector")
            self.lbl_desc.configure(text="Automatically detects connected flash drives, generates hidden autorun scripts,\nand propagates payloads instantly without user interaction.")
            self.lbl_drives.configure(text="📀 Detected USB Drives:")
            self.btn_refresh.configure(text="🔄 Refresh Drives")
            self.chk_autorun.configure(text="Generate hidden autorun.inf & LNK hijacking stub")
            self.chk_hide.configure(text="Apply Hidden + System attributes to payloads")
            self.chk_spread.configure(text="Enable auto-spread to all connected drives")
            self.btn_inject.configure(text="🧛 Infect & Prepare Connected Drive")