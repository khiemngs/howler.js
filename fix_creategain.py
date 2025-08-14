#!/usr/bin/env python3
import re

# Read the file
with open('/home/daytona/howler.js/src/howler.core.js', 'r') as f:
    content = f.read()

# Replace the deprecated createGainNode fallback pattern
pattern = r'\(typeof Howler\.ctx\.createGain === \'undefined\'\) \? Howler\.ctx\.createGainNode\(\) : Howler\.ctx\.createGain\(\)'
replacement = 'Howler.ctx.createGain()'

# Perform the replacement
new_content = re.sub(pattern, replacement, content)

# Write the file back
with open('/home/daytona/howler.js/src/howler.core.js', 'w') as f:
    f.write(new_content)

print("Successfully updated createGainNode() fallbacks to use createGain() directly")
