# HTTP Login Brute-Force Tool 🛡️

一个基于 Python 的多线程 HTTP 登录暴力破解工具。集成在 Neobee_Tools 工具集中，支持多种 HTTP 方法（GET/POST）、自定义 Headers、以及两种不同的破解模式。

> ⚠️ **注意**：本工具仅供网络安全学习和经授权的渗透测试使用。严禁用于非法用途。

## 🚀 功能特点 (Features)

- 🧵 **多线程支持**：使用 `ThreadPoolExecutor` 加快破解速度。
- 🔄 **双模式 (Attack Modes)**：
  - `USER` 模式：锁定一个用户，尝试所有密码（减少被封号风险）。
  - `PASS` 模式：锁定一个密码，尝试所有用户（“撞库”常用）。
- 🛠 **高度自定义**：
  - 支持自定义 HTTP 请求方法 (POST/GET/PUT)。
  - 支持自定义 HTTP Headers (Cookie, User-Agent 等)。
  - 灵活的 Payload 模板配置。
- 🛑 **智能停止**：一旦找到正确密码，所有线程自动停止。

## 📦 安装 (Installation)

1. 克隆仓库：
```bash
git clone https://github.com/Neobee714/Neobee_Tools.git
cd Neobee_Tools

```

2. 安装依赖：
```bash
pip install requests

```



## 📖 使用方法 (Usage)

假设你的脚本文件名为 `brute.py` (如果你的文件名不同，请替换命令中的文件名)：

### 参数说明

| 参数 | 说明 | 示例 |
| --- | --- | --- |
| `-u`, `--url` | 目标 URL 地址 | `http://example.com/login.php` |
| `-P`, `--passfile` | 密码字典路径 | `passwords.txt` |
| `-U`, `--userfile` | 用户名字典路径 | `users.txt` |
| `-n`, `--username` | 单个用户名 | `admin` |
| `-d`, `--data` | POST 数据模板 | `"user=~USER~&pass=~PASS~"` |
| `-t`, `--threads` | 线程数量 (默认 40) | `50` |
| `-M`, `--Mode` | 攻击模式 (USER/PASS) | `USER` |

### ⚡ 运行示例

#### 1. 针对单个用户 (admin) 进行破解

```bash
python brute.py -u http://target.com/login -n admin -P pass.txt -d "username=~USER~&password=~PASS~"

```

#### 2. 使用用户列表和自定义 Header

```bash
python brute.py -u http://target.com/api/auth -U users.txt -P pass.txt -d "u=~USER~&p=~PASS~" -H "Cookie: session=123"

```

#### 3. 指定线程数和攻击模式

```bash
python brute.py -u http://target.com/login -n admin -P pass.txt -d "user=~USER~&pass=~PASS~" -t 60 -M USER

```

## ⚖️ 免责声明 (Disclaimer)

本工具 (**Neobee_Tools / Brute Force**) 仅用于**教育目的**和**经授权的安全测试**。

1. **严禁非授权攻击**：在使用本工具对任何目标进行测试之前，您必须获得目标系统所有者的明确书面许可。
2. **法律责任**：开发者不对因使用本工具而导致的任何非法行为、系统损坏或数据丢失承担责任。用户需自行承担所有法律后果。
3. **合规性**：请遵守当地及国际网络安全法律法规（如《中华人民共和国网络安全法》）。

**如果您下载、安装或使用本工具，即表示您同意本免责声明。**

---

Developed by [Neobee714](https://www.google.com/search?q=https://github.com/Neobee714)
