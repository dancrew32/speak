const out = document.getElementById('out');
window.py.onStdout(msg => out.textContent += msg);
window.py.onStderr(msg => out.textContent += msg);
window.py.onExit(code => out.textContent += `\n[python exited ${code}]\n`);
