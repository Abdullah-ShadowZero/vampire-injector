"""
modal_options.py - Advanced Stealth & Evasion Options Modal
"""

import customtkinter as ctk


class OptionsModal(ctk.CTkToplevel):
    def __init__(self, master, lang="en"):
        super().__init__(master)
        self.geometry("500x420")
        self.title("Advanced Stealth & Evasion Options")
        self.configure(fg_color="#0f0f0f")
        self.resizable(False, False)
        self.lang = lang

        self._build_ui()
        self._update_language()

    def _build_ui(self):
        """بناء واجهة الخيارات"""
        
        self.lbl_title = ctk.CTkLabel(self, text="🛡️ Stealth & Evasion Configuration", 
                                     font=("Consolas", 16, "bold"), text_color="#FF1E1E")
        self.lbl_title.pack(pady=15)

        ctk.CTkFrame(self, height=2, fg_color="#8B0000").pack(fill="x", padx=20, pady=5)

        self.chk_av = ctk.CTkCheckBox(self, text="🛡️ Disable AV / AMSI Bypass covertly", 
                                     fg_color="#8B0000")
        self.chk_av.pack(anchor="w", padx=30, pady=8)
        self.chk_av.select()

        self.chk_persist = ctk.CTkCheckBox(self, text="🔄 Ensure Persistence via Registry / Tasks", 
                                          fg_color="#8B0000")
        self.chk_persist.pack(anchor="w", padx=30, pady=8)
        self.chk_persist.select()

        self.chk_sandbox = ctk.CTkCheckBox(self, text="🖥️ Anti-VM & Sandbox Evasion Detection", 
                                          fg_color="#8B0000")
        self.chk_sandbox.pack(anchor="w", padx=30, pady=8)
        self.chk_sandbox.select()

        self.chk_debug = ctk.CTkCheckBox(self, text="🐛 Anti-Debugging (Detect Debuggers)", 
                                        fg_color="#8B0000")
        self.chk_debug.pack(anchor="w", padx=30, pady=8)
        self.chk_debug.select()

        self.chk_hide_process = ctk.CTkCheckBox(self, text="👻 Hide Process from Task Manager", 
                                               fg_color="#8B0000")
        self.chk_hide_process.pack(anchor="w", padx=30, pady=8)
        self.chk_hide_process.select()

        self.chk_traffic = ctk.CTkCheckBox(self, text="🌐 Traffic Obfuscation (Mimic Normal Traffic)", 
                                          fg_color="#8B0000")
        self.chk_traffic.pack(anchor="w", padx=30, pady=8)
        self.chk_traffic.select()

        ctk.CTkFrame(self, height=2, fg_color="#8B0000").pack(fill="x", padx=20, pady=10)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=10)

        ctk.CTkButton(btn_frame, text="💾 Save & Apply", 
                     fg_color="#8B0000", hover_color="#b30000",
                     command=self.save_and_close).pack(side="left", padx=5, fill="x", expand=True)
        
        ctk.CTkButton(btn_frame, text="❌ Cancel", 
                     fg_color="#1a0000", hover_color="#660000",
                     command=self.destroy).pack(side="right", padx=5, fill="x", expand=True)

        self.lbl_info = ctk.CTkLabel(self, 
            text="⚙️ These settings will be applied to future injections",
            font=("Consolas", 10), text_color="#666666")
        self.lbl_info.pack(pady=5)

    def save_and_close(self):
        if hasattr(self.master, 'stealth_options'):
            self.master.stealth_options.update({
                'disable_av': self.chk_av.get() == 1,
                'persistence': self.chk_persist.get() == 1,
                'anti_sandbox': self.chk_sandbox.get() == 1,
                'anti_debug': self.chk_debug.get() == 1,
                'process_hiding': self.chk_hide_process.get() == 1,
                'traffic_obfuscation': self.chk_traffic.get() == 1
            })
        self.destroy()

    def _update_language(self):
        if self.lang == "ar":
            self.title("خيارات التخفي والتهرب المتقدمة")
            self.lbl_title.configure(text="🛡️ إعدادات التخفي والتهرب")
            self.chk_av.configure(text="🛡️ تعطيل برامج الحماية و AMSI بشكل مخفي")
            self.chk_persist.configure(text="🔄 ضمان الاستمرارية عبر الريجستري والمهام المجدولة")
            self.chk_sandbox.configure(text="🖥️ كشف البيئات الافتراضية وصناديق التحليل")
            self.chk_debug.configure(text="🐛 كشف أدوات التصحيح (Anti-Debugging)")
            self.chk_hide_process.configure(text="👻 إخفاء العملية من إدارة المهام")
            self.chk_traffic.configure(text="🌐 تشويش حركة الشبكة لتشبه المرور العادي")
            self.lbl_info.configure(text="⚙️ سيتم تطبيق هذه الإعدادات على عمليات الحقن المستقبلية")
            
            for child in self.winfo_children():
                if isinstance(child, ctk.CTkFrame):
                    for btn in child.winfo_children():
                        if isinstance(btn, ctk.CTkButton):
                            if "Save" in btn.cget("text") or "حفظ" in btn.cget("text"):
                                btn.configure(text="💾 حفظ وتطبيق")
                            elif "Cancel" in btn.cget("text") or "إلغاء" in btn.cget("text"):
                                btn.configure(text="❌ إلغاء")