# 🔴 REAPERSCAN GOD EDITION

Ultimate Vulnerability Scanner - Web + Cloud + Infrastructure
100+ Vulnerability Types • 1100+ Payloads • Full Takeover Capable


## 🚀 FITUR UTAMA

🌐 WEB
- SQL Injection (Boolean, Time, Union, Error, Stacked, Second Order)
- XSS (Reflected, Stored, DOM, Blind, Mutation)
- LFI (Local File Inclusion)
- RFI (Remote File Inclusion)
- RCE (Remote Code Execution)
- SSTI (Server-Side Template Injection)
- XXE (XML External Entity)
- SSRF (Server-Side Request Forgery)
- CSRF (Cross-Site Request Forgery)
- IDOR (Insecure Direct Object Reference)
- Open Redirect
- File Upload Bypass
- GraphQL Introspection
- REST API Misconfiguration
- LDAP Injection
- XPath Injection
- Host Header Injection
- CRLF Injection
- HTTP Request Smuggling
- NoSQL Injection
- Directory Listing
- Admin Panel Detection
- Sensitive Files (.env, .git, .ssh, dll)

☁️ CLOUD
- AWS Metadata (IAM Credentials)
- GCP Metadata (Service Account)
- Azure Metadata (Instance Info)
- Public S3 Buckets
- Cloud Keys (.aws/credentials, .gcp/credentials)
- Terraform State File
- Kubernetes API Exposure
- Docker API Exposure

🖥️ INFRASTRUCTURE
- Port Scanning (30+ ports)
- SSH Weak Credentials
- FTP Anonymous Login
- SMB Share Access
- SNMP Community Strings
- Default Credentials (admin:admin, root:toor, dll)
- Service Detection

🔥 EXTRA
- Auto Exploit
- Multi-threading
- Proxy Support
- Cookie Support
- JSON/HTML Report
- Bypass WAF
- Payload Rotator


## 📦 INSTALLASI

### 1. Clone Repository
git clone https://github.com/g0d150ne/reaper-god.git
cd reaper-god

### 2. Install Dependencies
pip install requests colorama paramiko ftplib

### 3. Jalankan
python3 reaper_god_main.py -u https://target.com -p "id=1" --all

---

## 🛠️ CARA PENGGUNAAN

### Basic Scan
python3 reaper_god_main.py -u "https://target.com/page.php?id=1" -p "id=1"

### Dengan Cloud Scan (AWS/GCP/Azure)
python3 reaper_god_main.py -u "https://target.com/page.php?id=1" -p "id=1" --cloud

### Dengan Infra Scan (Port, SSH, FTP, SMB)
python3 reaper_god_main.py -u "https://target.com/page.php?id=1" -p "id=1" --infra

### FULL SCAN (Semua Fitur)
python3 reaper_god_main.py -u "https://target.com/page.php?id=1" -p "id=1" --all

### Dengan Proxy
python3 reaper_god_main.py -u "https://target.com/page.php?id=1" -p "id=1" --all --proxy http://127.0.0.1:8080

### Dengan Cookies
python3 reaper_god_main.py -u "https://target.com/admin.php" -c "PHPSESSID=abc123; token=xyz789" --all

### Custom Threads
python3 reaper_god_main.py -u "https://target.com/page.php?id=1" -p "id=1" --all -t 50


## 📊 HASIL SCAN

### Output Files:
- reaper_god_report.json → Format JSON (mudah diparsing)
- reaper_god_report.html → Format HTML (visual rapi)

### Contoh Output JSON:
{
  "id": 1,
  "category": "Web",
  "url": "https://target.com/page.php",
  "parameter": "id",
  "type": "SQL Injection",
  "payload": "' OR '1'='1' -- -",
  "severity": "Critical",
  "evidence": "Content difference detected",
  "timestamp": "2024-01-15 14:30:22"
}


## 📁 STRUKTUR FILE

reaper-god/
├── reaper_god_main.py          # Scanner utama (500+ baris)
├── reaper_god_payloads.py      # Semua payload (400+ baris)
├── README.md                   # Dokumentasi ini
└── requirements.txt            # Dependencies


## ⚙️ KONFIGURASI

Edit reaper_god_payloads.py untuk mengubah:

THREADS = 20              # Jumlah thread default
TIMEOUT = 15              # Timeout request (detik)
DELAY_MIN = 1             # Delay minimal antar request
DELAY_MAX = 3             # Delay maksimal antar request
C2_SERVER = "https://your-c2-server.com"  # Server untuk reverse shell
BACKDOOR_PORT = 4444      # Port untuk backdoor
PROXIES = []              # Daftar proxy (opsional)


## 🎯 PAYLOAD LENGKAP

Kategori           | Jumlah Payload
-------------------|---------------
SQL Injection      | 80+
XSS                | 60+
LFI                | 50+
RFI                | 20+
RCE                | 30+
SSTI               | 15+
XXE                | 10+
SSRF               | 15+
Cloud Metadata     | 20+
Lain-lain          | 800+
TOTAL              | 1100+


## 🔧 DEPENDENCIES

requests>=2.28.0
colorama>=0.4.6
paramiko>=2.12.0
ftplib>=1.0.1
urllib3>=1.26.0


## ⚠️ DISCLAIMER

Tools ini dibuat untuk tujuan educational dan authorized testing ONLY.

- Hanya gunakan di server yang Anda miliki atau sudah mendapat izin
- Segala penyalahgunaan menjadi tanggung jawab pengguna
- Penulis tidak bertanggung jawab atas kerusakan atau kerugian yang timbul


## 📌 UPDATE LOG

### v3.0 (2024)
- Tambah Cloud Scanner (AWS/GCP/Azure)
- Tambah Infrastructure Scanner
- Tambah 500+ payload baru
- Optimasi multi-threading
- Fix bug bypass WAF
- Tambah report HTML

### v2.0 (2023)
- Tambah Auto Exploit
- Tambah Reverse Shell
- Tambah Webshell Upload

### v1.0 (2022)
- Web Scanner Dasar
- SQLi, XSS, LFI, RFI


## 📞 KONTAK

GitHub: https://github.com/g0d150ne
Telegram: @G0D150NE


Made with ❤️ by G0D150NE
"Dengan kekuatan besar, datang tanggung jawab besar"
