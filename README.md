# 日志敏感数据检查脚本

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

- Python环境：Python3

- 扫描单独日志敏感信息：
  - `$ python3 loginfoCheck.py -f *.log`

- 扫描文件夹日志敏感信息：
  - `$ python3 loginfoCheck.py -d /dir`

- 指定输出路径：
  - `$ python3 loginfoCheck.py -f *.log -s /dir`

- 默认输出路径为./info_check.txt ./info_check.csv


## 版本更新信息

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

# Log Sensitive Data Check Script

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

- Python environment: Python3

- Scan individual log files for sensitive information:
  - `$ python3 loginfoCheck.py -f *.log`

- Scan a folder for sensitive information in log files:
  - `$ python3 loginfoCheck.py -d /dir`

- Specify output path:
  - `$ python3 loginfoCheck.py -f *.log -s /dir`

- By default, the output path is ./info_check.txt ./info_check.csv


## Version Update Information

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