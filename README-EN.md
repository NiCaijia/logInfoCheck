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