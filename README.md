# 日志敏感数据检查脚本 / Log Sensitive Data Check Script

**语言 / Language**: [中文](#简介) | [English](#introduction)

---

## 简介

- 此脚本用于检查日志文件中客户的敏感信息
- 检查内容覆盖了C3类数据和C2类数据的客户敏感信息
- 采用字段匹配和正则匹配两种方式进行检查
- 正则匹配的规则包括：
  - C3类数据（不允许保存）：
    - 银行卡磁道数据-磁道2
    - 银行卡磁道数据-磁道3
    - 银行卡账号
    - 用于身份鉴别生物识别信息
  - C2类数据（需要脱敏后保存）：
    - 证件号码
    - 手机号码
    - 家庭地址
- 字段匹配可以在配置文件configs.ini中进行配置，配置key后即可在日志文件中扫描相关字段

## 使用方法

### 环境要求

- **Python 版本**：Python 3.7 或更高版本
- **依赖库**：
  ```bash
  pip install -r requirements.txt
  ```

### 基础用法

#### 1. 扫描单个日志文件
```bash
python3 loginfoCheck.py -f /path/to/logfile.log
```

#### 2. 扫描文件夹（推荐）
```bash
python3 loginfoCheck.py -d /path/to/logs/
```

#### 3. 扫描压缩包
```bash
python3 loginfoCheck.py -z /path/to/logs.zip
```

### 扫描级别

#### Level 1 - 标准模式（推荐日常使用）
- **规则数量**：13 条基础正则
- **扫描速度**：快（约 8.5 秒 / 17.2MB）
- **适用场景**：日常日志检查、快速安全审计

```bash
python3 loginfoCheck.py -f logfile.log -l 1
```

#### Level 2 - 深度模式（完整合规扫描）
- **规则数量**：800+ 条（包含完整银行卡 BIN 码库）
- **扫描速度**：慢（约 3 分 15 秒 / 17.2MB，比 Level 1 慢 15-20 倍）
- **适用场景**：完整合规审计、深度安全检查

```bash
python3 loginfoCheck.py -f logfile.log -l 2
```

**注意**：选择 Level 2 时会提示确认，可选择继续或切换到 Level 1。

### 高级选项

#### 指定输出路径
```bash
python3 loginfoCheck.py -f logfile.log -s /custom/path/report
```
输出文件：`/custom/path/report.txt` 和 `/custom/path/report.csv`

#### 自动解压 .gz 文件
```bash
# 解压单个 .gz 文件后扫描
python3 loginfoCheck.py -f logfile.log.gz -gz

# 解压文件夹中所有 .gz 文件后扫描
python3 loginfoCheck.py -d /path/to/logs/ -gz
```

#### 禁用彩色输出
```bash
# 适用于重定向到文件或不支持 ANSI 颜色的终端
python3 loginfoCheck.py -f logfile.log --no-color
```

### 完整命令示例

```bash
# 使用所有选项
python3 loginfoCheck.py -f /var/log/app.log -l 1 -s ./reports/scan_result -gz --no-color
```

### 参数说明

| 参数 | 长参数 | 说明 | 示例 |
|------|--------|------|------|
| `-f` | `--file` | 扫描单个日志文件 | `-f app.log` |
| `-d` | `--dir` | 扫描文件夹 | `-d /var/logs/` |
| `-z` | `--zip` | 扫描压缩包（支持 .zip .rar） | `-z logs.zip` |
| `-l` | `--level` | 扫描级别（1 或 2，默认 1） | `-l 2` |
| `-s` | `--save` | 输出路径（默认 ./info_check） | `-s /tmp/report` |
| `-gz` | `--extract_gz` | 自动解压 .gz 文件 | `-gz` |
| | `--no-color` | 禁用彩色输出 | `--no-color` |
| `-v` | `--version` | 显示版本信息 | `-v` |

### 输出文件

默认输出到当前目录：
- `info_check.txt` - 文本格式报告
- `info_check.csv` - CSV 格式报告

### 性能参考

基于 17.2MB 日志文件的实测数据：
- **Level 1**：约 8.5 秒
- **Level 2**：约 3 分 15 秒

**建议**：
- 日常检查使用 Level 1
- 深度合规审计使用 Level 2



## 版本更新信息

### v0.7.0

1. 新增 Level 2 深度扫描模式，新增 800+ 银行卡 BIN 码规则。
2. 新增滑动窗口分块扫描功能，解决超长行（10万+字符）导致的卡死问题，支持完整扫描不跳过数据。
3. 优化了正则检出准确率。
4. 优化了扫描逻辑性能，可以更快的执行扫描任务，Level 1 模式下较上版本速度提升约34%。
5. 优化了用于身份鉴别生物识别信息的正则，大幅减少误报。输出结果展示由原来的1000位缩短至300位以减少编辑器打开时的错行问题。
6. 优化了日志输出格式及内容。
7. 优化了控制台输出，新增 SQLMap 风格输出，增加 Level 2 交互式确认。
8. 优化了扫描过程中去重逻辑，去重算法 O(n²) → O(n)。
9. 修复了之前版本大文件或多文件扫描时输出缓冲区阻塞的问题。
10. 修复了 -f 选项下扫描文件时，扫描时间过长卡死的问题。
11. 修复了文件句柄泄漏的问题。
12. 实测当前版本17.2M的日志文件，Level 1 扫描需要8.5秒左右，Level 2 扫描需要3分15秒左右。

### v0.6.1

1. 优化正则匹配规则，更加精准匹配敏感信息的检出。

### v0.6.0

1. 新增 GB2312 转 UTF-8 编码转换功能，程序中自动转码。
2. 变更默认扫描级别更改为 Level 2。
3. 优化 .gz 文件解压功能，支持在 '-f' 和 '-d' 后面加上 '-gz'，以在执行扫描前解压压缩文件。
4. 优化控制台输出，实时显示扫描进度，更新文件扫描状态。
5. 修复已知BUG。

### v0.5.230706

1. 新增了扫描级别选项，Level 1 仅检出当前行首条敏感信息（速度快）,Level 2 检出当前行所有敏感信息（精度高）。默认使用1级。
2. 新增了.gz解压功能，将当前文件夹中所有的.gz文件遍历解压并将源.gz文件删除。
3. 新增了文件夹扫描功能，参数为：-d /dir。
4. 新增了当前扫描进度在控制台输出。
5. 优化正则匹配精度。

### v0.4.230627

1. 新增了压缩包扫描功能（压缩包内仅有文件夹及日志文件），支持.zip .rar两种压缩包文件格式。
2. 新增了压缩包中文件转码功能，自动转为utf-8。
3. 新增了csv输出格式。
4. 优化了检出精度，同行数据中所有的敏感信息将被检出。
5. 优化了扫描结果输出，输出格式为*'敏感数据类型','配置文件匹配字段','疑似敏感信息','文件名称','检出行数'*。

### v0.3.221104

1. 忘了～

### v0.2.221101

1. 新增了configs.ini配置文件。
2. 新增了扫描类型，可以在配置文件中添加log的检查字段（key）列。
3. 新增了扫描用时计时。
4. 优化了扫描结果输出。

### v0.1

1. 新增了日志检查扫描。

------

## Introduction

- This script checks for customer's sensitive information in log files
- It checks for both C3 and C2 categories of sensitive data
- The checking is done via field matching and regex matching
- The regex matching rules cover the following types of data:
  - C3 category data (cannot be saved):
    - Bank card magnetic stripe data - Track 2
    - Bank card magnetic stripe data - Track 3
    - Bank account number
    - Biometric information used for identity verification
  - C2 category data (can be saved after anonymization):
    - Identification number
    - Mobile phone number
    - Home address
- For field matching, you can configure the keys in the configs.ini file. The script will then scan the corresponding fields in the log files.

## Usage

### Requirements

- **Python Version**: Python 3.7 or higher
- **Dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

### Basic Usage

#### 1. Scan a Single Log File
```bash
python3 loginfoCheck.py -f /path/to/logfile.log
```

#### 2. Scan a Folder (Recommended)
```bash
python3 loginfoCheck.py -d /path/to/logs/
```

#### 3. Scan a Compressed Archive
```bash
python3 loginfoCheck.py -z /path/to/logs.zip
```

### Scan Levels

#### Level 1 - Standard Mode (Recommended for Daily Use)
- **Rule Count**: 13 basic regex patterns
- **Scan Speed**: Fast (approx. 8.5 seconds / 17.2MB)
- **Use Cases**: Daily log checks, quick security audits

```bash
python3 loginfoCheck.py -f logfile.log -l 1
```

#### Level 2 - Deep Scan Mode (Complete Compliance Scanning)
- **Rule Count**: 800+ patterns (includes complete bank card BIN code database)
- **Scan Speed**: Slow (approx. 3 min 15 sec / 17.2MB, 15-20x slower than Level 1)
- **Use Cases**: Complete compliance audits, in-depth security checks

```bash
python3 loginfoCheck.py -f logfile.log -l 2
```

**Note**: When selecting Level 2, you will be prompted to confirm. You can choose to continue or switch to Level 1.

### Advanced Options

#### Specify Output Path
```bash
python3 loginfoCheck.py -f logfile.log -s /custom/path/report
```
Output files: `/custom/path/report.txt` and `/custom/path/report.csv`

#### Auto-extract .gz Files
```bash
# Extract and scan a single .gz file
python3 loginfoCheck.py -f logfile.log.gz -gz

# Extract all .gz files in a folder before scanning
python3 loginfoCheck.py -d /path/to/logs/ -gz
```

#### Disable Color Output
```bash
# Suitable for redirection to files or terminals without ANSI color support
python3 loginfoCheck.py -f logfile.log --no-color
```

### Complete Command Example

```bash
# Using all options
python3 loginfoCheck.py -f /var/log/app.log -l 1 -s ./reports/scan_result -gz --no-color
```

### Parameter Reference

| Param | Long Param | Description | Example |
|-------|------------|-------------|---------|
| `-f` | `--file` | Scan a single log file | `-f app.log` |
| `-d` | `--dir` | Scan a folder | `-d /var/logs/` |
| `-z` | `--zip` | Scan compressed archive (.zip .rar) | `-z logs.zip` |
| `-l` | `--level` | Scan level (1 or 2, default 1) | `-l 2` |
| `-s` | `--save` | Output path (default ./info_check) | `-s /tmp/report` |
| `-gz` | `--extract_gz` | Auto-extract .gz files | `-gz` |
| | `--no-color` | Disable color output | `--no-color` |
| `-v` | `--version` | Show version information | `-v` |

### Output Files

Default output to current directory:
- `info_check.txt` - Text format report
- `info_check.csv` - CSV format report

### Performance Benchmark

Based on 17.2MB log file testing:
- **Level 1**: approx. 8.5 seconds
- **Level 2**: approx. 3 minutes 15 seconds

**Recommendations**:
- Use Level 1 for daily checks
- Use Level 2 for deep compliance audits



## Version Update Information

### v0.7.0

1. Added Level 2 deep scan mode with 800+ bank card BIN code rules.
2. Added sliding window chunked scanning to resolve freeze issues caused by extremely long lines (100K+ characters), with full scanning capability without skipping data.
3. Optimized regular expression detection accuracy.
4. Optimized scanning logic performance, achieving approximately 34% speed improvement in Level 1 mode compared to the previous version.
5. Optimized regex for biometric identification information, significantly reducing false positives. Output display shortened from 1000 characters to 300 characters to reduce line wrapping issues in editors.
6. Optimized log output format and content.
7. Enhanced console output with SQLMap-style formatting and added interactive confirmation for Level 2 mode.
8. Optimized deduplication logic during scanning, improving algorithm complexity from O(n²) to O(n).
9. Fixed output buffer blocking issue in previous versions when scanning large or multiple files.
10. Fixed freeze issue when scanning files with the -f option that caused prolonged scan times.
11. Fixed file handle leak issue.
12. Performance benchmark: For a 17.2M log file, Level 1 scan takes approximately 8.5 seconds, Level 2 scan takes approximately 3 minutes 15 seconds.

### v0.6.1

1. Optimize regular expression matching rules for more accurate detection of sensitive information.

### v0.6.0

1. Added GB2312 to UTF-8 encoding conversion for automatic transcoding within the program.
2. Default scanning level changed to Level 2.
3. Enhanced .gz file extraction functionality, allowing the use of '-f' and '-d' followed by '-gz' to decompress compressed files before executing scans.
4. Improved console output for real-time scanning progress updates and file scanning status.
5. Fixed known bugs.

### v0.5.230706

1. Added scan level option, Level 1 only detects the first sensitive information in the current line (fast speed), Level 2 detects all sensitive information in the current line (high precision). Level 1 is used by default.
2. Added .gz decompression function, decompresses all .gz files in the current folder, and deletes the source .gz files.
3. Added folder scan function, parameter is: -d /dir.
4. Added current scan progress output in the console.
5. Optimized regular expression matching accuracy.

### v0.4.230627

1. Added the feature to scan compressed packages (only directories and log files within the package). Supports two types of compressed file formats: .zip and .rar.
2. Added a feature to convert the encoding of files in the compressed package to UTF-8 automatically.
3. CSV output format has been added.
4. Improved detection precision - all sensitive information in the same line will now be detected.
5. Optimized the output of scan results. The output format is now: 'Type of sensitive data', 'Matching field from the config file', 'Potential sensitive information', 'File name', 'Line number where the data is detected'.

### v0.3.221104

1. Forget～

### v0.2.221101

1. Added configs.ini configuration file.
2. Added scan type, you can add log check field (key) column in the configuration file.
3. Added scan timing.
4. Optimized scan results output.

### v0.1

1. Added log check scan.