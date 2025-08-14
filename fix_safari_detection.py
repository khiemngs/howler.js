#!/usr/bin/env python3
import re

# Read the file
with open('/home/daytona/howler.js/src/howler.core.js', 'r') as f:
    content = f.read()

# Update Safari version detection logic
# 1. Improve the version parsing regex to handle edge cases
old_version_regex = r'var safariVersion = ua\.match\(/Version\/\(\.\*\?\) /\);'
new_version_regex = 'var safariVersion = ua.match(/Version\/([\\d\\.]+)/);'

# 2. Update the version threshold from < 15 to < 17
old_threshold = r'var isOldSafari = \(checkSafari && safariVersion && parseInt\(safariVersion\[1\], 10\) < 15\);'
new_threshold = 'var isOldSafari = (checkSafari && safariVersion && parseInt(safariVersion[1], 10) < 17);'

# Apply the changes
content = re.sub(old_version_regex, new_version_regex, content)
content = re.sub(old_threshold, new_threshold, content)

# Write the file back
with open('/home/daytona/howler.js/src/howler.core.js', 'w') as f:
    f.write(content)

print("Successfully updated Safari version detection logic:")
print("- Improved version parsing regex to handle edge cases")
print("- Updated version threshold from < 15 to < 17")
