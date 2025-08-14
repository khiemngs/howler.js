#!/usr/bin/env python3

# Read the file
with open('/home/daytona/howler.js/src/plugins/howler.spatial.js', 'r') as f:
    content = f.read()

# Replace deprecated spatial audio APIs
# Since all browsers that support spatial audio now support the modern API,
# we can remove the fallback calls to deprecated setPosition() and setOrientation() methods

# 1. Fix listener position setting (around line 74)
old_listener_pos = '''      if (typeof self.ctx.listener.positionX !== 'undefined') {
        self.ctx.listener.positionX.setTargetAtTime(self._pos[0], Howler.ctx.currentTime, 0.1);
        self.ctx.listener.positionY.setTargetAtTime(self._pos[1], Howler.ctx.currentTime, 0.1);
        self.ctx.listener.positionZ.setTargetAtTime(self._pos[2], Howler.ctx.currentTime, 0.1);
      } else {
        self.ctx.listener.setPosition(self._pos[0], self._pos[1], self._pos[2]);
      }'''

new_listener_pos = '''      self.ctx.listener.positionX.setTargetAtTime(self._pos[0], Howler.ctx.currentTime, 0.1);
      self.ctx.listener.positionY.setTargetAtTime(self._pos[1], Howler.ctx.currentTime, 0.1);
      self.ctx.listener.positionZ.setTargetAtTime(self._pos[2], Howler.ctx.currentTime, 0.1);'''

# 2. Fix listener orientation setting (around line 124)
old_listener_orient = '''      if (typeof self.ctx.listener.forwardX !== 'undefined') {
        self.ctx.listener.forwardX.setTargetAtTime(x, Howler.ctx.currentTime, 0.1);
        self.ctx.listener.forwardY.setTargetAtTime(y, Howler.ctx.currentTime, 0.1);
        self.ctx.listener.forwardZ.setTargetAtTime(z, Howler.ctx.currentTime, 0.1);
        self.ctx.listener.upX.setTargetAtTime(xUp, Howler.ctx.currentTime, 0.1);
        self.ctx.listener.upY.setTargetAtTime(yUp, Howler.ctx.currentTime, 0.1);
        self.ctx.listener.upZ.setTargetAtTime(zUp, Howler.ctx.currentTime, 0.1);
      } else {
        self.ctx.listener.setOrientation(x, y, z, xUp, yUp, zUp);
      }'''

new_listener_orient = '''      self.ctx.listener.forwardX.setTargetAtTime(x, Howler.ctx.currentTime, 0.1);
      self.ctx.listener.forwardY.setTargetAtTime(y, Howler.ctx.currentTime, 0.1);
      self.ctx.listener.forwardZ.setTargetAtTime(z, Howler.ctx.currentTime, 0.1);
      self.ctx.listener.upX.setTargetAtTime(xUp, Howler.ctx.currentTime, 0.1);
      self.ctx.listener.upY.setTargetAtTime(yUp, Howler.ctx.currentTime, 0.1);
      self.ctx.listener.upZ.setTargetAtTime(zUp, Howler.ctx.currentTime, 0.1);'''

# 3. Fix panner position setting in pan method (around line 236)
old_pan_pos = '''              if (typeof sound._panner.positionX !== 'undefined') {
                sound._panner.positionX.setValueAtTime(pan, Howler.ctx.currentTime);
                sound._panner.positionY.setValueAtTime(0, Howler.ctx.currentTime);
                sound._panner.positionZ.setValueAtTime(0, Howler.ctx.currentTime);
              } else {
                sound._panner.setPosition(pan, 0, 0);
              }'''

new_pan_pos = '''              sound._panner.positionX.setValueAtTime(pan, Howler.ctx.currentTime);
              sound._panner.positionY.setValueAtTime(0, Howler.ctx.currentTime);
              sound._panner.positionZ.setValueAtTime(0, Howler.ctx.currentTime);'''

# 4. Fix panner position setting in pos method (around line 316)
old_pos_set = '''            if (typeof sound._panner.positionX !== 'undefined') {
              sound._panner.positionX.setValueAtTime(x, Howler.ctx.currentTime);
              sound._panner.positionY.setValueAtTime(y, Howler.ctx.currentTime);
              sound._panner.positionZ.setValueAtTime(z, Howler.ctx.currentTime);
            } else {
              sound._panner.setPosition(x, y, z);
            }'''

new_pos_set = '''            sound._panner.positionX.setValueAtTime(x, Howler.ctx.currentTime);
            sound._panner.positionY.setValueAtTime(y, Howler.ctx.currentTime);
            sound._panner.positionZ.setValueAtTime(z, Howler.ctx.currentTime);'''

# 5. Fix panner orientation setting in orientation method (around line 400)
old_orient_set = '''            if (typeof sound._panner.orientationX !== 'undefined') {
              sound._panner.orientationX.setValueAtTime(x, Howler.ctx.currentTime);
              sound._panner.orientationY.setValueAtTime(y, Howler.ctx.currentTime);
              sound._panner.orientationZ.setValueAtTime(z, Howler.ctx.currentTime);
            } else {
              sound._panner.setOrientation(x, y, z);
            }'''

new_orient_set = '''            sound._panner.orientationX.setValueAtTime(x, Howler.ctx.currentTime);
            sound._panner.orientationY.setValueAtTime(y, Howler.ctx.currentTime);
            sound._panner.orientationZ.setValueAtTime(z, Howler.ctx.currentTime);'''

# 6. Fix panner setup in setupPanner method (around lines 637 and 645)
old_panner_pos = '''      if (typeof sound._panner.positionX !== 'undefined') {
        sound._panner.positionX.setValueAtTime(sound._pos[0], Howler.ctx.currentTime);
        sound._panner.positionY.setValueAtTime(sound._pos[1], Howler.ctx.currentTime);
        sound._panner.positionZ.setValueAtTime(sound._pos[2], Howler.ctx.currentTime);
      } else {
        sound._panner.setPosition(sound._pos[0], sound._pos[1], sound._pos[2]);
      }'''

new_panner_pos = '''      sound._panner.positionX.setValueAtTime(sound._pos[0], Howler.ctx.currentTime);
      sound._panner.positionY.setValueAtTime(sound._pos[1], Howler.ctx.currentTime);
      sound._panner.positionZ.setValueAtTime(sound._pos[2], Howler.ctx.currentTime);'''

old_panner_orient = '''      if (typeof sound._panner.orientationX !== 'undefined') {
        sound._panner.orientationX.setValueAtTime(sound._orientation[0], Howler.ctx.currentTime);
        sound._panner.orientationY.setValueAtTime(sound._orientation[1], Howler.ctx.currentTime);
        sound._panner.orientationZ.setValueAtTime(sound._orientation[2], Howler.ctx.currentTime);
      } else {
        sound._panner.setOrientation(sound._orientation[0], sound._orientation[1], sound._orientation[2]);
      }'''

new_panner_orient = '''      sound._panner.orientationX.setValueAtTime(sound._orientation[0], Howler.ctx.currentTime);
      sound._panner.orientationY.setValueAtTime(sound._orientation[1], Howler.ctx.currentTime);
      sound._panner.orientationZ.setValueAtTime(sound._orientation[2], Howler.ctx.currentTime);'''

# Apply all the changes
content = content.replace(old_listener_pos, new_listener_pos)
content = content.replace(old_listener_orient, new_listener_orient)
content = content.replace(old_pan_pos, new_pan_pos)
content = content.replace(old_pos_set, new_pos_set)
content = content.replace(old_orient_set, new_orient_set)
content = content.replace(old_panner_pos, new_panner_pos)
content = content.replace(old_panner_orient, new_panner_orient)

# Write the file back
with open('/home/daytona/howler.js/src/plugins/howler.spatial.js', 'w') as f:
    f.write(content)

print("Successfully replaced deprecated spatial audio APIs:")
print("- Removed setPosition() fallbacks at lines 74, 236, 316, 637")
print("- Removed setOrientation() fallbacks at lines 124, 400, 645")
print("- Now uses only modern positionX/Y/Z and orientationX/Y/Z properties")
print("- Simplified code by removing unnecessary feature detection")
