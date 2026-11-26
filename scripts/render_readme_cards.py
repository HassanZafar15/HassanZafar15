import base64
import html
import json
import os
import textwrap
from datetime import date, datetime, timedelta, timezone

STATIC = os.environ.get("STATIC", "0") == "1"

# --- Warm Paper & Ink Editorial Palette ---
PAPER = "#F6F3EC"
PAPER_ALT = "#EFEAE0"
BORDER = "#DDD6C7"
INK = "#171614"
INK_MUTED = "#6B655D"
INK_SUBTLE = "#9A9389"

BLUE = "#2255D4"
RED = "#C83E2B"
OCHRE = "#B88212"
GREEN = "#1F8A5B"

GRAPH_COLORS = {
    "NONE": "#EAE4D7",
    "FIRST_QUARTILE": "#C2D4FA",
    "SECOND_QUARTILE": "#7FA4F4",
    "THIRD_QUARTILE": "#3E71E6",
    "FOURTH_QUARTILE": "#1A44B8",
}

# --- Profile Content ---
PROFILE = {
    "first_name": "Hassan",
    "last_name": "Zafar",
    "role": "Senior Flutter Developer at Abacus Consulting",
    "bio": "5+ years shipping cross-platform mobile & web apps to millions of users.",
    "location": "ISLAMABAD, PK · PKT (UTC+5)",
    "status": "OPEN TO REMOTE & FREELANCE",
    "pills": ["FLUTTER & DART", "IOS · ANDROID · WEB", "BLOC · RIVERPOD · CI/CD"],
}

TILES = [
    {
        "filename": "tile-experience.svg",
        "eyebrow": "EXPERIENCE",
        "accent": BLUE,
        "count_target": 5,
        "count_suffix": "+",
        "unit": "YEARS",
        "subtitle": "Flutter · Dart · Cross-Platform",
        "cta": "VIEW LINKEDIN",
        "delay": 1.35,
    },
    {
        "filename": "tile-portfolio.svg",
        "eyebrow": "PORTFOLIO",
        "accent": RED,
        "count_target": 10,
        "count_suffix": "+",
        "unit": "SHIPPED APPS",
        "subtitle": "GovTech · SaaS · eSIM · Health",
        "cta": "HASSANZAFAR.NETLIFY.APP",
        "delay": 1.50,
    },
    {
        "filename": "tile-contact.svg",
        "eyebrow": "AVAILABILITY",
        "accent": OCHRE,
        "count_target": 24,
        "count_suffix": "h",
        "unit": "AVG REPLY",
        "subtitle": "Remote Roles & Freelance",
        "cta": "START A CONVERSATION",
        "delay": 1.65,
    },
]

FEATURED_WORK = [
    {
        "filename": "work-epads.svg",
        "category": "GOVERNMENT · WEB & MOBILE",
        "accent": GREEN,
        "title": "EPADS",
        "desc": "World Bank-funded PPRA system digitising Pakistan's public procurement lifecycle. Contributed to eprocure.gov.pk and the Flutter companion app.",
        "tags": ["Flutter", "REST APIs", "Firebase", "Live Web"],
        "delay": 1.90,
    },
    {
        "filename": "work-movingcrm.svg",
        "category": "FLUTTER WEB · AI SAAS",
        "accent": BLUE,
        "title": "MovingCRM",
        "desc": "AI-powered SaaS CRM for moving companies with lead pipelines, dispatch, payroll, and portals. Built the Flutter Web app and core dashboards.",
        "tags": ["Flutter Web", "CRM", "SaaS", "Dashboards"],
        "delay": 2.00,
    },
    {
        "filename": "work-tjwalnet.svg",
        "category": "TRAVEL & TELECOM",
        "accent": BLUE,
        "title": "Tjwalnet — Travel eSIM",
        "desc": "Region-aware eSIM system covering 70+ countries with in-app wallet and points-based payments. Handles complex telecom logic seamlessly.",
        "tags": ["Flutter", "Firebase", "PayPal", "iOS & Android"],
        "delay": 2.10,
    },
    {
        "filename": "work-quotes.svg",
        "category": "LIFESTYLE · 4.7★ · 10K+",
        "accent": RED,
        "title": "Quotes & Motivation",
        "desc": "Daily quotes and motivation app with 10K+ downloads and a 4.7★ rating — curated collections, shareable cards, favorites, and smart reminders.",
        "tags": ["Flutter", "10K+ Downloads", "Android"],
        "delay": 2.20,
    },
    {
        "filename": "work-guardtrack.svg",
        "category": "SECURITY OPS · 1K+",
        "accent": RED,
        "title": "GuardTrack & Staff",
        "desc": "Mission-critical security platform supporting 500+ officers with precise GPS geofencing and real-time monitoring under demanding field conditions.",
        "tags": ["GPS Geofencing", "Real-Time", "iOS & Android"],
        "delay": 2.30,
    },
    {
        "filename": "work-mymyo.svg",
        "category": "HEALTH TECH",
        "accent": OCHRE,
        "title": "My MYO — Therapy",
        "desc": "Clinical therapy platform featuring an interactive video exercise player and client appointment management bridging patients and therapists.",
        "tags": ["Video Player", "Scheduling", "iOS & Android"],
        "delay": 2.40,
    },
    {
        "filename": "work-surrey.svg",
        "category": "ENTERPRISE WORKFORCE",
        "accent": INK,
        "title": "Surrey Security Staff",
        "desc": "Enterprise-grade staff coordination system for large-scale security operations, compliance, workforce scheduling, live shift tools, and reporting.",
        "tags": ["Workforce", "Compliance", "iOS & Android"],
        "delay": 2.50,
    },
    {
        "filename": "work-buildingco.svg",
        "category": "CONSTRUCTION · FIELD OPS",
        "accent": OCHRE,
        "title": "09 Building Co",
        "desc": "Operations app for construction teams featuring job assignment, project tracking, employee workflows, PDF handoffs, and completion photos.",
        "tags": ["Construction", "Field Ops", "iOS & Android"],
        "delay": 2.60,
    },
]

# Core Tech Stack curated from hassanzafar.netlify.app & LinkedIn
TECH_STACK = [
    "Flutter", "Dart", "BLoC", "Riverpod",
    "Firebase", "REST APIs", "GraphQL", "Supabase",
    "SQLite", "WSO2", "TDD", "GitHub Actions",
]

EXPERIENCE = [
    ("2022 – Present", "Senior Flutter Developer", "Abacus Consulting"),
    ("2020 – 2022", "Flutter Developer", "Mobile Development"),
    ("2019 – 2020", "Junior Mobile Developer", "Getting Started"),
]


def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def load_font_css() -> str:
    """Embed subsetted WOFF fonts as base64 data URIs if present in fonts/."""
    font_map = [
        ("Instrument Serif", "fonts/instrument-serif-regular.woff", 400),
        ("Geist", "fonts/geist-regular.woff", 400),
        ("Geist", "fonts/geist-medium.woff", 500),
    ]
    rules = []
    for family, path, weight in font_map:
        if os.path.exists(path):
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("ascii")
            rules.append(
                f"@font-face{{font-family:'{family}';font-weight:{weight};"
                f"font-style:normal;src:url(data:font/woff;base64,{b64}) format('woff');}}"
            )
    return "\n".join(rules)


FONT_CSS = load_font_css()
SERIF = "'Instrument Serif', Georgia, 'Times New Roman', serif"
SANS = "'Geist', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace"


def load_contributions() -> dict:
    """Load fetched JSON or generate a realistic fallback for immediate local preview."""
    path = "data/contributions.json"
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    # Fallback preview dataset (replaced once fetch_contributions.py runs)
    today = date.today()
    start = today - timedelta(days=364)
    days = []
    for i in range(365):
        d = start + timedelta(days=i)
        c = (i * 7 + d.weekday() * 3) % 9 if d.weekday() < 5 and i % 3 != 0 else 0
        level = (
            "NONE" if c == 0 else
            "FIRST_QUARTILE" if c <= 2 else
            "SECOND_QUARTILE" if c <= 4 else
            "THIRD_QUARTILE" if c <= 6 else
            "FOURTH_QUARTILE"
        )
        days.append({"date": d.isoformat(), "count": c, "level": level})

    monthly_map = {}
    for d in days:
        m = d["date"][:7]
        monthly_map[m] = monthly_map.get(m, 0) + d["count"]
    monthly = [{"month": k, "count": v} for k, v in sorted(monthly_map.items())][-12:]
    busiest = max(days, key=lambda x: x["count"])
    return {
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "total_contributions": sum(d["count"] for d in days),
        "active_days": sum(1 for d in days if d["count"] > 0),
        "current_streak": 6,
        "longest_streak": 19,
        "busiest_day": busiest,
        "monthly": monthly,
        "days": days,
    }


def base_style(extra: str = "") -> str:
    reduced = """
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation: none !important;
        transition: none !important;
        opacity: 1 !important;
        transform: none !important;
      }
      .smil-count { display: none !important; }
      .smil-static { display: inline !important; visibility: visible !important; }
    }
    """
    static_override = """
    .anim, .rise, .bar, .sq, .tile-wrap, .row-in, .pop-in {
      animation: none !important;
      opacity: 1 !important;
      transform: none !important;
    }
    """ if STATIC else ""
    return f"<style>{FONT_CSS}\n{extra}\n{reduced}\n{static_override}</style>"


def render_hero(data: dict) -> str:
    w, h = 880, 232
    css = f"""
    .eyebrow {{ font-family: {MONO}; font-size: 10.5px; letter-spacing: 0.1em; fill: {INK_MUTED}; }}
    .eyebrow-status {{ font-family: {MONO}; font-size: 10.5px; letter-spacing: 0.1em; fill: {GREEN}; }}
    .name {{ font-family: {SERIF}; font-size: 64px; font-weight: 400; letter-spacing: -0.015em; }}
    .role {{ font-family: {SANS}; font-size: 15.5px; font-weight: 500; fill: {INK}; }}
    .bio {{ font-family: {SANS}; font-size: 13.5px; fill: {INK_MUTED}; }}
    .pill-txt {{ font-family: {MONO}; font-size: 9.5px; letter-spacing: 0.06em; fill: {INK_MUTED}; }}
    .ledger-k {{ font-family: {MONO}; font-size: 9px; letter-spacing: 0.07em; fill: {INK_SUBTLE}; }}
    .ledger-v {{ font-family: {SERIF}; font-size: 20px; fill: {INK}; }}
    .ascii {{ font-family: {MONO}; font-size: 3.1px; fill: {INK}; white-space: pre; }}
    @keyframes riseIn {{
      from {{ opacity: 0; transform: translateY(12px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    @keyframes pulseDot {{
      0%, 100% {{ transform: scale(1); opacity: 0.9; }}
      50% {{ transform: scale(1.9); opacity: 0; }}
    }}
    @keyframes rowFade {{
      from {{ opacity: 0; }}
      to {{ opacity: 1; }}
    }}
    .rise {{ opacity: 0; animation: riseIn 0.55s cubic-bezier(0.22,1,0.36,1) forwards; }}
    .dot-ring {{ transform-box: fill-box; transform-origin: center; animation: pulseDot 2.4s ease-out infinite; }}
    .row-in {{ opacity: 0; animation: rowFade 0.25s ease-out forwards; }}
    """

    shine_smil = "" if STATIC else """
      <animateTransform attributeName="gradientTransform" type="translate"
        values="-1.6 0; 2.2 0; 2.2 0" keyTimes="0; 0.32; 1"
        dur="5.2s" begin="1.1s" repeatCount="indefinite" />
    """

    pills_svg = []
    px = 36
    for idx, label in enumerate(PROFILE["pills"]):
        pw = len(label) * 6.4 + 22
        delay = 0.42 + idx * 0.07
        pills_svg.append(f"""
        <g class="rise" style="animation-delay:{delay:.2f}s">
          <rect x="{px}" y="186" width="{pw:.1f}" height="24" rx="5" fill="{PAPER_ALT}" stroke="{BORDER}" />
          <text x="{px + pw / 2:.1f}" y="201.5" text-anchor="middle" class="pill-txt">{esc(label)}</text>
        </g>
        """)
        px += pw + 8

    portrait_path = "assets/portrait.txt"
    if os.path.exists(portrait_path):
        with open(portrait_path, "r", encoding="utf-8") as f:
            rows = [line.rstrip("\n") for line in f.readlines()[:96]]
        right_parts = [f'<rect x="646" y="18" width="214" height="196" rx="10" fill="{PAPER_ALT}" stroke="{BORDER}" />']
        for i, row in enumerate(rows):
            ry = 28 + i * 1.9
            r_delay = i * 0.018
            right_parts.append(
                f'<text x="656" y="{ry:.1f}" class="ascii row-in" style="animation-delay:{r_delay:.3f}s">{esc(row)}</text>'
            )
        right_panel = "\n".join(right_parts)
    else:
        ledger_items = [
            ("CONTRIBUTIONS", f"{data['total_contributions']:,}"),
            ("ACTIVE DAYS", f"{data['active_days']}"),
            ("LONGEST STREAK", f"{data['longest_streak']} days"),
            ("PEAK DAY", f"{data['busiest_day']['count']} commits"),
        ]
        right_parts = [
            f'<rect x="612" y="22" width="244" height="188" rx="10" fill="{PAPER_ALT}" stroke="{BORDER}" />',
            f'<text x="630" y="44" class="eyebrow">ACTIVITY LEDGER</text>',
            f'<line x1="630" y1="53" x2="838" y2="53" stroke="{BORDER}" />',
        ]
        for idx, (k, v) in enumerate(ledger_items):
            col = idx % 2
            row = idx // 2
            lx = 630 + col * 108
            ly = 82 + row * 64
            d = 0.30 + idx * 0.09
            right_parts.append(f"""
            <g class="row-in" style="animation-delay:{d:.2f}s">
              <text x="{lx}" y="{ly}" class="ledger-k">{esc(k)}</text>
              <text x="{lx}" y="{ly + 25}" class="ledger-v">{esc(v)}</text>
            </g>
            """)
        right_panel = "\n".join(right_parts)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Hassan Zafar — Senior Flutter Developer">
  <defs>
    <linearGradient id="nameShine" x1="0%" y1="0%" x2="100%" y2="0%" gradientUnits="objectBoundingBox">
      <stop offset="0%" stop-color="{INK}" />
      <stop offset="38%" stop-color="{INK}" />
      <stop offset="50%" stop-color="{BLUE}" />
      <stop offset="62%" stop-color="{INK}" />
      <stop offset="100%" stop-color="{INK}" />
      {shine_smil}
    </linearGradient>
  </defs>
  {base_style(css)}
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{PAPER}" stroke="{BORDER}" />

  <!-- Top eyebrow & pulsing status -->
  <g class="rise" style="animation-delay:0.05s">
    <text x="36" y="38" class="eyebrow">{esc(PROFILE['location'])}</text>
    <circle cx="256" cy="34.5" r="3.5" fill="{GREEN}" class="dot-ring" />
    <circle cx="256" cy="34.5" r="3.5" fill="{GREEN}" />
    <text x="267" y="38" class="eyebrow-status">{esc(PROFILE['status'])}</text>
  </g>

  <!-- Editorial serif name -->
  <text x="36" y="106" class="name rise" style="animation-delay:0.14s" fill="{INK}">{esc(PROFILE['first_name'])} <tspan fill="url(#nameShine)">{esc(PROFILE['last_name'])}</tspan></text>

  <!-- Bio lines -->
  <text x="36" y="140" class="role rise" style="animation-delay:0.26s">{esc(PROFILE['role'])}</text>
  <text x="36" y="164" class="bio rise" style="animation-delay:0.34s">{esc(PROFILE['bio'])}</text>

  <!-- Bottom tags -->
  {''.join(pills_svg)}

  <!-- Right editorial ledger or ASCII portrait -->
  {right_panel}
</svg>
"""


def render_graph(data: dict) -> str:
    w, h = 880, 178
    days = data["days"]
    css = f"""
    .eyebrow {{ font-family: {MONO}; font-size: 10px; letter-spacing: 0.1em; fill: {INK_MUTED}; }}
    .meta {{ font-family: {SANS}; font-size: 12px; fill: {INK_MUTED}; }}
    .lbl {{ font-family: {MONO}; font-size: 9px; fill: {INK_SUBTLE}; }}
    @keyframes sqPop {{
      from {{ opacity: 0; transform: scale(0.45); }}
      to {{ opacity: 1; transform: scale(1); }}
    }}
    .sq {{ opacity: 0; transform-box: fill-box; transform-origin: center;
           animation: sqPop 0.28s cubic-bezier(0.22,1,0.36,1) forwards; }}
    """

    weeks = []
    if days:
        first_dt = date.fromisoformat(days[0]["date"])
        pad = (first_dt.weekday() + 1) % 7
        current_week = [None] * pad
        for d in days:
            current_week.append(d)
            if len(current_week) == 7:
                weeks.append(current_week)
                current_week = []
        if current_week:
            weeks.append(current_week + [None] * (7 - len(current_week)))
    weeks = weeks[-53:]

    cell = 11.4
    gap = 3.4
    step = cell + gap
    ox, oy = 64, 54

    squares = []
    month_labels = []
    seen_month = None
    last_label_wi = -99

    for wi, week in enumerate(weeks):
        col_x = ox + wi * step
        delay = 0.55 + wi * 0.014
        first_valid = next((d for d in week if d is not None), None)
        if first_valid:
            ym = first_valid["date"][:7]
            if ym != seen_month and wi < len(weeks) - 1:
                seen_month = ym
                if wi - last_label_wi >= 3:
                    last_label_wi = wi
                    m_txt = datetime.strptime(ym, "%Y-%m").strftime("%b")
                    month_labels.append(f'<text x="{col_x:.1f}" y="44" class="lbl">{m_txt}</text>')

        for di, d in enumerate(week):
            if d is None:
                continue
            cy = oy + di * step
            fill = GRAPH_COLORS.get(d["level"], GRAPH_COLORS["NONE"])
            squares.append(
                f'<rect x="{col_x:.1f}" y="{cy:.1f}" width="{cell}" height="{cell}" rx="2.5" '
                f'fill="{fill}" class="sq" style="animation-delay:{delay:.3f}s" />'
            )

    day_labels = [
        f'<text x="26" y="{oy + 1 * step + 9:.1f}" class="lbl">Mon</text>',
        f'<text x="26" y="{oy + 3 * step + 9:.1f}" class="lbl">Wed</text>',
        f'<text x="26" y="{oy + 5 * step + 9:.1f}" class="lbl">Fri</text>',
    ]

    legend_levels = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
    legend = ['<text x="720" y="29" class="lbl">Less</text>']
    for idx, lv in enumerate(legend_levels):
        lx = 748 + idx * 14
        legend.append(f'<rect x="{lx}" y="20.5" width="10" height="10" rx="2" fill="{GRAPH_COLORS[lv]}" />')
    legend.append('<text x="845" y="29" text-anchor="end" class="lbl">More</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Contribution graph">
  {base_style(css)}
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{PAPER}" stroke="{BORDER}" />
  <text x="24" y="29" class="eyebrow">CONTRIBUTION GRAPH · {data['total_contributions']:,} CONTRIBUTIONS (PUBLIC + PRIVATE)</text>
  {''.join(legend)}
  {''.join(month_labels)}
  {''.join(day_labels)}
  {''.join(squares)}
</svg>
"""


def render_activity(data: dict) -> str:
    w, h = 880, 238
    monthly = data["monthly"]
    max_val = max((m["count"] for m in monthly), default=1) or 1
    peak_idx = max(range(len(monthly)), key=lambda i: monthly[i]["count"]) if monthly else 0

    css = f"""
    .eyebrow {{ font-family: {MONO}; font-size: 10px; letter-spacing: 0.1em; fill: {INK_MUTED}; }}
    .stat-v {{ font-family: {SERIF}; font-size: 30px; fill: {INK}; }}
    .stat-k {{ font-family: {MONO}; font-size: 9.5px; letter-spacing: 0.08em; fill: {INK_SUBTLE}; }}
    .m-lbl {{ font-family: {MONO}; font-size: 9.5px; fill: {INK_MUTED}; }}
    .peak-v {{ font-family: {MONO}; font-size: 10.5px; font-weight: 700; fill: {BLUE}; }}
    @keyframes growUp {{
      from {{ transform: scaleY(0); opacity: 0.2; }}
      to {{ transform: scaleY(1); opacity: 1; }}
    }}
    @keyframes popIn {{
      from {{ opacity: 0; transform: translateY(6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .bar {{ transform-box: fill-box; transform-origin: center bottom; transform: scaleY(0);
            animation: growUp 0.55s cubic-bezier(0.22,1,0.36,1) forwards; }}
    .pop-in {{ opacity: 0; animation: popIn 0.35s ease-out forwards; }}
    """

    busiest_date = data["busiest_day"]["date"]
    busiest_short = datetime.strptime(busiest_date, "%Y-%m-%d").strftime("%b %d") if busiest_date else "—"
    stats = [
        ("TOTAL (12M)", f"{data['total_contributions']:,}"),
        ("ACTIVE DAYS", f"{data['active_days']}"),
        ("CURRENT STREAK", f"{data['current_streak']}d"),
        ("LONGEST STREAK", f"{data['longest_streak']}d"),
        ("BUSIEST DAY", f"{data['busiest_day']['count']} ({busiest_short})"),
    ]
    stats_svg = []
    for idx, (k, v) in enumerate(stats):
        sx = 32 + idx * 165
        stats_svg.append(f'<text x="{sx}" y="58" class="stat-k">{esc(k)}</text>')
        stats_svg.append(f'<text x="{sx}" y="86" class="stat-v">{esc(v)}</text>')

    baseline = 202
    max_bar_h = 84
    bar_w = 48
    gap = 18.5
    start_x = 50.25

    bars_svg = [f'<line x1="32" y1="{baseline}" x2="848" y2="{baseline}" stroke="{BORDER}" />']
    for idx, m in enumerate(monthly):
        bh = max(4, (m["count"] / max_val) * max_bar_h) if m["count"] > 0 else 3
        bx = start_x + idx * (bar_w + gap)
        by = baseline - bh
        is_peak = idx == peak_idx and m["count"] > 0
        fill = BLUE if is_peak else "#D4CCBD"
        delay = 0.85 + idx * 0.045
        m_name = datetime.strptime(m["month"], "%Y-%m").strftime("%b").upper()

        bars_svg.append(
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_w}" height="{bh:.1f}" rx="5" '
            f'fill="{fill}" class="bar" style="animation-delay:{delay:.3f}s" />'
        )
        bars_svg.append(
            f'<text x="{bx + bar_w / 2:.1f}" y="220" text-anchor="middle" class="m-lbl">{m_name}</text>'
        )
        if is_peak:
            pop_delay = delay + 0.42
            bars_svg.append(
                f'<text x="{bx + bar_w / 2:.1f}" y="{by - 7:.1f}" text-anchor="middle" '
                f'class="peak-v pop-in" style="animation-delay:{pop_delay:.2f}s">{m["count"]}</text>'
            )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Monthly contributions">
  {base_style(css)}
  <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{PAPER}" stroke="{BORDER}" />
  <text x="32" y="30" class="eyebrow">MONTHLY BREAKDOWN &amp; STREAKS</text>
  {''.join(stats_svg)}
  {''.join(bars_svg)}
</svg>
"""


def render_smil_countup(x: float, y: float, target: int, suffix: str, start_delay: float) -> str:
    """18-frame SMIL <set> count-up animation with static + reduced-motion fallback."""
    final_label = f"{target}{suffix}"
    if STATIC:
        return f'<text x="{x}" y="{y}" class="big-num">{esc(final_label)}</text>'

    frames = 18
    step_dur = 0.045
    els = [f'<text x="{x}" y="{y}" class="big-num smil-static" style="display:none">{esc(final_label)}</text>']
    for i in range(frames):
        val = round((i / (frames - 1)) * target)
        begin = start_delay + i * step_dur
        if i < frames - 1:
            end = begin + step_dur
            set_tags = (
                f'<set attributeName="visibility" to="visible" begin="{begin:.3f}s" end="{end:.3f}s" />'
            )
            txt = f"{val}{suffix}" if i > 0 else "0"
        else:
            set_tags = f'<set attributeName="visibility" to="visible" begin="{begin:.3f}s" fill="freeze" />'
            txt = final_label
        els.append(
            f'<text x="{x}" y="{y}" class="big-num smil-count" visibility="hidden">{esc(txt)}{set_tags}</text>'
        )
    return "\n".join(els)


def render_tile(tile: dict) -> str:
    w, h = 286, 192
    accent = tile["accent"]
    delay = tile["delay"]
    css = f"""
    .eyebrow {{ font-family: {MONO}; font-size: 10px; letter-spacing: 0.12em; fill: #F6F3EC; opacity: 0.82; }}
    .big-num {{ font-family: {SERIF}; font-size: 62px; fill: #FFFFFF; }}
    .unit {{ font-family: {MONO}; font-size: 10px; letter-spacing: 0.1em; fill: #F6F3EC; opacity: 0.85; }}
    .sub {{ font-family: {SANS}; font-size: 12.5px; fill: #F6F3EC; opacity: 0.92; }}
    .cta {{ font-family: {MONO}; font-size: 9.5px; letter-spacing: 0.08em; fill: #FFFFFF; }}
    @keyframes tileSwing {{
      0% {{ opacity: 0; transform: translateY(22px) rotate(-2.5deg) scale(0.96); }}
      70% {{ opacity: 1; transform: translateY(-3px) rotate(0.5deg) scale(1.01); }}
      100% {{ opacity: 1; transform: translateY(0) rotate(0deg) scale(1); }}
    }}
    @keyframes ringPulse {{
      0% {{ transform: scale(0.8); opacity: 0.45; }}
      100% {{ transform: scale(2.1); opacity: 0; }}
    }}
    @keyframes nudgeArrow {{
      0%, 100% {{ transform: translate(0, 0); }}
      50% {{ transform: translate(3px, -2px); }}
    }}
    .tile-wrap {{
      opacity: 0; transform-box: fill-box; transform-origin: center;
      animation: tileSwing 0.65s cubic-bezier(0.22,1,0.36,1) {delay:.2f}s forwards;
    }}
    .corner-ring {{
      transform-box: fill-box; transform-origin: center;
      animation: ringPulse 3.2s ease-out {delay + 0.6:.2f}s infinite;
    }}
    .arrow {{
      display: inline-block;
      animation: nudgeArrow 2.2s ease-in-out {delay + 0.9:.2f}s infinite;
    }}
    """

    shine_smil = "" if STATIC else f"""
      <animateTransform attributeName="gradientTransform" type="translate"
        values="-1.4 0; 2.4 0; 2.4 0" keyTimes="0; 0.25; 1"
        dur="5.8s" begin="{delay + 1.4:.2f}s" repeatCount="indefinite" />
    """

    count_svg = render_smil_countup(24, 98, tile["count_target"], tile["count_suffix"], delay + 0.25)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(tile['eyebrow'])}">
  <defs>
    <clipPath id="tileClip"><rect x="0" y="0" width="{w}" height="{h}" rx="14" /></clipPath>
    <linearGradient id="tileShine" x1="0%" y1="0%" x2="100%" y2="35%">
      <stop offset="0%" stop-color="#FFFFFF" stop-opacity="0" />
      <stop offset="44%" stop-color="#FFFFFF" stop-opacity="0" />
      <stop offset="50%" stop-color="#FFFFFF" stop-opacity="0.22" />
      <stop offset="56%" stop-color="#FFFFFF" stop-opacity="0" />
      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0" />
      {shine_smil}
    </linearGradient>
  </defs>
  {base_style(css)}
  <g class="tile-wrap">
    <g clip-path="url(#tileClip)">
      <rect x="0" y="0" width="{w}" height="{h}" rx="14" fill="{accent}" />
      <circle cx="{w - 22}" cy="24" r="18" fill="none" stroke="#FFFFFF" stroke-width="1.2" class="corner-ring" />
      <circle cx="{w - 22}" cy="24" r="4" fill="#FFFFFF" opacity="0.85" />
      <rect x="0" y="0" width="{w}" height="{h}" fill="url(#tileShine)" />
    </g>
    <text x="24" y="34" class="eyebrow">{esc(tile['eyebrow'])}</text>
    {count_svg}
    <text x="24" y="123" class="unit">{esc(tile['unit'])}</text>
    <text x="24" y="147" class="sub">{esc(tile['subtitle'])}</text>
    <line x1="24" y1="160" x2="{w - 24}" y2="160" stroke="#FFFFFF" stroke-opacity="0.24" />
    <text x="24" y="178" class="cta">{esc(tile['cta'])}</text>
    <text x="{w - 24}" y="178" text-anchor="end" class="cta arrow">↗</text>
  </g>
</svg>
"""


def render_work_card(work: dict) -> str:
    w, h = 432, 190
    css = f"""
    .cat {{ font-family: {MONO}; font-size: 9.5px; letter-spacing: 0.1em; fill: {work['accent']}; }}
    .title {{ font-family: {SERIF}; font-size: 29px; fill: {INK}; }}
    .desc {{ font-family: {SANS}; font-size: 12.5px; fill: {INK_MUTED}; }}
    .tag {{ font-family: {MONO}; font-size: 9.5px; fill: {INK_MUTED}; }}
    @keyframes cardIn {{
      from {{ opacity: 0; transform: translateY(14px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .rise {{ opacity: 0; animation: cardIn 0.5s cubic-bezier(0.22,1,0.36,1) {work['delay']:.2f}s forwards; }}
    """

    lines = textwrap.wrap(work["desc"], width=55)[:3]
    desc_svg = "\n".join(
        f'<text x="24" y="{94 + i * 18}" class="desc">{esc(line)}</text>'
        for i, line in enumerate(lines)
    )

    tags_svg = []
    tx = 24
    for t in work["tags"]:
        tw = len(t) * 6.2 + 18
        tags_svg.append(
            f'<rect x="{tx}" y="152" width="{tw:.1f}" height="22" rx="5" fill="{PAPER_ALT}" stroke="{BORDER}" />'
            f'<text x="{tx + tw / 2:.1f}" y="166.5" text-anchor="middle" class="tag">{esc(t)}</text>'
        )
        tx += tw + 7

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{esc(work['title'])}">
  {base_style(css)}
  <g class="rise">
    <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{PAPER}" stroke="{BORDER}" />
    <rect x="24" y="0.5" width="44" height="3.5" rx="1.75" fill="{work['accent']}" />
    <text x="24" y="32" class="cat">{esc(work['category'])}</text>
    <text x="24" y="66" class="title">{esc(work['title'])}</text>
    {desc_svg}
    {''.join(tags_svg)}
  </g>
</svg>
"""


def render_stack_and_experience() -> str:
    w, h = 880, 174
    css = f"""
    .eyebrow {{ font-family: {MONO}; font-size: 10px; letter-spacing: 0.1em; fill: {INK_MUTED}; }}
    .tag {{ font-family: {MONO}; font-size: 10px; fill: {INK}; }}
    .period {{ font-family: {MONO}; font-size: 10.5px; fill: {INK_SUBTLE}; }}
    .role {{ font-family: {SANS}; font-size: 12.5px; font-weight: 600; fill: {INK}; }}
    .org {{ font-family: {SANS}; font-size: 12px; fill: {INK_MUTED}; }}
    @keyframes fadeUp {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}
    .rise {{ opacity: 0; animation: fadeUp 0.5s ease-out 2.75s forwards; }}
    """

    # Left: Tech Stack pills wrapped cleanly within x=28..408
    stack_svg = []
    sx, sy = 28, 52
    for tech in TECH_STACK:
        tw = len(tech) * 6.8 + 20
        if sx + tw > 408:
            sx = 28
            sy += 34
        stack_svg.append(
            f'<rect x="{sx}" y="{sy}" width="{tw:.1f}" height="25" rx="6" fill="{PAPER_ALT}" stroke="{BORDER}" />'
            f'<text x="{sx + tw / 2:.1f}" y="{sy + 16}" text-anchor="middle" class="tag">{esc(tech)}</text>'
        )
        sx += tw + 8

    # Right: Experience timeline with generous column spacing
    exp_svg = []
    for idx, (period, role, org) in enumerate(EXPERIENCE):
        ey = 66 + idx * 36
        dot_fill = BLUE if idx == 0 else BORDER
        exp_svg.append(f'<circle cx="452" cy="{ey - 4}" r="3.5" fill="{dot_fill}" />')
        exp_svg.append(f'<text x="466" y="{ey}" class="period">{esc(period)}</text>')
        exp_svg.append(f'<text x="568" y="{ey}" class="role">{esc(role)}</text>')
        exp_svg.append(f'<text x="854" y="{ey}" text-anchor="end" class="org">{esc(org)}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Tech Stack and Experience">
  {base_style(css)}
  <g class="rise">
    <rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="{PAPER}" stroke="{BORDER}" />
    <text x="28" y="32" class="eyebrow">CORE TECH STACK</text>
    {''.join(stack_svg)}
    <line x1="426" y1="22" x2="426" y2="152" stroke="{BORDER}" />
    <text x="448" y="32" class="eyebrow">EXPERIENCE</text>
    {''.join(exp_svg)}
  </g>
</svg>
"""


def main():
    os.makedirs("cards", exist_ok=True)
    data = load_contributions()

    outputs = {
        "hero.svg": render_hero(data),
        "graph.svg": render_graph(data),
        "activity.svg": render_activity(data),
        "stack.svg": render_stack_and_experience(),
    }
    for tile in TILES:
        outputs[tile["filename"]] = render_tile(tile)
    for work in FEATURED_WORK:
        outputs[work["filename"]] = render_work_card(work)

    for filename, svg in outputs.items():
        with open(os.path.join("cards", filename), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Rendered cards/{filename}")


if __name__ == "__main__":
    main()
