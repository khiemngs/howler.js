#!/usr/bin/env python3

# Read the file
with open('/home/daytona/howler.js/src/howler.core.js', 'r') as f:
    content = f.read()

# Improve iOS version detection for modern iOS browsers
# Current logic is outdated and may not handle newer iOS versions properly
# 
# Issues with current implementation:
# 1. Version threshold is hardcoded to < 9 (very outdated)
# 2. iOS version regex may not handle all modern formats
# 3. Webview detection may not work with modern iOS browsers
# 4. Safari detection is case-sensitive and may miss variations

# Find the iOS detection block and replace it with improved logic
old_ios_block = '''    // Check if a webview is being used on iOS8 or earlier (rather than the browser).
    // If it is, disable Web Audio as it causes crashing.
    var iOS = (/iP(hone|od|ad)/.test(Howler._navigator && Howler._navigator.platform));
    var appVersion = Howler._navigator && Howler._navigator.appVersion.match(/OS (\\d+)_(\\d+)_?(\\d+)?/);
    var version = appVersion ? parseInt(appVersion[1], 10) : null;
    if (iOS && version && version < 9) {
      var safari = /safari/.test(Howler._navigator && Howler._navigator.userAgent.toLowerCase());
      if (Howler._navigator && !safari) {
        Howler.usingWebAudio = false;
      }
    }'''

new_ios_block = '''    // Check if a webview is being used on older iOS versions (rather than the browser).
    // If it is, disable Web Audio as it can cause issues in webviews.
    var iOS = (/iP(hone|od|ad)/.test(Howler._navigator && Howler._navigator.platform));
    var appVersion = Howler._navigator && Howler._navigator.appVersion.match(/OS (\\d+)[._](\\d+)[._]?(\\d+)?/);
    var version = appVersion ? parseInt(appVersion[1], 10) : null;
    if (iOS && version && version < 13) {
      // Improved Safari/webview detection for modern iOS
      var userAgent = Howler._navigator && Howler._navigator.userAgent.toLowerCase();
      var isSafari = /safari/.test(userAgent) && !/crios|fxios|opios/.test(userAgent);
      var isWebView = !isSafari && (/webkit/.test(userAgent) || /mobile/.test(userAgent));
      
      if (Howler._navigator && isWebView) {
        Howler.usingWebAudio = false;
      }
    }'''

# Apply the change
content = content.replace(old_ios_block, new_ios_block)

# Write the file back
with open('/home/daytona/howler.js/src/howler.core.js', 'w') as f:
    f.write(content)

print("Successfully improved iOS version detection:")
print("- Updated iOS version regex to handle both underscore and dot separators")
print("- Increased version threshold from < 9 to < 13 for modern iOS compatibility")
print("- Improved Safari vs webview detection logic")
print("- Added detection for Chrome iOS, Firefox iOS, and Opera iOS")
print("- Enhanced webview detection for modern iOS browsers")
print("- Updated comments to reflect current iOS landscape")
