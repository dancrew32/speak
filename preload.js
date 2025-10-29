const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('py', {
  onStdout: (cb) => ipcRenderer.on('py:stdout', (_, msg) => cb(msg)),
  onStderr: (cb) => ipcRenderer.on('py:stderr', (_, msg) => cb(msg)),
  onExit:   (cb) => ipcRenderer.on('py:exit',   (_, code)=> cb(code))
});

