const { app, BrowserWindow } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

let win = null;
let py = null;
let quitting = false;

function safeSend(channel, payload) {
  if (!win) return;
  const wc = win.webContents;
  if (win.isDestroyed()) return;
  if (!wc || wc.isDestroyed()) return;
  wc.send(channel, payload);
}

function cleanupPython() {
  if (!py) return;
  try {
    py.stdout?.removeAllListeners();
    py.stderr?.removeAllListeners();
    py.removeAllListeners();
    py.stdout?.destroy();
    py.stderr?.destroy();
    if (!py.killed) py.kill('SIGTERM');
  } catch {}
  py = null;
}

function createWindow() {
  win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: { preload: path.join(__dirname, 'preload.js') }
  });
  win.loadFile('index.html');

  const venvPython = path.join(__dirname, 'venv', 'bin', 'python');
  const pythonCmd = fs.existsSync(venvPython)
    ? venvPython
    : (process.platform === 'win32'
        ? path.join(__dirname, 'venv', 'Scripts', 'python.exe')
        : 'python3');

  py = spawn(pythonCmd, [path.join(__dirname, 'main.py')], {
    cwd: __dirname,
    env: { ...process.env }
  });

  py.stdout.on('data', (data) => {
    safeSend('py:stdout', data.toString());
  });
  py.stderr.on('data', (data) => {
    safeSend('py:stderr', data.toString());
  });
  py.on('close', (code) => {
    safeSend('py:exit', code);
  });

  win.on('closed', () => {
    cleanupPython();
    win = null;
  });

  win.webContents.on('destroyed', () => {
    cleanupPython();
  });
}

app.on('before-quit', () => {
  quitting = true;
  cleanupPython();
});

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  cleanupPython();
  if (process.platform !== 'darwin') app.quit();
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0 && !quitting) createWindow();
});

