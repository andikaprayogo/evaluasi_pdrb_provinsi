from __future__ import annotations

import re
import tempfile
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

import engine

APP_DIR = Path(__file__).resolve().parent
NOTEBOOK_PATH = APP_DIR / "main.ipynb"

st.set_page_config(page_title="Evaluasi PDRB Provinsi", page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem; max-width: 1300px;}
    div[data-testid="stMetric"] {
        background: rgba(128,128,128,.08);
        border: 1px solid rgba(128,128,128,.25);
        padding: 14px 18px; border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- helpers
@st.cache_data(show_spinner=False)
def inspect_workbook(data: bytes) -> dict:
    """Baca daftar sheet dan kolom periode dari file yang diunggah."""
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp:
        tmp.write(data)
        path = tmp.name
    try:
        with pd.ExcelFile(path) as xls:
            sheets = list(xls.sheet_names)
        missing = engine.missing_sheets(sheets)
        periods: list[str] = []
        if not missing:
            mapping = engine.build_sheet_mapping(sheets)
            periods = engine.detect_periods(path, mapping["209"])
        return {"sheets": sheets, "missing": missing, "periods": periods}
    finally:
        Path(path).unlink(missing_ok=True)


def kategori_evaluasi(text: str) -> str:
    """Kelompokkan teks evaluasi agar ringkasan tidak terpecah per peringkat/pulau."""
    t = str(text)
    if re.match(r"^(Pertumbuhan )?[Tt]ertinggi", t):
        return "Peringkat pertumbuhan tertinggi sepulau"
    if re.match(r"^(Pertumbuhan )?[Tt]erendah", t):
        return "Peringkat pertumbuhan terendah sepulau"
    return t


def prepare_result(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["Kategori"] = out["Evaluasi"].map(kategori_evaluasi)
    return out


# ------------------------------------------------------------------ header
st.title("📊 Sistem Evaluasi PDRB Provinsi")
st.caption(
    "Antarmuka web untuk menjalankan evaluasi PDRB triwulanan dari `main.ipynb`. "
    "Aturan evaluasi tetap dijalankan oleh notebook."
)

if not NOTEBOOK_PATH.exists():
    st.error("File `main.ipynb` tidak ditemukan. Simpan `app.py` satu folder dengan `main.ipynb`.")
    st.stop()

with st.sidebar:
    st.header("Panduan singkat")
    st.markdown(
        "1. Unggah file Excel sumber\n"
        "2. Pilih periode yang dievaluasi\n"
        "3. Klik **Jalankan Evaluasi**\n"
        "4. Telaah hasil dan unduh Excel"
    )
    st.divider()
    st.markdown("**Sheet wajib**")
    st.code(", ".join(engine.REQUIRED_SHEETS), language=None)
    st.caption("Penamaan `Sheet205` / `Sheet 205` juga dikenali.")

# ------------------------------------------------------------------ input
left, right = st.columns([1.3, 1])

with left:
    st.subheader("1. Unggah data sumber")
    uploaded = st.file_uploader(
        "File Excel sumber PDRB",
        type=["xlsx"],
        help="Contoh: Export Semua Tabel Resume_olah.xlsx (struktur sesuai template).",
    )

info = None
if uploaded is not None:
    try:
        info = inspect_workbook(uploaded.getvalue())
    except Exception as exc:  # file rusak / bukan xlsx valid
        st.error(f"File Excel tidak dapat dibaca: {exc}")

with right:
    st.subheader("2. Periode evaluasi")
    periode = None
    if info is None:
        st.info("Unggah file terlebih dahulu; periode akan dibaca otomatis dari header tabel.")
    elif info["missing"]:
        st.error("Sheet berikut tidak ditemukan: **" + ", ".join(info["missing"]) + "**")
        st.caption("Sheet pada file: " + ", ".join(info["sheets"]))
    elif info["periods"]:
        periode = st.selectbox(
            "Periode (kolom pada tabel)",
            info["periods"],
            index=len(info["periods"]) - 1,
            help="Default: periode terbaru pada file.",
        )
        st.success(f"File valid · {len(info['sheets'])} sheet · {len(info['periods'])} periode terdeteksi")
    else:
        st.warning("Kolom periode (mis. 2026Q3) tidak terdeteksi otomatis. Isi manual:")
        c1, c2 = st.columns(2)
        yr = c1.number_input("Tahun", 2000, 2100, datetime.now().year, 1)
        qt = c2.selectbox("Kuartal", ["Q1", "Q2", "Q3", "Q4"], index=2)
        periode = f"{int(yr)}{qt}"

can_run = uploaded is not None and info is not None and not info["missing"] and periode is not None

run_clicked = st.button(
    "▶ Jalankan Evaluasi", type="primary", disabled=not can_run, use_container_width=True
)

# ----------------------------------------------------------------- proses
if run_clicked and can_run:
    work_dir = Path(tempfile.mkdtemp(prefix="pdrb_"))
    src_path = work_dir / "sumber.xlsx"
    src_path.write_bytes(uploaded.getvalue())

    with st.status("Menjalankan evaluasi…", expanded=True) as status:
        bar = st.progress(0.0)
        label = st.empty()

        def on_progress(i: int, n: int) -> None:
            bar.progress(i / n)
            label.write(f"Menjalankan sel {i} dari {n}")

        try:
            result = engine.run_evaluation(
                NOTEBOOK_PATH, src_path, periode, info["sheets"], APP_DIR, on_progress
            )
        except Exception as exc:
            status.update(label="Evaluasi gagal", state="error")
            st.session_state.pop("result", None)
            st.error("Evaluasi gagal dijalankan.")
            st.code(str(exc), language="text")
        else:
            status.update(label="Evaluasi selesai", state="complete", expanded=False)
            st.session_state["result"] = {
                "df": prepare_result(result.dataframe),
                "path": str(result.output_path),
                "bytes": result.output_path.read_bytes(),
                "periode": periode,
                "source": uploaded.name,
            }

# ------------------------------------------------------------------ hasil
res = st.session_state.get("result")
if res:
    df: pd.DataFrame = res["df"]
    st.divider()
    st.subheader("3. Hasil evaluasi")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Periode", res["periode"])
    m2.metric("Total temuan", f"{len(df):,}")
    m3.metric("Kab/kota terdampak", f"{df['Kabkot'].nunique():,}")
    m4.metric("Jenis evaluasi", f"{df['Kategori'].nunique():,}")

    if df.empty:
        st.success("Tidak ada temuan evaluasi pada periode ini.")
    else:
        tab_sum, tab_detail = st.tabs(["Ringkasan", "Detail temuan"])

        with tab_sum:
            a, b = st.columns(2)
            with a:
                st.markdown("**Temuan per jenis evaluasi**")
                st.bar_chart(df["Kategori"].value_counts(), horizontal=True)
            with b:
                st.markdown("**Temuan per komponen**")
                st.bar_chart(df["Komponen"].value_counts().head(15), horizontal=True)
            st.markdown("**15 provinsi dengan temuan terbanyak**")
            st.bar_chart(df["Kabkot"].value_counts().head(15))

        with tab_detail:
            f1, f2, f3 = st.columns(3)
            sel_kab = f1.multiselect("Provinsi", sorted(df["Kabkot"].unique()))
            sel_kom = f2.multiselect("Komponen", sorted(df["Komponen"].unique()))
            sel_kat = f3.multiselect("Jenis evaluasi", sorted(df["Kategori"].unique()))
            view = df
            if sel_kab:
                view = view[view["Kabkot"].isin(sel_kab)]
            if sel_kom:
                view = view[view["Komponen"].isin(sel_kom)]
            if sel_kat:
                view = view[view["Kategori"].isin(sel_kat)]
            st.caption(f"Menampilkan {len(view):,} dari {len(df):,} temuan")
            st.dataframe(view.drop(columns=["Kategori"]), use_container_width=True, hide_index=True, height=480)

    st.download_button(
        "⬇️ Unduh hasil evaluasi (.xlsx)",
        data=res["bytes"],
        file_name=Path(res["path"]).name,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary",
        use_container_width=True,
    )
    st.caption(f"Salinan juga tersimpan di `data/output/{Path(res['path']).name}`")
