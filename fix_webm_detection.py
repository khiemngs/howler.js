#!/usr/bin/env python3

# Read the file
with open('/home/daytona/howler.js/src/howler.core.js', 'r') as f:
    content = f.read()

# Update WebM codec detection for modern Safari
# Current logic disables WebM for all Safari versions using !isOldSafari
# We need to enable WebM for Safari 15+ since modern Safari supports WebM audio
# 
# We need to create a more specific condition that allows WebM for Safari 15+
# while still blocking it for older Safari versions that don't support it

# First, we need to add a specific check for Safari versions that support WebM
# We'll add this logic right after the isOldSafari definition

# Find the line after isOldSafari definition to insert our new logic
insert_point = content.find('var isOldSafari = (checkSafari && safariVersion && parseInt(safariVersion[1], 10) < 17);')
if insert_point != -1:
    # Find the end of this line
    end_of_line = content.find('\n', insert_point)
    if end_of_line != -1:
        # Insert the new logic for WebM-capable Safari detection
        new_logic = '\n      var isWebMCapableSafari = (checkSafari && safariVersion && parseInt(safariVersion[1], 10) >= 15);'
        content = content[:end_of_line] + new_logic + content[end_of_line:]

# Now update the WebM codec detection lines to use the new logic
# Change from !isOldSafari to (!checkSafari || isWebMCapableSafari)
# This means: allow WebM if it's not Safari, OR if it's Safari 15+

old_weba = 'weba: !!(!isOldSafari && audioTest.canPlayType(\'audio/webm; codecs="vorbis"\').replace(/^no$/, \'\')),'
new_weba = 'weba: !!((!checkSafari || isWebMCapableSafari) && audioTest.canPlayType(\'audio/webm; codecs="vorbis"\').replace(/^no$/, \'\')),'

old_webm = 'webm: !!(!isOldSafari && audioTest.canPlayType(\'audio/webm; codecs="vorbis"\').replace(/^no$/, \'\')),'
new_webm = 'webm: !!((!checkSafari || isWebMCapableSafari) && audioTest.canPlayType(\'audio/webm; codecs="vorbis"\').replace(/^no$/, \'\')),'

# Apply the changes
content = content.replace(old_weba, new_weba)
content = content.replace(old_webm, new_webm)

# Write the file back
with open('/home/daytona/howler.js/src/howler.core.js', 'w') as f:
    f.write(content)

print("Successfully updated WebM codec detection for modern Safari:")
print("- Added isWebMCapableSafari check for Safari 15+")
print("- Updated weba codec detection to enable for Safari 15+")
print("- Updated webm codec detection to enable for Safari 15+")
print("- Maintains backward compatibility by blocking WebM for Safari < 15")
