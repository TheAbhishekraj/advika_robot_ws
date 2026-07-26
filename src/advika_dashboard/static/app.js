/**
 * ADVIKA 3.0 — Dashboard Frontend (app.js)
 * SocketIO client + Canvas rendering + Keyboard teleop
 */

const socket = io();

// ── State ────────────────────────────────────────────────────────────────────
let state = {
  linear_x: 0, angular_z: 0,
  e_stop: false, auto_mode: false,
  robot_x: 0, robot_y: 0, robot_yaw: 0,
  battery: 100,
  fps_h: 0, fps_f: 0,
};

let speed  = 5;       // 1–10
let kP     = 0.05 * speed; // drive multiplier

// ── Canvas refs ──────────────────────────────────────────────────────────────
const canvasHorizon = document.getElementById('canvas-horizon');
const canvasFloor   = document.getElementById('canvas-floor');
const canvasLidar   = document.getElementById('canvas-lidar');
const canvasTraj    = document.getElementById('canvas-traj');
const ctxH  = canvasHorizon.getContext('2d');
const ctxF  = canvasFloor.getContext('2d');
const ctxL  = canvasLidar.getContext('2d');
const ctxT  = canvasTraj.getContext('2d');

// ── Chart.js instances ───────────────────────────────────────────────────────
let accelChart, gyroChart;

// ── Demo data generators ─────────────────────────────────────────────────────
let demoTick = 0;
let lidarRanges = Array(360).fill(3.0);

function tickDemo() {
  demoTick += 0.05;
  // Simulate LiDAR
  lidarRanges = lidarRanges.map((r, i) => {
    const base = 2.5 + 0.3 * Math.sin(i * 0.05 + demoTick);
    return Math.max(0.15, base + (Math.random() - 0.5) * 0.2);
  });
  // Simulate pose (circle)
  state.robot_x   = 1.5 * Math.cos(demoTick * 0.3);
  state.robot_y   = 1.5 * Math.sin(demoTick * 0.3);
  state.robot_yaw  = Math.atan2(state.robot_y, state.robot_x);
  state.battery   = Math.max(20, 100 - demoTick * 0.02);
}

function drawDemoCameras() {
  // Simulate horizon camera — gradient with noise
  const w = canvasHorizon.width, h = canvasHorizon.height;
  const grad = ctxH.createLinearGradient(0, 0, 0, h);
  grad.addColorStop(0,   `hsl(${200 + 20*Math.sin(demoTick)}, 60%, 20%)`);
  grad.addColorStop(0.5, `hsl(${220 + 15*Math.sin(demoTick*1.3)}, 40%, 15%)`);
  grad.addColorStop(1,   `hsl(${180 + 10*Math.sin(demoTick*0.7)}, 50%, 8%)`);
  ctxH.fillStyle = grad;
  ctxH.fillRect(0, 0, w, h);

  // Add fake "room" lines
  ctxH.strokeStyle = 'rgba(255,255,255,0.08)';
  ctxH.lineWidth = 1;
  for (let i = 0; i < 8; i++) {
    ctxH.beginPath();
    ctxH.moveTo(w * (i/8), 0);
    ctxH.lineTo(w * (i/8), h);
    ctxH.stroke();
  }
  // Some fake objects
  ctxH.fillStyle = 'rgba(255,180,80,0.15)';
  ctxH.beginPath();
  ctxH.arc(w * 0.6, h * 0.3, 20, 0, Math.PI * 2);
  ctxH.fill();
  ctxH.fillStyle = 'rgba(80,200,255,0.12)';
  ctxH.fillRect(w * 0.2, h * 0.5, 40, 60);

  // Simulate floor camera — checkerboard floor
  const fw = canvasFloor.width, fh = canvasFloor.height;
  const floorGrad = ctxF.createLinearGradient(0, 0, 0, fh);
  floorGrad.addColorStop(0, '#1a1a2e');
  floorGrad.addColorStop(1, '#0d0d1a');
  ctxF.fillStyle = floorGrad;
  ctxF.fillRect(0, 0, fw, fh);

  const ts = 30;
  for (let y = 0; y < fh + ts; y += ts) {
    for (let x = 0; x < fw + ts; x += ts) {
      const bright = ((x / ts + y / ts + Math.floor(demoTick)) % 2 === 0);
      ctxF.fillStyle = bright ? 'rgba(255,255,255,0.07)' : 'rgba(0,0,0,0)';
      ctxF.fillRect(x, y, ts, ts);
    }
  }
}

// ── LiDAR Renderer ──────────────────────────────────────────────────────────
function drawLidar(ranges) {
  const w = canvasLidar.width, h = canvasLidar.height;
  const cx = w/2, cy = h/2, maxR = Math.min(w, h)/2 - 4;

  ctxL.clearRect(0, 0, w, h);

  // Background ring
  for (let r = 1; r <= 4; r++) {
    ctxL.beginPath();
    ctxL.arc(cx, cy, maxR * r/4, 0, Math.PI * 2);
    ctxL.strokeStyle = `rgba(255,255,255,0.06)`;
    ctxL.lineWidth = 1;
    ctxL.stroke();
  }

  // Color gradient for intensity
  const grad = ctxL.createRadialGradient(cx, cy, 0, cx, cy, maxR);
  grad.addColorStop(0, 'rgba(59,130,246,0.3)');
  grad.addColorStop(1, 'rgba(16,185,129,0.05)');

  // Draw scan points
  const step = Math.floor(ranges.length / 360);
  for (let i = 0; i < 360; i++) {
    const r = ranges[i * step] || 3.0;
    const norm = Math.min(r / 5.0, 1.0);
    const angle = (i - 90) * Math.PI / 180;
    const px = cx + Math.cos(angle) * norm * maxR;
    const py = cy + Math.sin(angle) * norm * maxR;

    const hue = 120 * (1 - norm);
    ctxL.beginPath();
    ctxL.arc(px, py, 2, 0, Math.PI * 2);
    ctxL.fillStyle = `hsla(${hue}, 80%, 60%, 0.9)`;
    ctxL.fill();
  }

  // Center dot
  ctxL.beginPath();
  ctxL.arc(cx, cy, 3, 0, Math.PI * 2);
  ctxL.fillStyle = '#fff';
  ctxL.fill();

  // Range label
  const min = Math.min(...ranges.slice(0, 360)).toFixed(2);
  const avg = (ranges.slice(0, 360).reduce((a,b)=>a+b,0)/360).toFixed(2);
  const max = Math.max(...ranges.slice(0, 360)).toFixed(2);
  document.getElementById('lidar-min').textContent = min + 'm';
  document.getElementById('lidar-avg').textContent = avg + 'm';
  document.getElementById('lidar-max').textContent = max + 'm';
  document.getElementById('lidar-range').textContent = (maxR * 5 / maxR).toFixed(1) + 'm';
}

// ── Trajectory Renderer ─────────────────────────────────────────────────────
const trajPoints = [];

function drawTrajectory() {
  const w = canvasTraj.width, h = canvasTraj.height;
  const scale = 30; // pixels per meter
  const cx = w/2, cy = h/2;

  ctxT.clearRect(0, 0, w, h);

  // Grid
  ctxT.strokeStyle = 'rgba(255,255,255,0.05)';
  ctxT.lineWidth = 1;
  for (let x = 0; x < w; x += 30) {
    ctxT.beginPath(); ctxT.moveTo(x, 0); ctxT.lineTo(x, h); ctxT.stroke();
  }
  for (let y = 0; y < h; y += 30) {
    ctxT.beginPath(); ctxT.moveTo(0, y); ctxT.lineTo(w, y); ctxT.stroke();
  }
  // Axes
  ctxT.strokeStyle = 'rgba(255,255,255,0.15)';
  ctxT.beginPath(); ctxT.moveTo(0, cy); ctxT.lineTo(w, cy); ctxT.stroke();
  ctxT.beginPath(); ctxT.moveTo(cx, 0); ctxT.lineTo(cx, h); ctxT.stroke();

  // Store point
  const px = cx + state.robot_x * scale;
  const py = cy - state.robot_y * scale;
  trajPoints.push({x: px, y: py, yaw: state.robot_yaw});
  if (trajPoints.length > 500) trajPoints.shift();

  // Trail
  if (trajPoints.length > 1) {
    ctxT.beginPath();
    ctxT.moveTo(trajPoints[0].x, trajPoints[0].y);
    for (const p of trajPoints) ctxT.lineTo(p.x, p.y);
    ctxT.strokeStyle = 'rgba(59,130,246,0.4)';
    ctxT.lineWidth = 2;
    ctxT.stroke();
  }

  // Robot dot + heading
  ctxT.beginPath();
  ctxT.arc(px, py, 5, 0, Math.PI * 2);
  ctxT.fillStyle = '#3b82f6';
  ctxT.fill();

  ctxT.strokeStyle = '#fff';
  ctxT.lineWidth = 1.5;
  ctxT.beginPath();
  ctxT.moveTo(px, py);
  ctxT.lineTo(px + 12 * Math.cos(state.robot_yaw), py - 12 * Math.sin(state.robot_yaw));
  ctxT.stroke();
}

// ── IMU Charts ──────────────────────────────────────────────────────────────
function initCharts() {
  const commonOpts = {
    animation: false,
    responsive: true,
    scales: { x: { display: false }, y: { display: true, grid: { color: 'rgba(255,255,255,0.05)' }, ticks: { color: '#6b7280', font: { size: 9 } } } },
    plugins: { legend: { display: false } }
  };

  const newData = () => Array(40).fill(0);

  accelChart = new Chart(document.getElementById('chart-accel'), {
    type: 'line',
    data: {
      labels: Array(40).fill(''),
      datasets: [
        { data: newData(), borderColor: '#ef4444', borderWidth: 1.5, pointRadius: 0, tension: 0.4, label: 'AX' },
        { data: newData(), borderColor: '#10b981', borderWidth: 1.5, pointRadius: 0, tension: 0.4, label: 'AY' },
        { data: newData(), borderColor: '#3b82f6', borderWidth: 1.5, pointRadius: 0, tension: 0.4, label: 'AZ' },
      ]
    },
    options: { ...commonOpts, scales: { ...commonOpts.scales, y: { ...commonOpts.scales.y, title: { display: true, text: 'm/s²', color: '#6b7280', font: { size: 8 } } } } }
  });

  gyroChart = new Chart(document.getElementById('chart-gyro'), {
    type: 'line',
    data: {
      labels: Array(40).fill(''),
      datasets: [
        { data: newData(), borderColor: '#ef4444', borderWidth: 1.5, pointRadius: 0, tension: 0.4 },
        { data: newData(), borderColor: '#10b981', borderWidth: 1.5, pointRadius: 0, tension: 0.4 },
        { data: newData(), borderColor: '#3b82f6', borderWidth: 1.5, pointRadius: 0, tension: 0.4 },
      ]
    },
    options: { ...commonOpts, scales: { ...commonOpts.scales, y: { ...commonOpts.scales.y, title: { display: true, text: 'rad/s', color: '#6b7280', font: { size: 8 } } } } }
  });
}

let accelBuf = { ax: [0], ay: [0], az: [9.8], gx: [0], gy: [0], gz: [0] };

function updateIMUCharts(data) {
  const push = (buf, val) => { buf.push(val); if (buf.length > 40) buf.shift(); };

  push(accelBuf.ax, data.ax);
  push(accelBuf.ay, data.ay);
  push(accelBuf.az, data.az);
  push(accelBuf.gx, data.gx);
  push(accelBuf.gy, data.gy);
  push(accelBuf.gz, data.gz);

  accelChart.data.datasets[0].data = [...accelBuf.ax];
  accelChart.data.datasets[1].data = [...accelBuf.ay];
  accelChart.data.datasets[2].data = [...accelBuf.az];
  accelChart.update('none');

  gyroChart.data.datasets[0].data = [...accelBuf.gx];
  gyroChart.data.datasets[1].data = [...accelBuf.gy];
  gyroChart.data.datasets[2].data = [...accelBuf.gz];
  gyroChart.update('none');
}

// ── Joystick ────────────────────────────────────────────────────────────────
let joyActive = false, joyX = 0, joyY = 0;

function setupJoystick() {
  const stick   = document.getElementById('joystick-stick');
  const joystickBase = document.querySelector('.joystick-base');

  const onMove = (clientX, clientY) => {
    if (!joyActive) return;
    const rect = joystickBase.getBoundingClientRect();
    const cx = rect.left + rect.width/2;
    const cy = rect.top  + rect.height/2;
    const maxR = rect.width/2 - 18;

    let dx = clientX - cx, dy = clientY - cy;
    const dist = Math.sqrt(dx*dx + dy*dy);
    if (dist > maxR) { dx = dx/dist*maxR; dy = dy/dist*maxR; }

    stick.style.transform = `translate(${dx}px, ${dy}px)`;
    joyX = dx/maxR;
    joyY = -dy/maxR;

    const lx = +(joyY * speed * 0.05).toFixed(3);
    const az = +(joyX * speed * 0.1).toFixed(3);
    document.getElementById('jx-out').textContent = lx;
    document.getElementById('jz-out').textContent = az;

    socket.emit('cmd_vel', { linear_x: lx, angular_z: az });
  };

  const onEnd = () => {
    joyActive = false;
    stick.style.transform = '';
    joyX = joyY = 0;
    document.getElementById('jx-out').textContent = '0.00';
    document.getElementById('jz-out').textContent = '0.00';
    socket.emit('cmd_vel', { linear_x: 0, angular_z: 0 });
  };

  joystickBase.addEventListener('mousedown',  e => { joyActive = true; onMove(e.clientX, e.clientY); });
  joystickBase.addEventListener('touchstart', e => { joyActive = true; onMove(e.touches[0].clientX, e.touches[0].clientY); e.preventDefault(); }, { passive: false });
  document.addEventListener('mousemove',  e => onMove(e.clientX, e.clientY));
  document.addEventListener('touchmove',  e => { if (joyActive) { onMove(e.touches[0].clientX, e.touches[0].clientY); e.preventDefault(); } }, { passive: false });
  document.addEventListener('mouseup',  onEnd);
  document.addEventListener('touchend', onEnd);
}

// ── Keyboard Teleop ─────────────────────────────────────────────────────────
const KEY_MAP = { i: [0.05,0], m: [-0.05,0], j: [0,0.1], l: [0,-0.1], k: [0,0] };
const keys = {};

function setupKeyboard() {
  document.addEventListener('keydown', e => {
    if (KEY_MAP[e.key]) keys[e.key] = true;
  });
  document.addEventListener('keyup', e => {
    if (KEY_MAP[e.key]) keys[e.key] = false;
  });

  setInterval(() => {
    let lx = 0, az = 0;
    for (const [k, [a, b]] of Object.entries(KEY_MAP)) {
      if (keys[k]) { lx += a * speed * 0.5; az += b * speed * 0.5; }
    }
    socket.emit('cmd_vel', { linear_x: Math.max(-0.5, Math.min(0.5, lx)), angular_z: Math.max(-1, Math.min(1, az)) });
  }, 80);
}

// ── Direction Buttons ───────────────────────────────────────────────────────
function setupDirBtns() {
  const btns = {
    'btn-forward': [0.05, 0],
    'btn-back':    [-0.05, 0],
    'btn-left':    [0, 0.1],
    'btn-right':   [0, -0.1],
    'btn-stop':    [0, 0],
  };
  for (const [id, [lx, az]] of Object.entries(btns)) {
    const el = document.getElementById(id);
    if (!el) continue;
    const set = () => socket.emit('cmd_vel', { linear_x: lx * speed * 0.3, angular_z: az * speed * 0.3 });
    el.addEventListener('mousedown',  set);
    el.addEventListener('touchstart', e => { set(); e.preventDefault(); }, { passive: false });
    el.addEventListener('mouseup',  () => socket.emit('cmd_vel', { linear_x: 0, angular_z: 0 }));
    el.addEventListener('mouseleave', () => socket.emit('cmd_vel', { linear_x: 0, angular_z: 0 }));
  }
}

// ── UI Event Bindings ───────────────────────────────────────────────────────
function setupUI() {
  // Speed slider
  const slider = document.getElementById('speed-slider');
  const sval   = document.getElementById('speed-val');
  slider.addEventListener('input', () => {
    speed = +slider.value;
    sval.textContent = speed;
    kP = 0.05 * speed;
  });

  // E-Stop
  document.getElementById('btn-estop').addEventListener('click', () => {
    socket.emit('e_stop');
    state.e_stop = true;
  });
  document.getElementById('btn-estop-reset').addEventListener('click', () => {
    socket.emit('e_stop_reset');
    state.e_stop = false;
  });

  // Auto/Manual
  document.getElementById('btn-auto').addEventListener('click', () => {
    socket.emit('auto_mode', { enabled: true });
    state.auto_mode = true;
  });
  document.getElementById('btn-manual').addEventListener('click', () => {
    socket.emit('auto_mode', { enabled: false });
    state.auto_mode = false;
  });

  // Camera tab switching
  document.getElementById('tab-sim').addEventListener('click', () => {
    document.getElementById('tab-sim').classList.add('active');
    document.getElementById('tab-raw').classList.remove('active');
  });
}

// ── Status Update ───────────────────────────────────────────────────────────
function updateUI() {
  // Pose
  document.getElementById('pose-x').textContent   = state.robot_x.toFixed(3);
  document.getElementById('pose-y').textContent   = state.robot_y.toFixed(3);
  document.getElementById('pose-yaw').textContent = (state.robot_yaw * 180/Math.PI).toFixed(1) + '°';

  // Battery
  const bat = state.battery;
  document.getElementById('battery-bar').style.width  = bat + '%';
  document.getElementById('battery-bar').className   = 'battery-bar-inner' + (bat < 20 ? ' low' : bat < 50 ? ' mid' : '');
  document.getElementById('battery-pct').textContent = bat.toFixed(0) + '%';

  // Lights
  document.getElementById('light-connected').className = 'light ' + (state.connected === false ? 'off' : 'green');
  document.getElementById('light-auto').className      = 'light ' + (state.auto_mode ? 'blue' : 'off');
  document.getElementById('light-estop').className     = 'light ' + (state.e_stop ? 'red' : 'off');

  // FPS
  document.getElementById('fps-horizon').textContent = state.fps_h + ' fps';
  document.getElementById('fps-floor').textContent   = state.fps_f + ' fps';

  // Status bar
  const mode = state.e_stop ? 'E-STOP' : state.auto_mode ? 'AUTO' : 'MANUAL';
  document.getElementById('status-msg').textContent = `Mode: ${mode} | Position: (${state.robot_x.toFixed(2)}, ${state.robot_y.toFixed(2)}) | Yaw: ${(state.robot_yaw*180/Math.PI).toFixed(1)}°`;
}

// ── Clock ───────────────────────────────────────────────────────────────────
function updateClock() {
  const now = new Date();
  document.getElementById('clock').textContent =
    now.toLocaleTimeString() + ' | ' + now.toLocaleDateString();
}

// ── Socket events ───────────────────────────────────────────────────────────
socket.on('connect', () => {
  console.log('[Dashboard] Connected to server');
  document.getElementById('light-connected').className = 'light green';
});

socket.on('disconnect', () => {
  document.getElementById('light-connected').className = 'light off';
});

socket.on('telemetry', data => {
  Object.assign(state, data);
  updateUI();
  drawLidar(lidarRanges);
  drawTrajectory();
});

socket.on('cmd_ack', data => {
  if (data.e_stop !== undefined) state.e_stop = data.e_stop;
});

socket.on('camera_frame', data => {
  const canvas = data.camera === 'horizon' ? canvasHorizon : canvasFloor;
  const ctx    = data.camera === 'horizon' ? ctxH : ctxF;
  const img    = new Image();
  img.onload = () => {
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
  };
  img.src = 'data:image/jpeg;base64,' + data.data;
});

socket.on('imu_data', data => {
  updateIMUCharts(data);
});

// ── Demo mode render loop ──────────────────────────────────────────────────
function renderLoop() {
  tickDemo();
  drawDemoCameras();
  drawLidar(lidarRanges);
  drawTrajectory();
  updateClock();
  requestAnimationFrame(renderLoop);
}

// ── Init ───────────────────────────────────────────────────────────────────
function init() {
  initCharts();
  setupJoystick();
  setupKeyboard();
  setupDirBtns();
  setupUI();

  // Start render loop (demo mode)
  renderLoop();

  document.getElementById('status-msg').textContent = 'ADVIKA 3.0 Dashboard Ready (Demo Mode)';
}

window.addEventListener('load', init);