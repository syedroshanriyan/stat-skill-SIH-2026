/**
 * Unified Runner for STAT-SKILL AI Platform
 * Spawns both FastAPI Backend (port 8000) and Next.js Web (port 3000).
 * Exposes the entire platform seamlessly on http://localhost:3000!
 */

const { spawn } = require('child_process');
const path = require('path');
const http = require('http');

const ROOT_DIR = path.resolve(__dirname, '..');
const API_DIR = path.join(ROOT_DIR, 'apps', 'api');
const WEB_DIR = path.join(ROOT_DIR, 'apps', 'web');

const isWindows = process.platform === 'win32';

console.log('\x1b[36m%s\x1b[0m', '════════════════════════════════════════════════════════════════');
console.log('\x1b[1m\x1b[32m%s\x1b[0m', '  🚀 STAT-SKILL AI — Unified Platform Launch');
console.log('\x1b[36m%s\x1b[0m', '════════════════════════════════════════════════════════════════');

let backendProcess = null;
let webProcess = null;

function cleanup() {
  console.log('\n\x1b[33m%s\x1b[0m', 'Shutting down STAT-SKILL AI servers...');
  if (backendProcess) {
    try {
      if (isWindows) {
        spawn('taskkill', ['/pid', backendProcess.pid, '/f', '/t']);
      } else {
        backendProcess.kill('SIGTERM');
      }
    } catch {}
  }
  if (webProcess) {
    try {
      if (isWindows) {
        spawn('taskkill', ['/pid', webProcess.pid, '/f', '/t']);
      } else {
        webProcess.kill('SIGTERM');
      }
    } catch {}
  }
  process.exit(0);
}

process.on('SIGINT', cleanup);
process.on('SIGTERM', cleanup);

// 1. Launch Backend Process
console.log('\x1b[34m%s\x1b[0m', '[1/2] Starting FastAPI Backend on loopback port 8000...');
const pythonCmd = isWindows ? 'python' : 'python3';
backendProcess = spawn(pythonCmd, ['-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', '8000'], {
  cwd: API_DIR,
  stdio: 'inherit',
  shell: true,
});

backendProcess.on('error', (err) => {
  console.error('\x1b[31m[BACKEND ERROR]\x1b[0m', err.message);
});

// 2. Poll Backend Health then launch Next.js
function checkBackend(attempts = 0) {
  if (attempts > 30) {
    console.log('\x1b[33m%s\x1b[0m', 'Backend taking longer than expected. Proceeding to launch web...');
    launchWeb();
    return;
  }

  const req = http.get('http://127.0.0.1:8000/api/v1/health', (res) => {
    if (res.statusCode === 200) {
      console.log('\x1b[32m%s\x1b[0m', '✓ FastAPI Backend is healthy and listening on 127.0.0.1:8000');
      launchWeb();
    } else {
      setTimeout(() => checkBackend(attempts + 1), 500);
    }
  });

  req.on('error', () => {
    setTimeout(() => checkBackend(attempts + 1), 500);
  });
}

function launchWeb() {
  console.log('\x1b[35m%s\x1b[0m', '[2/2] Starting Next.js Web App on port 3000...');
  const npmCmd = isWindows ? 'npm.cmd' : 'npm';
  
  webProcess = spawn(npmCmd, ['run', 'start'], {
    cwd: WEB_DIR,
    stdio: 'inherit',
    shell: true,
    env: {
      ...process.env,
      BACKEND_URL: 'http://127.0.0.1:8000',
      NEXT_PUBLIC_API_URL: '/api/v1'
    }
  });

  webProcess.on('error', (err) => {
    console.error('\x1b[31m[WEB ERROR]\x1b[0m', err.message);
  });

  setTimeout(() => {
    console.log('\n\x1b[36m%s\x1b[0m', '────────────────────────────────────────────────────────────────');
    console.log('\x1b[1m\x1b[32m%s\x1b[0m', '  🌟 ALL SERVICES READY ON A SINGLE PORT: 3000');
    console.log('\x1b[36m%s\x1b[0m', '────────────────────────────────────────────────────────────────');
    console.log('  🏠 Intro Landing Page:      \x1b[4m\x1b[36mhttp://localhost:3000/\x1b[0m');
    console.log('  🔑 4 Demo Logins Gateway:   \x1b[4m\x1b[36mhttp://localhost:3000/login\x1b[0m');
    console.log('  ⚡ Proxied Backend API:     \x1b[4m\x1b[36mhttp://localhost:3000/api/v1\x1b[0m');
    console.log('  📖 Swagger Documentation:   \x1b[4m\x1b[36mhttp://localhost:3000/docs\x1b[0m');
    console.log('\x1b[36m%s\x1b[0m', '────────────────────────────────────────────────────────────────\n');
  }, 2000);
}

// Start polling
checkBackend();
