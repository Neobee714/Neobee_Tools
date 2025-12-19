# HTTP Login Brute-Force Tool 🛡️

[🇨🇳 中文说明 (Chinese)](#-中文说明-chinese-documentation) | [🇺🇸 English Docs](#-english-documentation)

**A multi-threaded HTTP login brute-force tool integrated into the Neobee_Tools suite.** This tool is designed for security professionals and researchers to test the strength of credentials on web applications via HTTP/HTTPS.

> ⚠️ **DISCLAIMER**: This tool is strictly for **educational purposes** and **authorized security testing only**. Do not use it for illegal activities. The author is not responsible for any misuse or damage caused by this tool.

---

## 🇺🇸 English Documentation

### 🚀 Features
- 🧵 **Multi-threaded**: High-speed brute-forcing using `ThreadPoolExecutor`.
- 🔄 **Dual Attack Modes**:
  - `USER` Mode: Locks one user, tries all passwords (avoids account lockouts).
  - `PASS` Mode: Locks one password, tries all users (Credential Stuffing).
- 🛠 **Highly Customizable**:
  - Supports custom HTTP Methods (POST/GET/PUT).
  - Custom Headers (User-Agent, Cookies, etc.).
  - Flexible Payload Templates.
- 🛑 **Smart Stop**: Automatically stops all threads once credentials are found.

### 📦 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Neobee714/Neobee_Tools.git
   cd Neobee_Tools

```

2. Install dependencies:
```bash
pip install requests

```



### 📖 Usage

**Command Format:**

```bash
python brute.py [options]

```

| Argument | Description | Example |
| --- | --- | --- |
| `-u`, `--url` | Target URL | `http://target.com/login` |
| `-P`, `--passfile` | Password dictionary file | `passwords.txt` |
| `-U`, `--userfile` | Username dictionary file | `users.txt` |
| `-n`, `--username` | Single username target | `admin` |
| `-d`, `--data` | POST data template | `"user=~USER~&pass=~PASS~"` |
| `-t`, `--threads` | Number of threads (Default: 40) | `50` |
| `-M`, `--Mode` | Attack Mode (USER/PASS) | `USER` |

> **Note**: Use `~USER~` and `~PASS~` as placeholders in the `-d` argument.

### ⚡ Examples

**1. Single User Attack:**

```bash
python brute.py -u http://target.com/login -n admin -P pass.txt -d "username=~USER~&password=~PASS~"

```

**2. User List with Custom Cookie:**

```bash
python brute.py -u http://target.com/api/auth -U users.txt -P pass.txt -d "u=~USER~&p=~PASS~" -H "Cookie: session=123"

```

---

## 🇨🇳 中文说明 (Chinese Documentation)

一个基于 Python 的多线程 HTTP 登录暴力破解工具，集成在 **Neobee_Tools** 工具集中。支持多种 HTTP 方法、自定义 Headers 以及两种不同的破解模式。

> ⚠️ **注意**：本工具仅供**网络安全学习**和**经授权的渗透测试**使用。严禁用于非法用途。开发者不对因使用本工具造成的任何直接或间接损失负责。

### 🚀 功能特点

* 🧵 **多线程支持**：使用 `ThreadPoolExecutor` 加快破解速度。
* 🔄 **双模式 (Attack Modes)**：
* `USER` 模式：锁定一个用户，尝试所有密码（减少被封号风险）。
* `PASS` 模式：锁定一个密码，尝试所有用户（常见于“撞库”攻击）。


* 🛠 **高度自定义**：
* 支持自定义 HTTP 请求方法 (POST/GET/PUT)。
* 支持自定义 HTTP Headers (Cookie, User-Agent 等)。
* 灵活的 Payload 模板配置。


* 🛑 **智能停止**：一旦找到正确密码，所有线程自动停止。

### 📦 安装与使用

**安装依赖：**

```bash
pip install requests

```

**参数说明：**

| 参数 | 说明 | 示例 |
| --- | --- | --- |
| `-u`, `--url` | 目标 URL 地址 | `http://example.com/login.php` |
| `-P`, `--passfile` | 密码字典路径 | `passwords.txt` |
| `-U`, `--userfile` | 用户名字典路径 | `users.txt` |
| `-n`, `--username` | 单个用户名 | `admin` |
| `-d`, `--data` | POST 数据模板 | `"user=~USER~&pass=~PASS~"` |
| `-t`, `--threads` | 线程数量 (默认 40) | `50` |
| `-M`, `--Mode` | 攻击模式 (USER/PASS) | `USER` |

**运行示例：**

```bash
# 针对 admin 用户进行破解
python brute.py -u http://target.com/login -n admin -P pass.txt -d "username=~USER~&password=~PASS~"

```

---

### ⚖️ Legal & Disclaimer (免责声明)

**English**:

The developer of this tool is not responsible for any damage caused by the misuse of this tool. Use strictly for educational purposes and authorized security testing.

**中文**:

本工具仅限于安全研究与教学用途。用户在使用前必须获得目标系统的授权。如因非法使用导致任何法律后果，由用户自行承担。

---

Developed by [Neobee714](https://www.google.com/search?q=https://github.com/Neobee714)
