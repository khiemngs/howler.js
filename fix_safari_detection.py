#!/usr/bin/env python3

# Read the file
with open('/home/daytona/howler.js/src/howler.core.js', 'r') as f:
    content = f.read()

# Update Safari version detection logic using simple string replacement
# 1. Improve the version parsing regex to handle edge cases
content = content.replace(
    'var safariVersion = ua.match(/Version\/(.*?) /);',
    'var safariVersion = ua.match(/Version\/([\\d\\.]+)/);'
)

# 2. Update the version threshold from < 15 to < 17
content = content.replace(
    'var isOldSafari = (checkSafari && safariVersion && parseInt(safariVersion[1], 10) < 15);',
    'var isOldSafari = (checkSafari && safariVersion && parseInt(safariVersion[1], 10) < 17);'
)

# Write the file back
with open('/home/daytona/howler.js/src/howler.core.js', 'w') as f:
    f.write(content)

print("Successfully updated Safari version detection logic:")
print("- Improved version parsing regex to handle edge cases")
print("- Updated version threshold from < 15 to < 17")


