#!/usr/bin/env python3

# Read the file
with open('/home/daytona/howler.js/src/howler.core.js', 'r') as f:
    content = f.read()

# Improve AudioContext state management for modern browser audio policies
# and better mobile device interrupt handling

# 1. Enhance the _setup method to include better state change listeners
old_setup = '''    _setup: function() {
      var self = this || Howler;

      // Keeps track of the suspend/resume state of the AudioContext.
      self.state = self.ctx ? self.ctx.state || 'suspended' : 'suspended';

      // Automatically begin the 30-second suspend process
      self._autoSuspend();'''

new_setup = '''    _setup: function() {
      var self = this || Howler;

      // Keeps track of the suspend/resume state of the AudioContext.
      self.state = self.ctx ? self.ctx.state || 'suspended' : 'suspended';

      // Add state change listeners for better AudioContext state management
      if (self.ctx && typeof self.ctx.addEventListener === 'function') {
        // Listen for state changes to keep our internal state in sync
        self.ctx.addEventListener('statechange', function() {
          self.state = self.ctx.state;
          
          // Handle interrupted state on mobile devices
          if (self.ctx.state === 'interrupted') {
            // Clear any pending suspend timer since we're interrupted
            if (self._suspendTimer) {
              clearTimeout(self._suspendTimer);
              self._suspendTimer = null;
            }
            
            // Emit interrupt event to all Howls
            for (var i = 0; i < self._howls.length; i++) {
              self._howls[i]._emit('interrupt');
            }
          } else if (self.ctx.state === 'running' && self.state !== 'running') {
            // AudioContext resumed from interrupted state
            for (var i = 0; i < self._howls.length; i++) {
              self._howls[i]._emit('resume');
            }
          }
        });
      }

      // Automatically begin the 30-second suspend process
      self._autoSuspend();'''

# 2. Improve the _autoResume method to handle interrupted states better
old_auto_resume = '''      if (self.state === 'running' && self.ctx.state !== 'interrupted' && self._suspendTimer) {
        clearTimeout(self._suspendTimer);
        self._suspendTimer = null;
      } else if (self.state === 'suspended' || self.state === 'running' && self.ctx.state === 'interrupted') {
        self.ctx.resume().then(function() {
          self.state = 'running';

          // Emit to all Howls that the audio has resumed.
          for (var i=0; i<self._howls.length; i++) {
            self._howls[i]._emit('resume');
          }
        });

        if (self._suspendTimer) {
          clearTimeout(self._suspendTimer);
          self._suspendTimer = null;
        }
      } else if (self.state === 'suspending') {
        self._resumeAfterSuspend = true;
      }'''

new_auto_resume = '''      if (self.state === 'running' && self.ctx.state !== 'interrupted' && self._suspendTimer) {
        clearTimeout(self._suspendTimer);
        self._suspendTimer = null;
      } else if (self.state === 'suspended' || self.state === 'interrupted' || (self.state === 'running' && self.ctx.state === 'interrupted')) {
        // Enhanced resume logic with better error handling
        self.ctx.resume().then(function() {
          self.state = 'running';

          // Emit to all Howls that the audio has resumed.
          for (var i=0; i<self._howls.length; i++) {
            self._howls[i]._emit('resume');
          }
        }).catch(function(err) {
          // Handle resume failures gracefully
          console.warn('AudioContext resume failed:', err);
          
          // Try to recover by creating a new AudioContext if needed
          if (self.ctx.state === 'closed') {
            self._recoverAudioContext();
          }
        });

        if (self._suspendTimer) {
          clearTimeout(self._suspendTimer);
          self._suspendTimer = null;
        }
      } else if (self.state === 'suspending') {
        self._resumeAfterSuspend = true;
      }'''

# 3. Add a new method for AudioContext recovery
recovery_method = '''
    /**
     * Recover from a closed or corrupted AudioContext by creating a new one.
     * This can happen on mobile devices when the app is backgrounded for too long.
     * @return {Howler}
     */
    _recoverAudioContext: function() {
      var self = this;
      
      if (!self.usingWebAudio) {
        return self;
      }
      
      // Store the old context for cleanup
      var oldCtx = self.ctx;
      
      try {
        // Create a new AudioContext
        if (typeof AudioContext !== 'undefined') {
          self.ctx = new AudioContext();
        } else {
          self.usingWebAudio = false;
          return self;
        }
        
        // Update state
        self.state = self.ctx.state || 'suspended';
        
        // Recreate master gain node
        if (self.masterGain) {
          self.masterGain = self.ctx.createGain();
          self.masterGain.gain.setValueAtTime(self._muted ? 0 : self._volume, self.ctx.currentTime);
          self.masterGain.connect(self.ctx.destination);
        }
        
        // Re-setup state change listeners
        if (typeof self.ctx.addEventListener === 'function') {
          self.ctx.addEventListener('statechange', function() {
            self.state = self.ctx.state;
          });
        }
        
        // Notify all Howls that the context has been recovered
        for (var i = 0; i < self._howls.length; i++) {
          self._howls[i]._emit('contextrecovered');
        }
        
        // Clean up old context
        if (oldCtx && typeof oldCtx.close === 'function') {
          oldCtx.close();
        }
        
      } catch (e) {
        console.error('Failed to recover AudioContext:', e);
        self.usingWebAudio = false;
      }
      
      return self;
    },'''

# Apply the changes
content = content.replace(old_setup, new_setup)
content = content.replace(old_auto_resume, new_auto_resume)

# Insert the recovery method before the setupAudioContext function
setup_audio_context_pos = content.find('  var setupAudioContext = function() {')
if setup_audio_context_pos != -1:
    content = content[:setup_audio_context_pos] + recovery_method + '\n\n  ' + content[setup_audio_context_pos:]

# Write the file back
with open('/home/daytona/howler.js/src/howler.core.js', 'w') as f:
    f.write(content)

print("Successfully improved AudioContext state management:")
print("- Added state change event listeners for better state tracking")
print("- Enhanced handling of 'interrupted' states on mobile devices")
print("- Improved suspend/resume logic with better error handling")
print("- Added AudioContext recovery method for closed contexts")
print("- Added interrupt and contextrecovered events for Howls")
print("- Better compatibility with modern browser audio policies")
