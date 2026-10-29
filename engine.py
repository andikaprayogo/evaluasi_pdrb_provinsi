"""Mesin evaluasi: menjalankan sel kode main.ipynb di dalam proses Python.

Logika evaluasi TIDAK ditulis ulang. Seluruh sel kode di main.ipynb dijalankan
apa adanya; hanya beberapa baris konfigurasi (lokasi file, nama sheet, periode)
yang diganti pada salinan di memori. File main.ipynb asli tidak diubah.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import re
import traceback
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

REQUIRED_SHEETS = ["205", "209", "210", "211", "212", "213", "218", "219"]
PERIOD_RE = re.compile(r"^\d{4}Q[1-4]$")


class EvaluationError(Exception):
    """Kesalahan saat menjalankan notebook (membawa info nomor sel)."""


@dataclass
class EvaluationResult:
    dataframe: pd.DataFrame
    output_path: Path
    log: str


def normalize_sheet_name(name: str) -> str:
    """'Sheet205', 'Sheet 205', '205' -> '205'."""
    normalized = "".join(str(name).lower().split())
    if normalized.startswith("sheet"):
        normalized = normalized[len("sheet"):]
    return normalized


def build_sheet_mapping(sheet_names: list[str]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for actual in sheet_names:
        mapping.setdefault(normalize_sheet_name(actual), actual)
    return mapping


def missing_sheets(sheet_names: list[str]) -> list[str]:
    mapping = build_sheet_mapping(sheet_names)
    return [s for s in REQUIRED_SHEETS if s not in mapping]


def detect_periods(xlsx_path: str | Path, sheet_name: str) -> list[str]:
    """Baca header tabel (skiprows=3, kolom A:F seperti di notebook)."""
    header = pd.read_excel(
        xlsx_path, sheet_name=sheet_name, usecols="A:F", skiprows=3, nrows=0
    )
    return [str(c) for c in header.columns if PERIOD_RE.match(str(c))]


def load_code_cells(notebook_path: str | Path) -> list[str]:
    with open(notebook_path, encoding="utf-8") as fh:
        nb = json.load(fh)
    cells = []
    for cell in nb["cells"]:
        if cell.get("cell_type") == "code":
            src = cell["source"]
            cells.append("".join(src) if isinstance(src, list) else src)
    return cells


_FILE_PATH_RE = re.compile(r"^(\s*)file_path\s*=.*$", re.MULTILINE)
_SHEET_RE = re.compile(
    r"^(\s*)(sheet_\w+)\s*=\s*([\"'])([^\"']+)\3\s*$", re.MULTILINE
)


def patch_cells(
    cells: list[str],
    xlsx_path: str,
    periode: str,
    sheet_mapping: dict[str, str],
) -> list[str]:
    patched: list[str] = []
    found_path = found_period = False

    for src in cells:
        if _FILE_PATH_RE.search(src):
            src = _FILE_PATH_RE.sub(
                lambda m: f"{m.group(1)}file_path = {xlsx_path!r}", src
            )
            found_path = True

        def _sheet(m: re.Match) -> str:
            indent, var, quote, value = m.groups()
            actual = sheet_mapping.get(normalize_sheet_name(value), value)
            return f"{indent}{var} = {actual!r}"

        src = _SHEET_RE.sub(_sheet, src)

        if "# Menentukan kuartal saat ini" in src:
            # Sel asli tetap dipertahankan (variabel `today` dipakai untuk
            # nama file output); periode ditimpa setelahnya.
            src = f"{src}\n\n# Periode dipilih melalui GUI\nperiode = {periode!r}\n"
            found_period = True

        patched.append(src)

    if not found_path:
        raise EvaluationError("Baris `file_path = ...` tidak ditemukan di main.ipynb.")
    if not found_period:
        raise EvaluationError(
            "Sel '# Menentukan kuartal saat ini' tidak ditemukan di main.ipynb."
        )
    return patched


def run_evaluation(
    notebook_path: str | Path,
    xlsx_path: str | Path,
    periode: str,
    sheet_names: list[str],
    base_dir: str | Path,
    progress=None,
) -> EvaluationResult:
    base_dir = Path(base_dir)
    (base_dir / "data" / "output").mkdir(parents=True, exist_ok=True)

    cells = patch_cells(
        load_code_cells(notebook_path),
        str(Path(xlsx_path).resolve()),
        periode,
        build_sheet_mapping(sheet_names),
    )

    ns: dict = {"__name__": "__main__"}
    buffer = io.StringIO()
    previous_cwd = os.getcwd()
    os.chdir(base_dir)  # notebook memakai path relatif "data/output/..."
    try:
        with contextlib.redirect_stdout(buffer):
            for i, src in enumerate(cells, start=1):
                if progress:
                    progress(i, len(cells))
                try:
                    exec(compile(src, f"<sel kode {i}>", "exec"), ns)
                except Exception as exc:
                    first_line = next(
                        (l for l in src.splitlines() if l.strip()), ""
                    )
                    raise EvaluationError(
                        f"Gagal pada sel kode ke-{i} (diawali: `{first_line[:70]}`)\n"
                        f"{type(exc).__name__}: {exc}\n\n{traceback.format_exc()}"
                    ) from exc
    finally:
        os.chdir(previous_cwd)

    df = ns.get("df_write_to_excel")
    file_name = ns.get("file_name")
    if df is None or not file_name:
        raise EvaluationError(
            "Notebook selesai, tetapi `df_write_to_excel` / `file_name` tidak ditemukan."
        )
    output_path = (base_dir / file_name).resolve()
    if not output_path.exists():
        raise EvaluationError(f"File output tidak ditemukan: {output_path}")

    return EvaluationResult(df, output_path, buffer.getvalue())
