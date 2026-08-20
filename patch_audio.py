import codecs
with codecs.open('script.js', 'r', 'utf-8') as f:
    c = f.read()

audio_code = '''
// =============================
// Audio Feedback Web API
// =============================
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
function playTone(type) {
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const osc = audioCtx.createOscillator();
  const gainNode = audioCtx.createGain();
  osc.connect(gainNode);
  gainNode.connect(audioCtx.destination);

  if (type === 'success') {
    osc.type = 'sine';
    osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); // C5
    osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1); // E5
    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.3);
  } else if (type === 'error') {
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(150, audioCtx.currentTime);
    osc.frequency.linearRampToValueAtTime(100, audioCtx.currentTime + 0.3);
    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.3);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.3);
  }
}
'''

c = audio_code + '\n' + c
c = c.replace('console.log("Processing Volunteer ID for lookup:", id);', 'console.log("Processing Volunteer ID for lookup:", id);\n  playTone("success");')
c = c.replace('alert("Error: Volunteer ID not recognized. Please check with an admin.");', 'playTone("error");\n      alert("Error: Volunteer ID not recognized. Please check with an admin.");')
c = c.replace('alert("An error occurred while checking your status. Please try again.");', 'playTone("error");\n    alert("An error occurred while checking your status. Please try again.");')

with codecs.open('script.js', 'w', 'utf-8') as f:
    f.write(c)
