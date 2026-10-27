"""Komponen tampilan dan format angka yang dipakai seluruh halaman."""

from __future__ import annotations

import html
from textwrap import dedent

import plotly.graph_objects as go
import streamlit as st

# Palet konsisten: navy untuk dasar, teal untuk aksi, amber untuk perhatian.
NAVY = "#0B1F33"
TEAL = "#0F766E"
TEAL_LIGHT = "#14B8A6"
AMBER = "#D97706"
RED = "#B91C1C"
BLUE = "#2563EB"
PURPLE = "#7C3AED"
MUTED = "#64748B"
GRID = "#E2E8F0"
COLORWAY = [TEAL, AMBER, BLUE, "#DC2626", PURPLE, "#0891B2", "#65A30D", "#DB2777"]
MONTHS_ID = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "Mei",
    6: "Jun",
    7: "Jul",
    8: "Agu",
    9: "Sep",
    10: "Okt",
    11: "Nov",
    12: "Des",
}


def inject_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

        :root {
            --navy: #0B1F33;
            --teal: #0F766E;
            --teal-soft: #E6F4F1;
            --amber: #D97706;
            --amber-soft: #FFF4E5;
            --ink: #172033;
            --muted: #64748B;
            --line: #E2E8F0;
            --surface: #FFFFFF;
            --bg: #F5F7FA;
        }

        html, body, [class*="css"] {
            font-family: "Plus Jakarta Sans", "Segoe UI", system-ui, -apple-system, sans-serif;
        }
        .stApp {
            background:
                radial-gradient(circle at 8% 0%, rgba(20,184,166,0.08), transparent 30rem),
                radial-gradient(circle at 100% 8%, rgba(217,119,6,0.06), transparent 26rem),
                var(--bg);
            color: var(--ink);
        }
        .block-container {
            max-width: 1180px;
            padding-top: 2.0rem;
            padding-bottom: 3.5rem;
        }
        h1, h2, h3, h4 {
            color: var(--navy);
            letter-spacing: -0.025em;
        }
        h1 { font-weight: 800; }
        h2 { font-weight: 750; }
        p, li { line-height: 1.7; }
        a { color: var(--teal); }

        code, pre, .stCode {
            font-family: "Cascadia Code", "Consolas", monospace;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #081926 0%, #0B2637 48%, #0C3540 100%);
            border-right: 1px solid rgba(255,255,255,0.06);
        }
        [data-testid="stSidebar"] * { color: #E8F0F7; }
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] strong { color: #FFFFFF; }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255,255,255,0.12);
            margin: 0.9rem 0;
        }
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
        [data-testid="stSidebar"] .stCaption { color: #AFC3D4 !important; }
        [data-testid="stSidebar"] div[role="radiogroup"] { gap: 0.18rem; }
        [data-testid="stSidebar"] div[role="radiogroup"] label {
            border-radius: 10px;
            padding: 0.42rem 0.58rem;
            transition: background 0.15s ease;
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
            background: rgba(255,255,255,0.08);
        }
        [data-testid="stSidebar"] div[role="radiogroup"] label:has(input:checked) {
            background: rgba(20,184,166,0.20);
            box-shadow: inset 3px 0 0 #2DD4BF;
        }
        [data-testid="stSidebar"] .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #2DD4BF, #FBBF24);
        }
        [data-testid="stSidebar"] .side-brand {
            display: flex;
            align-items: center;
            gap: 0.65rem;
            padding: 0.15rem 0 0.7rem 0;
        }
        [data-testid="stSidebar"] .side-brand-mark {
            width: 2.35rem;
            height: 2.35rem;
            border-radius: 12px;
            display: grid;
            place-items: center;
            background: linear-gradient(135deg, #14B8A6, #0F766E);
            color: #FFFFFF !important;
            font-weight: 800;
            font-size: 1.15rem;
            box-shadow: 0 8px 18px rgba(20,184,166,0.25);
        }
        [data-testid="stSidebar"] .side-brand-name {
            color: #FFFFFF !important;
            font-weight: 800;
            font-size: 1.08rem;
            letter-spacing: -0.01em;
            line-height: 1.15;
        }
        [data-testid="stSidebar"] .side-brand-sub {
            color: #99F6E4 !important;
            font-size: 0.7rem;
            font-weight: 600;
            letter-spacing: 0.02em;
        }

        /* Header dan tombol bawaan */
        header[data-testid="stHeader"] {
            background: transparent;
        }
        #MainMenu, footer { visibility: hidden; }
        .stAppDeployButton { display: none !important; }

        .stButton > button, .stFormSubmitButton > button,
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="stBaseButton-primary"] {
            border-radius: 10px;
            font-weight: 600;
            border: 1px solid #D6DEE8;
            transition: transform 0.12s ease, box-shadow 0.12s ease;
        }
        .stButton > button:hover, .stFormSubmitButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 5px 16px rgba(15,23,42,0.08);
        }
        button[data-testid="stBaseButton-primary"],
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #0F766E, #0D9488);
            border-color: #0F766E;
            color: white;
        }

        /* Input dan panel */
        div[data-baseweb="input"] > div,
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"] {
            border-radius: 10px !important;
        }
        [data-testid="stExpander"] {
            border: 1px solid var(--line);
            border-radius: 14px;
            background: rgba(255,255,255,0.86);
            overflow: hidden;
        }
        [data-testid="stDataFrame"] {
            border: 1px solid var(--line);
            border-radius: 12px;
            overflow: hidden;
        }
        [data-testid="stAlert"] {
            border-radius: 12px;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.35rem;
            border-bottom: 1px solid var(--line);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 9px 9px 0 0;
            padding: 0.55rem 0.9rem;
            font-weight: 600;
        }
        .stTabs [aria-selected="true"] {
            background: var(--teal-soft);
            color: var(--teal);
        }
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #0F766E, #2DD4BF);
        }

        /* Komponen khusus */
        .app-hero {
            position: relative;
            overflow: hidden;
            border-radius: 24px;
            padding: clamp(1.4rem, 4vw, 2.6rem);
            background:
                radial-gradient(circle at 88% 18%, rgba(45,212,191,0.30), transparent 19rem),
                radial-gradient(circle at 96% 100%, rgba(251,191,36,0.20), transparent 16rem),
                linear-gradient(135deg, #081926 0%, #0C3345 55%, #0F766E 100%);
            color: white;
            box-shadow: 0 22px 50px rgba(11,31,51,0.18);
            margin-bottom: 1.2rem;
        }
        .app-hero .eyebrow {
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-size: 0.72rem;
            font-weight: 700;
            color: #99F6E4;
            margin-bottom: 0.7rem;
        }
        .app-hero h1 {
            color: white;
            font-size: clamp(1.75rem, 4.4vw, 3.1rem);
            line-height: 1.08;
            margin: 0 0 0.75rem 0;
        }
        .app-hero p {
            color: #D7E7F0;
            font-size: clamp(0.95rem, 1.5vw, 1.08rem);
            max-width: 48rem;
            margin: 0;
        }
        .hero-pills {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 1.25rem;
        }
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            border-radius: 999px;
            padding: 0.3rem 0.68rem;
            font-size: 0.74rem;
            font-weight: 650;
            letter-spacing: 0.01em;
            border: 1px solid transparent;
            white-space: nowrap;
        }
        .hero-pills .pill {
            background: rgba(255,255,255,0.11);
            border-color: rgba(255,255,255,0.18);
            color: #F0FDFA;
        }
        .pill-teal { background: #E6F4F1; color: #0F766E; border-color: #BCE7E0; }
        .pill-amber { background: #FFF4E5; color: #B45309; border-color: #FDE3BD; }
        .pill-red { background: #FEF2F2; color: #B91C1C; border-color: #FECACA; }
        .pill-gray { background: #F1F5F9; color: #475569; border-color: #E2E8F0; }
        .pill-blue { background: #EFF6FF; color: #1D4ED8; border-color: #BFDBFE; }

        .page-intro {
            margin: 0.2rem 0 1.35rem 0;
        }
        .page-intro .eyebrow {
            color: var(--teal);
            text-transform: uppercase;
            letter-spacing: 0.13em;
            font-size: 0.7rem;
            font-weight: 800;
            margin-bottom: 0.2rem;
        }
        .page-intro h1 {
            font-size: clamp(1.55rem, 3.2vw, 2.25rem);
            margin: 0 0 0.35rem 0;
        }
        .page-intro p {
            color: var(--muted);
            max-width: 52rem;
            margin: 0;
            font-size: 0.98rem;
        }

        .soft-card {
            background: rgba(255,255,255,0.92);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.15rem 1.2rem;
            box-shadow: 0 6px 24px rgba(15,23,42,0.035);
            height: 100%;
        }
        .soft-card h3, .soft-card h4 { margin-top: 0; }
        .soft-card p { color: #475569; margin-bottom: 0.3rem; }

        .stat-card {
            background: rgba(255,255,255,0.94);
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 1rem 1.05rem;
            border-top: 3px solid #CBD5E1;
            box-shadow: 0 5px 20px rgba(15,23,42,0.035);
            min-height: 104px;
        }
        .stat-card.good { border-top-color: #0F766E; }
        .stat-card.warn { border-top-color: #D97706; }
        .stat-card.bad { border-top-color: #B91C1C; }
        .stat-card.blue { border-top-color: #2563EB; }
        .stat-label {
            color: #64748B;
            font-size: 0.74rem;
            font-weight: 650;
            letter-spacing: 0.02em;
            text-transform: uppercase;
        }
        .stat-value {
            color: #0B1F33;
            font-size: clamp(1.25rem, 2.4vw, 1.75rem);
            font-weight: 800;
            line-height: 1.25;
            margin-top: 0.18rem;
            word-break: break-word;
        }
        .stat-note { color: #64748B; font-size: 0.78rem; margin-top: 0.25rem; }

        .section-heading {
            margin: 1.4rem 0 0.7rem 0;
        }
        .section-heading h2 {
            font-size: 1.22rem;
            margin: 0;
        }
        .section-heading p {
            color: var(--muted);
            font-size: 0.88rem;
            margin: 0.15rem 0 0 0;
        }

        .module-card {
            border: 1px solid var(--line);
            border-radius: 16px;
            padding: 0.95rem 1rem;
            background: rgba(255,255,255,0.92);
            min-height: 130px;
        }
        .module-card.done { border-color: #A7E3DA; background: #F3FBF9; }
        .module-card.active { border-color: #5EEAD4; box-shadow: 0 0 0 3px rgba(20,184,166,0.10); }
        .module-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
            margin-bottom: 0.35rem;
        }
        .module-kicker { color: #64748B; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; }
        .module-title { color: #0B1F33; font-weight: 750; font-size: 0.97rem; line-height: 1.3; margin: 0.25rem 0; }
        .module-desc { color: #64748B; font-size: 0.79rem; line-height: 1.45; margin: 0; }
        .module-icon { font-size: 1.25rem; }

        .lesson-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin: 0.2rem 0 1rem 0;
        }
        .lesson-panel {
            background: rgba(255,255,255,0.94);
            border: 1px solid var(--line);
            border-radius: 18px;
            padding: 1.25rem 1.35rem;
            box-shadow: 0 6px 24px rgba(15,23,42,0.035);
        }
        .analogy-box {
            border-left: 4px solid #D97706;
            background: #FFFBEB;
            border-radius: 0 12px 12px 0;
            padding: 0.85rem 1rem;
            color: #78350F;
        }
        .note-box {
            border-left: 4px solid #0F766E;
            background: #F0FDFA;
            border-radius: 0 12px 12px 0;
            padding: 0.85rem 1rem;
            color: #134E4A;
        }
        .warn-box {
            border-left: 4px solid #B91C1C;
            background: #FEF2F2;
            border-radius: 0 12px 12px 0;
            padding: 0.85rem 1rem;
            color: #7F1D1D;
        }

        .footer-note {
            color: #64748B;
            font-size: 0.76rem;
            line-height: 1.55;
            border-top: 1px solid var(--line);
            margin-top: 2rem;
            padding-top: 0.9rem;
        }
        .empty-state {
            text-align: center;
            padding: 2.2rem 1rem;
            border: 1px dashed #CBD5E1;
            border-radius: 18px;
            background: rgba(255,255,255,0.6);
        }
        .empty-state .icon { font-size: 2rem; }
        .empty-state h3 { margin: 0.5rem 0 0.25rem 0; }
        .empty-state p { color: var(--muted); max-width: 36rem; margin: 0 auto; }

        @media (max-width: 760px) {
            .block-container { padding-left: 1rem; padding-right: 1rem; }
            .app-hero { border-radius: 18px; }
            .stat-card { min-height: auto; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def clean_md(text: str | None) -> str:
    return dedent(text or "").strip()


def hero(title: str, subtitle: str, eyebrow: str, pills: list[str] | None = None) -> None:
    pill_html = "".join(f'<span class="pill">{html.escape(p)}</span>' for p in (pills or []))
    st.markdown(
        f"""
        <section class="app-hero">
            <div class="eyebrow">{html.escape(eyebrow)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
            <div class="hero-pills">{pill_html}</div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str, eyebrow: str = "") -> None:
    st.markdown(
        f"""
        <div class="page-intro">
            <div class="eyebrow">{html.escape(eyebrow)}</div>
            <h1>{html.escape(title)}</h1>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(title: str, subtitle: str = "") -> None:
    st.markdown(
        f"""
        <div class="section-heading">
            <h2>{html.escape(title)}</h2>
            <p>{html.escape(subtitle)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(text: str, tone: str = "gray") -> str:
    allowed = {"teal", "amber", "red", "gray", "blue"}
    tone = tone if tone in allowed else "gray"
    return f'<span class="pill pill-{tone}">{html.escape(str(text))}</span>'


def stat_cards(items: list[dict], per_row: int = 4) -> None:
    """Tampilkan kartu metrik. Setiap item: label, value, note, tone."""
    if not items:
        return
    for start in range(0, len(items), per_row):
        row = items[start : start + per_row]
        columns = st.columns(len(row))
        for column, item in zip(columns, row):
            tone = item.get("tone", "")
            with column:
                st.markdown(
                    f"""
                    <div class="stat-card {html.escape(tone)}">
                        <div class="stat-label">{html.escape(str(item.get("label", "")))}</div>
                        <div class="stat-value">{html.escape(str(item.get("value", "")))}</div>
                        <div class="stat-note">{html.escape(str(item.get("note", "")))}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


def callout(title: str, body: str, tone: str = "note") -> None:
    css_class = {"note": "note-box", "warn": "warn-box", "analogy": "analogy-box"}.get(tone, "note-box")
    st.markdown(
        f'<div class="{css_class}"><strong>{html.escape(title)}</strong><br>{html.escape(body)}</div>',
        unsafe_allow_html=True,
    )


def empty_state(title: str, text: str, icon: str = "📭") -> None:
    st.markdown(
        f"""
        <div class="empty-state">
            <div class="icon">{html.escape(icon)}</div>
            <h3>{html.escape(title)}</h3>
            <p>{html.escape(text)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def rupiah(value: float | int | None, compact: bool = False) -> str:
    if value is None or value != value:
        return "—"
    if compact:
        absolute = abs(value)
        if absolute >= 1_000_000_000_000:
            return f"Rp{value / 1_000_000_000_000:,.2f} T"
        if absolute >= 1_000_000_000:
            return f"Rp{value / 1_000_000_000:,.2f} M"
        if absolute >= 1_000_000:
            return f"Rp{value / 1_000_000:,.1f} jt"
        if absolute >= 1_000:
            return f"Rp{value / 1_000:,.0f} rb"
    return f"Rp{value:,.0f}".replace(",", ".")


def number(value: float | int | None, decimals: int = 0) -> str:
    if value is None or value != value:
        return "—"
    return f"{value:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def pct(value: float | None, decimals: int = 1, signed: bool = False) -> str:
    if value is None or value != value:
        return "—"
    text = f"{value * 100:+.{decimals}f}%" if signed else f"{value * 100:.{decimals}f}%"
    return text.replace(".", ",")


def decimal_pct(value: float | None, decimals: int = 1, signed: bool = False) -> str:
    """Untuk nilai yang sudah dalam persen (0-100), bukan desimal 0-1."""
    if value is None or value != value:
        return "—"
    text = f"{value:+.{decimals}f}%" if signed else f"{value:.{decimals}f}%"
    return text.replace(".", ",")


def date_label(value) -> str:
    if value is None or value != value:
        return "—"
    if hasattr(value, "strftime"):
        try:
            return f"{value.day:02d} {MONTHS_ID[value.month]} {value.year}"
        except (AttributeError, KeyError):
            return str(value)
    return str(value)


def plotly_style(
    fig: go.Figure,
    title: str,
    x_title: str = "",
    y_title: str = "",
    height: int = 420,
    percent_y: bool = False,
    percent_x: bool = False,
    show_legend: bool = True,
) -> go.Figure:
    fig.update_layout(
        title=dict(text=title, font=dict(size=16, color=NAVY), x=0.01, xanchor="left"),
        template="plotly_white",
        height=height,
        colorway=COLORWAY,
        font=dict(family="Plus Jakarta Sans, Segoe UI, sans-serif", size=12, color="#334155"),
        margin=dict(l=12, r=12, t=58, b=18),
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="right",
            x=1,
            font=dict(size=11),
            visible=show_legend,
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0)",
    )
    fig.update_xaxes(
        title_text=x_title,
        showgrid=False,
        linecolor=GRID,
        ticks="outside",
        tickcolor=GRID,
        tickformat=".1%" if percent_x else None,
    )
    fig.update_yaxes(
        title_text=y_title,
        showgrid=True,
        gridcolor=GRID,
        zeroline=False,
        linecolor=GRID,
        tickformat=".1%" if percent_y else None,
    )
    return fig


def disclaimer() -> None:
    st.markdown(
        """
        <div class="footer-note">
            <strong>Penting:</strong> Proyek ini adalah alat belajar dan riset, bukan rekomendasi beli/jual
            dan bukan jaminan keuntungan. Data historis tidak menjamin hasil masa depan. Harga bisa turun
            dan modal bisa berkurang. Jangan memakai utang, jangan mempertaruhkan uang kebutuhan, dan
            verifikasi informasi penting pada laporan resmi perusahaan serta sumber resmi BEI/OJK.
        </div>
        """,
        unsafe_allow_html=True,
    )


def dataframe_with_format(frame, **kwargs):
    """Tampilkan dataframe Streamlit dengan pengaturan awal yang konsisten."""
    return st.dataframe(frame, width="stretch", hide_index=True, **kwargs)
