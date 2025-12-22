# Neobee 🐝

A powerful multi-threaded login brute force tool with real-time progress display and flexible attack modes.

[English](#english) | [中文](#中文)

---

## English

### Features

✨ **Multi-threaded Attack**: Utilize multiple threads for concurrent credential testing
🎯 **Dual Attack Modes**:
  - **USER Mode**: Test all passwords against one user before moving to the next
  - **PASS Mode**: Test all users against each password

📊 **Real-time Progress Display**: Live updates showing current user/password being tested (refreshes on same line)

🔧 **Flexible Configuration**:
  - Support for GET/POST/PUT/HEAD HTTP methods
  - Custom HTTP headers support
  - Customizable error message detection
  - Batch password loading (memory efficient)

⚡ **High Performance**: Optimized lock management and resource usage

### Requirements

- Python 3.6+
- requests library

### Installation

```bash
git clone https://github.com/yourusername/Neobee.git
cd Neobee
pip install requests
```

### Usage

#### Basic Usage

```bash
# USER mode - test all passwords against a single user
python neobee.py -u http://target.com/login \
                  -P passwords.txt \
                  -n admin \
                  -d "username=~USER~&password=~PASS~"

# PASS mode - test all users against each password
python neobee.py -u http://target.com/login \
                  -U usernames.txt \
                  -P passwords.txt \
                  -d "username=~USER~&password=~PASS~" \
                  -M PASS
```

#### Command Line Options

| Option | Short | Required | Description |
|--------|-------|----------|-------------|
| `--url` | `-u` | ✅ | Target URL |
| `--passfile` | `-P` | ✅ | Password dictionary file |
| `--data` | `-d` | ✅ | POST/GET data format (use `~USER~` and `~PASS~` as placeholders) |
| `--userfile` | `-U` | ❌* | Username dictionary file |
| `--username` | `-n` | ❌* | Single username |
| `--threads` | `-t` | ❌ | Number of threads (default: 40) |
| `--method` | `-m` | ❌ | HTTP method: GET/POST/PUT/HEAD (default: POST) |
| `--Mode` | `-M` | ❌ | Attack mode: USER/PASS (default: USER) |
| `--error_message` | `-F` | ❌ | Error message to detect failed login (default: `type="password"`) |
| `--header` | `-H` | ❌ | Custom HTTP header, can be used multiple times |

*Either `--userfile` or `--username` must be provided

#### Examples

**Example 1: Basic POST request with custom headers**
```bash
python neobee.py -u http://example.com/login \
                  -P passwords.txt \
                  -n admin \
                  -d "user=~USER~&pass=~PASS~" \
                  -H "Cookie: session=abc123" \
                  -H "User-Agent: Mozilla/5.0"
```

**Example 2: GET request with custom error message**
```bash
python neobee.py -u http://example.com/login \
                  -U users.txt \
                  -P passwords.txt \
                  -d "username=~USER~&password=~PASS~" \
                  -m GET \
                  -F "Invalid credentials" \
                  -t 50
```

**Example 3: PASS mode with multiple users**
```bash
python neobee.py -u http://example.com/login \
                  -U users.txt \
                  -P passwords.txt \
                  -d "username=~USER~&password=~PASS~" \
                  -M PASS \
                  -t 30
```

### How It Works

1. **Initialization**: Loads user list and initializes thread pool
2. **Authentication Loop**: 
   - Submits login requests with different credentials
   - Monitors responses for success/failure indicators
3. **Progress Tracking**: Real-time display updates every 0.5 seconds
4. **Success Detection**: When credentials are found or all combinations tested, gracefully stops

### Detection Logic

The tool considers login successful when:
- HTTP response code is 200 AND
- The error message is NOT present in response body

**Default error message**: `type="password"` (common HTML form attribute)

You can specify custom error messages using the `-F` flag for different target applications.

### Performance Tips

- **Adjust thread count** (`-t`): Increase for faster testing, decrease to reduce load
- **Batch size**: Default is 1000 passwords per batch (memory efficient)
- **Timeout**: Default request timeout is 5 seconds
- **Error message**: Use specific error messages for faster detection

### Output Example

```
[*] target url:http://example.com/login
[*] pass wordlist:passwords.txt
[*] threads number:40
[*] attack mode: USER
[*] start: 2024-01-15 14:30:45
----------------------------------------
[*] [progress 1/5] Attempting to crack the user:admin
[*] User [1/5]: admin | Password: password123                 
[!] brute successful! credential is admin:password123

[*] Total time taken 45.23 seconds
```

### Disclaimer

⚠️ **Legal Notice**: This tool is provided for educational and authorized security testing purposes only. Unauthorized access to computer systems is illegal. Always obtain proper authorization before conducting any security testing.

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### License

MIT License

---

## 中文

### 功能特性

✨ **多线程攻击**：利用多线程并发测试凭证
🎯 **双重攻击模式**：
  - **USER 模式**：先对一个用户测试所有密码，再换用户
  - **PASS 模式**：先对一个密码测试所有用户，再换密码

📊 **实时进度显示**：同行刷新显示当前测试的用户/密码信息

🔧 **灵活配置**：
  - 支持 GET/POST/PUT/HEAD 等 HTTP 方法
  - 自定义 HTTP 请求头
  - 自定义错误信息检测
  - 批量加载密码（内存高效）

⚡ **高性能**：优化的锁管理和资源利用

### 环境要求

- Python 3.6+
- requests 库

### 安装

```bash
git clone https://github.com/yourusername/Neobee.git
cd Neobee
pip install requests
```

### 使用方法

#### 基础用法

```bash
# USER 模式 - 用所有密码测试一个用户
python neobee.py -u http://target.com/login \
                  -P passwords.txt \
                  -n admin \
                  -d "username=~USER~&password=~PASS~"

# PASS 模式 - 用所有用户测试一个密码
python neobee.py -u http://target.com/login \
                  -U usernames.txt \
                  -P passwords.txt \
                  -d "username=~USER~&password=~PASS~" \
                  -M PASS
```

#### 命令行参数

| 参数 | 短选项 | 必需 | 说明 |
|------|--------|------|------|
| `--url` | `-u` | ✅ | 目标 URL |
| `--passfile` | `-P` | ✅ | 密码字典文件 |
| `--data` | `-d` | ✅ | POST/GET 数据格式（使用 `~USER~` 和 `~PASS~` 作为占位符） |
| `--userfile` | `-U` | ❌* | 用户名字典文件 |
| `--username` | `-n` | ❌* | 单个用户名 |
| `--threads` | `-t` | ❌ | 线程数（默认：40） |
| `--method` | `-m` | ❌ | HTTP 方法：GET/POST/PUT/HEAD（默认：POST） |
| `--Mode` | `-M` | ❌ | 攻击模式：USER/PASS（默认：USER） |
| `--error_message` | `-F` | ❌ | 用于检测登录失败的错误信息（默认：`type="password"`） |
| `--header` | `-H` | ❌ | 自定义 HTTP 请求头，可多次使用 |

*必须提供 `--userfile` 或 `--username` 中的一个

#### 使用示例

**示例 1：带自定义请求头的基础 POST 请求**
```bash
python neobee.py -u http://example.com/login \
                  -P passwords.txt \
                  -n admin \
                  -d "user=~USER~&pass=~PASS~" \
                  -H "Cookie: session=abc123" \
                  -H "User-Agent: Mozilla/5.0"
```

**示例 2：GET 请求和自定义错误信息**
```bash
python neobee.py -u http://example.com/login \
                  -U users.txt \
                  -P passwords.txt \
                  -d "username=~USER~&password=~PASS~" \
                  -m GET \
                  -F "Invalid credentials" \
                  -t 50
```

**示例 3：PASS 模式和多个用户**
```bash
python neobee.py -u http://example.com/login \
                  -U users.txt \
                  -P passwords.txt \
                  -d "username=~USER~&password=~PASS~" \
                  -M PASS \
                  -t 30
```

### 工作原理

1. **初始化**：加载用户列表并初始化线程池
2. **认证循环**：
   - 提交不同凭证的登录请求
   - 监控响应中的成功/失败指示符
3. **进度追踪**：实时显示每 0.5 秒更新一次
4. **成功检测**：找到凭证或测试所有组合后，优雅地停止

### 检测逻辑

当满足以下条件时，认为登录成功：
- HTTP 响应代码为 200 AND
- 错误信息在响应体中不存在

**默认错误信息**：`type="password"`（常见 HTML 表单属性）

可以使用 `-F` 参数为不同的目标应用指定自定义错误信息。

### 性能优化建议

- **调整线程数** (`-t`)：增加以加快测试，减少以降低负载
- **批处理大小**：默认每批 1000 个密码（内存高效）
- **超时时间**：默认请求超时为 5 秒
- **错误信息**：使用具体的错误信息以加快检测速度

### 输出示例

```
[*] target url:http://example.com/login
[*] pass wordlist:passwords.txt
[*] threads number:40
[*] attack mode: USER
[*] start: 2024-01-15 14:30:45
----------------------------------------
[*] [progress 1/5] Attempting to crack the user:admin
[*] User [1/5]: admin | Password: password123                 
[!] brute successful! credential is admin:password123

[*] Total time taken 45.23 seconds
```

### 免责声明

⚠️ **法律声明**：此工具仅用于教育和授权的安全测试目的。未经授权访问计算机系统是违法的。在进行任何安全测试之前，请确保获得适当的授权。

### 贡献

欢迎提交 Pull Request！

### 许可证

MIT License
