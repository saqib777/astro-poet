// ASTRO POET — atmospheric background.
// Three depth layers of stars (parallax), a slow nebula glow,
// and the occasional comet drifting through. Built for presence,
// not just a dark backdrop with dots.
(function () {
  const canvas = document.getElementById('starfield');
  if (!canvas) return;
  const ctx = canvas.getContext ? canvas.getContext('2d') : null;
  if (!ctx) return;
  const reduceMotion = window.matchMedia
    ? window.matchMedia('(prefers-reduced-motion: reduce)').matches
    : false;

  let w, h, dpr;
  let layers = [];
  let comets = [];
  let nebulae = [];

  const LAYER_CONFIG = [
    { count: 0.00010, rMin: 0.4, rMax: 0.9, alphaMin: 0.15, alphaMax: 0.35, speed: 0.008, twinkle: 0.0005 },
    { count: 0.00007, rMin: 0.7, rMax: 1.5, alphaMin: 0.30, alphaMax: 0.55, speed: 0.018, twinkle: 0.0009 },
    { count: 0.00004, rMin: 1.1, rMax: 2.2, alphaMin: 0.55, alphaMax: 0.95, speed: 0.034, twinkle: 0.0014 },
  ];

  const NEBULA_COLORS = [
    [88, 48, 120],
    [120, 40, 90],
    [40, 60, 110],
  ];

  function makeLayer(cfg) {
    const count = Math.max(18, Math.floor(w * h * cfg.count));
    return {
      cfg,
      stars: Array.from({ length: count }, () => ({
        x: Math.random() * w,
        y: Math.random() * h,
        r: cfg.rMin + Math.random() * (cfg.rMax - cfg.rMin),
        baseAlpha: cfg.alphaMin + Math.random() * (cfg.alphaMax - cfg.alphaMin),
        phase: Math.random() * Math.PI * 2,
        twinkleSpeed: cfg.twinkle * (0.6 + Math.random() * 0.8),
      })),
    };
  }

  function makeNebulae() {
    const count = 2;
    return Array.from({ length: count }, (_, i) => {
      const c = NEBULA_COLORS[i % NEBULA_COLORS.length];
      return {
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.max(w, h) * (0.28 + Math.random() * 0.16),
        color: c,
        baseAlpha: 0.025 + Math.random() * 0.025,
        phase: Math.random() * Math.PI * 2,
        speed: 0.00006 + Math.random() * 0.00004,
        dx: (Math.random() - 0.5) * 0.01,
        dy: (Math.random() - 0.5) * 0.01,
      };
    });
  }

  function spawnComet() {
    const fromLeft = Math.random() > 0.5;
    const y = Math.random() * h * 0.6;
    comets.push({
      x: fromLeft ? -60 : w + 60,
      y,
      vx: (fromLeft ? 1 : -1) * (1.4 + Math.random() * 1.1),
      vy: 0.5 + Math.random() * 0.4,
      len: 90 + Math.random() * 70,
      life: 0,
      maxLife: 140 + Math.random() * 60,
      alpha: 0,
    });
  }

  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    w = window.innerWidth;
    h = window.innerHeight;
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    layers = LAYER_CONFIG.map(makeLayer);
    nebulae = makeNebulae();
  }

  function drawNebulae(t) {
    for (const n of nebulae) {
      const pulse = reduceMotion ? 1 : 0.85 + 0.15 * Math.sin(t * n.speed + n.phase);
      const grad = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r);
      const [r, g, b] = n.color;
      grad.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${n.baseAlpha * pulse})`);
      grad.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0)`);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, w, h);
      if (!reduceMotion) {
        n.x += n.dx;
        n.y += n.dy;
        if (n.x < -n.r * 0.3) n.x = w + n.r * 0.3;
        if (n.x > w + n.r * 0.3) n.x = -n.r * 0.3;
        if (n.y < -n.r * 0.3) n.y = h + n.r * 0.3;
        if (n.y > h + n.r * 0.3) n.y = -n.r * 0.3;
      }
    }
  }

  function drawStars(t) {
    for (const layer of layers) {
      const { cfg, stars } = layer;
      for (const s of stars) {
        const twinkle = reduceMotion ? 1 : 0.55 + 0.45 * Math.sin(t * s.twinkleSpeed + s.phase);
        ctx.globalAlpha = s.baseAlpha * twinkle;
        ctx.fillStyle = '#f3efe4';
        ctx.beginPath();
        ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
        ctx.fill();
        if (!reduceMotion) {
          s.y -= cfg.speed;
          if (s.y < -3) { s.y = h + 3; s.x = Math.random() * w; }
        }
      }
    }
    ctx.globalAlpha = 1;
  }

  function drawComets() {
    if (reduceMotion) return;
    if (Math.random() < 0.004 && comets.length < 2) spawnComet();

    comets = comets.filter(c => c.life < c.maxLife);
    for (const c of comets) {
      c.life++;
      c.x += c.vx;
      c.y += c.vy;
      const fadeIn = Math.min(1, c.life / 20);
      const fadeOut = Math.min(1, (c.maxLife - c.life) / 30);
      c.alpha = Math.min(fadeIn, fadeOut);

      const mag = Math.hypot(c.vx, c.vy);
      const tailX = c.x - (c.vx / mag) * c.len;
      const tailY = c.y - (c.vy / mag) * c.len;
      const grad = ctx.createLinearGradient(c.x, c.y, tailX, tailY);
      grad.addColorStop(0, `rgba(243, 239, 228, ${0.85 * c.alpha})`);
      grad.addColorStop(1, 'rgba(201, 168, 118, 0)');
      ctx.strokeStyle = grad;
      ctx.lineWidth = 1.4;
      ctx.beginPath();
      ctx.moveTo(c.x, c.y);
      ctx.lineTo(tailX, tailY);
      ctx.stroke();

      ctx.globalAlpha = c.alpha;
      ctx.fillStyle = '#f3efe4';
      ctx.beginPath();
      ctx.arc(c.x, c.y, 1.5, 0, Math.PI * 2);
      ctx.fill();
      ctx.globalAlpha = 1;
    }
  }

  function draw(t) {
    ctx.clearRect(0, 0, w, h);
    drawNebulae(t);
    drawStars(t);
    drawComets();
    if (!reduceMotion) requestAnimationFrame(draw);
  }

  resize();
  window.addEventListener('resize', resize);
  requestAnimationFrame(draw);
  if (reduceMotion) draw(0);
})();
