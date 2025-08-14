#!/usr/bin/env python3

# Read the file
with open('/home/daytona/howler.js/src/howler.core.js', 'r') as f:
    content = f.read()

# Fix Opera version detection for 3-digit versions
# The current logic is unnecessarily complex and could have issues with parsing
# Current: var checkOpera = ua.match(/OPR\/(\d+)/g);
#          var isOldOpera = (checkOpera && parseInt(checkOpera[0].split('/')[1], 10) < 33);
# 
# Issues: 1. Uses global flag 'g' which is unnecessary for single match
#         2. Uses complex parsing with split() instead of captured group
#         3. Could be more robust for multi-digit versions

# Replace the Opera detection logic
old_opera_match = 'var checkOpera = ua.match(/OPR\\/(\\d+)/g);'
new_opera_match = 'var checkOpera = ua.match(/OPR\\/(\\d+)/);'

old_opera_parse = 'var isOldOpera = (checkOpera && parseInt(checkOpera[0].split(\'/\')[1], 10) < 33);'
new_opera_parse = 'var isOldOpera = (checkOpera && parseInt(checkOpera[1], 10) < 33);'

# Apply the changes
content = content.replace(old_opera_match, new_opera_match)
content = content.replace(old_opera_parse, new_opera_parse)

# Write the file back
with open('/home/daytona/howler.js/src/howler.core.js', 'w') as f:
    f.write(content)

print("Successfully updated Opera version detection logic:")
print("- Removed unnecessary global flag 'g' from regex")
print("- Simplified parsing to use captured group directly")
print("- Improved reliability for multi-digit Opera versions (100+)")
