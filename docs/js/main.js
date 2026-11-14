/**
 * F1 Paddock Insights - Interactive Showcase Script
 * Features: Mobile Nav, Video Player & Simulation Engine, Interactive Telemetry Gauge, Code Copying
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initVideoPlayerAndSimulation();
  initLiveTelemetrySimulator();
  initCopyCodeButtons();
  initAppLinkProtocolHandler();
});

function initAppLinkProtocolHandler() {
  // If docs/index.html is opened directly via file://, route App links to http://localhost:5000
  if (window.location.protocol === 'file:') {
    document.querySelectorAll('.app-link-main').forEach(el => {
      el.href = 'http://localhost:5000/';
      el.title = 'Abrir Servidor Flask Local (http://localhost:5000)';
    });
  }
}

/* ==========================================================================
   1. MOBILE NAVIGATION DRAWER
   ========================================================================== */
function initMobileNav() {
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const navDrawer = document.getElementById('mobile-nav-drawer');
  const drawerLinks = document.querySelectorAll('.mobile-nav-link');

  if (!hamburgerBtn || !navDrawer) return;

  hamburgerBtn.addEventListener('click', () => {
    navDrawer.classList.toggle('open');
    const isOpen = navDrawer.classList.contains('open');
    hamburgerBtn.setAttribute('aria-expanded', isOpen);
  });

  drawerLinks.forEach(link => {
    link.addEventListener('click', () => {
      navDrawer.classList.remove('open');
      hamburgerBtn.setAttribute('aria-expanded', 'false');
    });
  });

  // Close on outside click
  document.addEventListener('click', (e) => {
    if (navDrawer.classList.contains('open') && 
        !navDrawer.contains(e.target) && 
        !hamburgerBtn.contains(e.target)) {
      navDrawer.classList.remove('open');
      hamburgerBtn.setAttribute('aria-expanded', 'false');
    }
  });
}

/* ==========================================================================
   2. VIDEO PLAYER & INTERACTIVE DEMO SIMULATOR
   ========================================================================== */
function initVideoPlayerAndSimulation() {
  const modeVideoBtn = document.getElementById('mode-video-btn');
  const modeSimBtn = document.getElementById('mode-sim-btn');
  const videoWrapper = document.getElementById('video-native-wrap');
  const simWrapper = document.getElementById('video-sim-wrap');
  const html5Video = document.getElementById('f1-demo-video');
  const chapterButtons = document.querySelectorAll('.chapter-card-btn');

  // Simulation step state
  const simSteps = [
    {
      time: "00:00",
      hud: "SYS // INIT // 2026.11.14",
      title: "1. Cockpit & Interface Mobile-First",
      desc: "Visão geral da interface responsiva construída especificamente para uso em smartphones com tema de Pit Wall da Fórmula 1.",
      widget: "🏎️ Grid 2026 Conectado &middot; Datalist de Pilotos Ativo",
      progress: 15
    },
    {
      time: "00:35",
      hud: "API // OPENF1.ORG // DRIVERS",
      title: "2. Consumo de API REST (OpenF1)",
      desc: "Busca em tempo real de informações cadastrais: numeração (#12), país (ITA), escuderia oficial (Mercedes-AMG) e foto em alta definição.",
      widget: "📡 Payload JSON 200 OK &middot; Foto Oficial Carregada",
      progress: 35
    },
    {
      time: "01:10",
      hud: "SCRAPING // BEAUTIFULSOUP // GP",
      title: "3. Web Scraping no Grande Prêmio",
      desc: "Extração automatizada de notícias recentes sobre o piloto buscado e raspagem da tabela oficial de classificação de pilotos do mundial.",
      widget: "🌐 BeautifulSoup4 &middot; Notícias de Bastidores Filtradas",
      progress: 55
    },
    {
      time: "01:50",
      hud: "AI // GOOGLE GEMINI // PIT WALL COMMS",
      title: "4. Rádio Pit Wall com Google Gemini",
      desc: "IA Generativa recebe dados de telemetria, grid e notícias, sintetizando um rádio de corrida em 3 personalidades: Engenheiro, Narrador ou Corneta.",
      widget: "🧠 SDK google-genai &middot; gemini-3.5-flash-lite",
      progress: 75
    },
    {
      time: "02:30",
      hud: "RULES // CHAMPIONSHIP ENDED // TITLE 100%",
      title: "5. Velocímetro: Andrea Kimi Antonelli Campeão (100%)",
      desc: "Campeonato encerrado! O velocímetro reflete o campeão consagrado com 100% de probabilidade confirmada, e 0% para os demais competidores.",
      widget: "⚡ Antonelli #1 (100% Campeão) vs Verstappen #2 (0% Vice)",
      progress: 90
    },
    {
      time: "03:10",
      hud: "STANDINGS // GP-STANDINGS // 2026",
      title: "6. Tabela Geral de Classificação 2026",
      desc: "Exibição da pontuação oficial acumulada de todos os 20+ pilotos com design de alta performance e badges das equipes.",
      widget: "🏆 Antonelli 390 pts &middot; Verstappen 279 pts &middot; Russell 262 pts",
      progress: 100
    }
  ];

  let currentStepIdx = 0;
  let isSimPlaying = false;
  let simTimer = null;

  // Tab toggling
  if (modeVideoBtn && modeSimBtn && videoWrapper && simWrapper) {
    modeVideoBtn.addEventListener('click', () => {
      modeVideoBtn.classList.add('active');
      modeSimBtn.classList.remove('active');
      videoWrapper.style.display = 'block';
      simWrapper.style.display = 'none';
      stopSimulation();
      if (html5Video) html5Video.play().catch(() => {});
    });

    modeSimBtn.addEventListener('click', () => {
      modeSimBtn.classList.add('active');
      modeVideoBtn.classList.remove('active');
      videoWrapper.style.display = 'none';
      simWrapper.style.display = 'flex';
      if (html5Video) html5Video.pause();
      renderSimStep(currentStepIdx);
    });
  }

  // Chapter buttons click
  chapterButtons.forEach((btn, idx) => {
    btn.addEventListener('click', () => {
      chapterButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Switch to simulation or video seek
      if (modeSimBtn && modeSimBtn.classList.contains('active')) {
        currentStepIdx = idx % simSteps.length;
        renderSimStep(currentStepIdx);
      } else if (html5Video) {
        const timeSecs = [0, 35, 70, 110, 150, 190][idx] || 0;
        if (html5Video.duration && timeSecs >= html5Video.duration) {
          html5Video.currentTime = Math.min(timeSecs, html5Video.duration - 1);
        } else {
          html5Video.currentTime = timeSecs;
        }
        html5Video.play().catch(() => {});
      }
    });
  });

  // Simulation controls
  const playTrigger = document.getElementById('sim-play-trigger');
  if (playTrigger) {
    playTrigger.addEventListener('click', () => {
      if (isSimPlaying) {
        stopSimulation();
      } else {
        startSimulation();
      }
    });
  }

  function renderSimStep(idx) {
    const step = simSteps[idx];
    if (!step) return;

    const hudEl = document.getElementById('sim-hud-text');
    const titleEl = document.getElementById('sim-step-title');
    const descEl = document.getElementById('sim-step-desc');
    const widgetEl = document.getElementById('sim-widget-text');
    const timeEl = document.getElementById('sim-time-display');
    const progressFill = document.getElementById('sim-progress-fill');

    if (hudEl) hudEl.textContent = step.hud;
    if (titleEl) titleEl.textContent = step.title;
    if (descEl) descEl.textContent = step.desc;
    if (widgetEl) widgetEl.innerHTML = step.widget;
    if (timeEl) timeEl.textContent = step.time + " / 03:30";
    if (progressFill) progressFill.style.width = step.progress + "%";

    // Highlight active chapter
    chapterButtons.forEach((b, i) => {
      b.classList.toggle('active', i === idx);
    });
  }

  function startSimulation() {
    isSimPlaying = true;
    if (playTrigger) playTrigger.textContent = '⏸️';
    
    simTimer = setInterval(() => {
      currentStepIdx = (currentStepIdx + 1) % simSteps.length;
      renderSimStep(currentStepIdx);
      if (currentStepIdx === 0) {
        // One loop done
      }
    }, 4500);
  }

  function stopSimulation() {
    isSimPlaying = false;
    if (playTrigger) playTrigger.textContent = '▶️';
    if (simTimer) clearInterval(simTimer);
  }

  // Initial render of step 0
  renderSimStep(0);
}

/* ==========================================================================
   3. LIVE TELEMETRY INTERACTIVE SIMULATOR (ANDREA KIMI ANTONELLI & VERSTAPPEN)
   ========================================================================== */
function initLiveTelemetrySimulator() {
  const pilotsData = {
    antonelli: {
      nome: "Andrea Kimi Antonelli",
      equipe: "Mercedes-AMG Petronas F1 Team",
      numero: "#12",
      pais: "ITA",
      posicao: "1º no Mundial",
      pontos: "390 pts",
      chance: 100,
      cor: "#00a19c",
      alertaLabel: "CAMPEÃO MATEMÁTICO // TÍTULO ANTECIPADO",
      statusClass: "champion",
      descChance: "Matematicamente Campeão Mundial! Vantagem de 111 pts supera os 78 pts restantes em disputa (3 GPs x 26 pts).",
      radioTitle: "ENGENHARIA DE PISTA MERCEDES",
      radioText: "\"Kimi, P1 confirmado no campeonato mundial. Você é o novo campeão do mundo antecipado! Vantagem matemática absoluta!\""
    },
    verstappen: {
      nome: "Max Verstappen",
      equipe: "Oracle Red Bull Racing",
      numero: "#1",
      pais: "NED",
      posicao: "2º no Mundial",
      pontos: "279 pts",
      chance: 0,
      cor: "#3671c6",
      alertaLabel: "VICE-LÍDER // TÍTULO MATEMATICAMENTE FINALIZADO",
      statusClass: "ended",
      descChance: "Matematicamente sem chances de título. Máximo alcançável: 357 pts (Líder já possui 390 pts em 3 corridas restantes).",
      radioTitle: "ENGENHARIA RED BULL RACING",
      radioText: "\"Max, mantemos a vice-liderança do mundial com 279 pontos. Foco em garantir o P2 nas corridas finais da temporada.\""
    },
    russell: {
      nome: "George Russell",
      equipe: "Mercedes-AMG Petronas F1 Team",
      numero: "#63",
      pais: "GBR",
      posicao: "3º no Mundial",
      pontos: "262 pts",
      chance: 0,
      cor: "#00a19c",
      alertaLabel: "PÓDIO DO MUNDIAL (3º) // TÍTULO INALCANÇÁVEL",
      statusClass: "ended",
      descChance: "Título matematicamente fora de alcance (máx. 340 pts vs 390 pts do líder). Disputa focada nas posições do pódio geral.",
      radioTitle: "ENGENHARIA MERCEDES-AMG",
      radioText: "\"George, P3 no campeonato com 262 pontos. Dobradinha da equipe no pódio do mundial de pilotos!\""
    },
    hamilton: {
      nome: "Lewis Hamilton",
      equipe: "Scuderia Ferrari HP",
      numero: "#44",
      pais: "GBR",
      posicao: "4º no Mundial",
      pontos: "261 pts",
      chance: 0,
      cor: "#e80020",
      alertaLabel: "4º NO MUNDIAL // DISPUTA POR PÓDIO",
      statusClass: "ended",
      descChance: "Título fora de alcance matemático (máx. 339 pts vs 390 pts do líder). 261 pontos somados pela Ferrari na briga pelo top 3.",
      radioTitle: "PIT WALL SCUDERIA FERRARI",
      radioText: "\"Lewis, corrida sólida. Estamos a apenas 1 ponto do P3 no campeonato mundial.\""
    },
    norris: {
      nome: "Lando Norris",
      equipe: "McLaren Formula 1 Team",
      numero: "#4",
      pais: "GBR",
      posicao: "6º no Mundial",
      pontos: "246 pts",
      chance: 0,
      cor: "#ff8000",
      alertaLabel: "6º NO MUNDIAL // DISPUTA POR PONTOS",
      statusClass: "ended",
      descChance: "Título matematicamente fora de alcance (máx. 324 pts vs 390 pts do líder). Foco na zona de pontuação da McLaren.",
      radioTitle: "ENGENHARIA MCLAREN F1",
      radioText: "\"Lando, P6 consolidado. Vamos continuar pontuando até a última etapa.\""
    }
  };

  const simPillButtons = document.querySelectorAll('.sim-pill-btn');
  const driverNameEl = document.getElementById('sim-driver-name');
  const driverTeamEl = document.getElementById('sim-driver-team');
  const driverPosEl = document.getElementById('sim-driver-pos');
  const driverPointsEl = document.getElementById('sim-driver-points');
  const gaugeFillEl = document.getElementById('sim-gauge-circle');
  const gaugePercentEl = document.getElementById('sim-gauge-percent');
  const gaugeStatusEl = document.getElementById('sim-gauge-status-text');
  const gaugeDescEl = document.getElementById('sim-gauge-desc-text');
  const radioCommsEl = document.getElementById('sim-radio-quote');
  const radioTitleEl = document.getElementById('sim-radio-channel-name');

  const circumference = 251.3; // 2 * PI * 40 (r=40 in SVG)

  simPillButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      simPillButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const pilotKey = btn.getAttribute('data-pilot');
      const data = pilotsData[pilotKey];
      if (!data) return;

      // Update text fields
      if (driverNameEl) driverNameEl.textContent = data.nome;
      if (driverTeamEl) {
        driverTeamEl.textContent = `${data.equipe} (${data.pais}) &bull; Carro ${data.numero}`;
        driverTeamEl.style.color = data.cor;
      }
      if (driverPosEl) driverPosEl.textContent = data.posicao;
      if (driverPointsEl) driverPointsEl.textContent = data.pontos;
      if (gaugePercentEl) gaugePercentEl.textContent = `${data.chance}%`;
      if (gaugeStatusEl) {
        gaugeStatusEl.textContent = data.alertaLabel;
        gaugeStatusEl.className = `sim-gauge-status ${data.statusClass}`;
      }
      if (gaugeDescEl) gaugeDescEl.textContent = data.descChance;
      if (radioCommsEl) radioCommsEl.textContent = data.radioText;
      if (radioTitleEl) radioTitleEl.textContent = data.radioTitle;

      // Animate circular gauge
      if (gaugeFillEl) {
        const offset = circumference - (data.chance / 100) * circumference;
        gaugeFillEl.style.strokeDashoffset = offset;
        gaugeFillEl.style.stroke = data.chance === 100 ? '#00e676' : '#64748b';
      }
    });
  });
}

/* ==========================================================================
   4. COPY CODE SNIPPETS HELPER
   ========================================================================== */
function initCopyCodeButtons() {
  const copyButtons = document.querySelectorAll('.copy-btn');

  copyButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-target');
      const codeEl = document.getElementById(targetId);
      if (!codeEl) return;

      const text = codeEl.innerText || codeEl.textContent;
      navigator.clipboard.writeText(text).then(() => {
        const originalText = btn.textContent;
        btn.textContent = 'Copiado! ✓';
        btn.style.background = '#00e676';
        btn.style.color = '#000000';

        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.background = '';
          btn.style.color = '';
        }, 2000);
      }).catch(err => {
        console.error('Falha ao copiar:', err);
      });
    });
  });
}
