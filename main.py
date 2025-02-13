import pandas as pd
from time import time
from datetime import datetime
import os
from openpyxl import load_workbook
import re
from time import time


def read(sheet):
    file_path = "data/Export Semua Tabel Resume_olah.xlsx"
    sheet_name = sheet

    return pd.read_excel(
        file_path,
        sheet_name=sheet_name,
        usecols="A:F",
        skiprows=3,
    )


def quarter():
    # Ambil tanggal hari ini
    today = datetime.today()

    # Ambil tahun dan bulan saat ini
    tahun = today.year
    bulan = today.month

    # Menentukan kuartal saat ini
    if 1 <= bulan <= 3:
        prev_tahun = tahun - 1  # Jika Q1, maka mundur ke Q4 tahun sebelumnya
        return f"{prev_tahun}Q4"
    elif 4 <= bulan <= 6:
        return f"{tahun}Q1"
    elif 7 <= bulan <= 9:
        return f"{tahun}Q2"
    else:
        return f"{tahun}Q3"


# def data_growth_implisit(
#     pkrt,
#     pkrt_a,
#     pkrt_b,
#     pkrt_c,
#     pkrt_d,
#     pkrt_e,
#     pkrt_f,
#     pkrt_g,
#     lnprt,
#     pkp,
#     pkp_a,
#     pkp_b,
#     pmtb,
#     pmtb_a,
#     pmtb_b,
#     inventori,
#     ekspor,
#     ekspor_a,
#     ekspor_b,
#     impor,
#     impor_a,
#     impor_b,
#     net_ekspor_daerah,
#     net_ekspor_daerah_a,
#     net_ekspor_daerah_b,
#     net_ekspor_luar_negeri,
# ):
#     return {
#         "pkrt": {
#             "data": pkrt,
#             "komponen": "Pengeluaran Konsumsi Rumah Tangga",
#         },
#         "pkrt_a": {
#             "data": pkrt_a,
#             "komponen": "PKRT - Makanan dan Minuman, Selain Restoran",
#         },
#         "pkrt_b": {
#             "data": pkrt_b,
#             "komponen": "PKRT - Pakaian, Alas Kaki dan Jasa Perawatannya",
#         },
#         "pkrt_c": {
#             "data": pkrt_c,
#             "komponen": "PKRT - Perumahan dan Perlengkapan Rumahtangga",
#         },
#         "pkrt_d": {
#             "data": pkrt_d,
#             "komponen": "PKRT - Kesehatan dan Pendidikan",
#         },
#         "pkrt_e": {
#             "data": pkrt_e,
#             "komponen": "PKRT - Transportasi dan Komunikasi",
#         },
#         "pkrt_f": {
#             "data": pkrt_f,
#             "komponen": "PKRT - Restoran dan Hotel",
#         },
#         "pkrt_g": {
#             "data": pkrt_g,
#             "komponen": "PKRT - Lainnya",
#         },
#         "lnprt": {
#             "data": lnprt,
#             "komponen": "Pengeluaran Konsumsi LNPRT",
#         },
#         "pkp": {
#             "data": pkp,
#             "komponen": "Pengeluaran Konsumsi Pemerintah",
#         },
#         "pkp_a": {
#             "data": pkp_a,
#             "komponen": "PKP - Konsumsi Kolektif",
#         },
#         "pkp_b": {
#             "data": pkp_b,
#             "komponen": "PKP - Konsumsi Individu",
#         },
#         "pmtb": {
#             "data": pmtb,
#             "komponen": "Pembentukan Modal Tetap Bruto",
#         },
#         "pmtb_a": {
#             "data": pmtb_a,
#             "komponen": "PMTB - Bangunan",
#         },
#         "pmtb_b": {
#             "data": pmtb_b,
#             "komponen": "PMTB - Non Bangunan",
#         },
#         "inventori": {
#             "data": inventori,
#             "komponen": "Perubahan Inventori",
#         },
#         "ekspor": {
#             "data": ekspor,
#             "komponen": "Ekspor luar negeri",
#         },
#         "ekspor_a": {
#             "data": ekspor_a,
#             "komponen": "Ekspor LN - Ekspor Barang",
#         },
#         "ekspor_b": {
#             "data": ekspor_b,
#             "komponen": "Ekspor LN - Ekspor Jasa",
#         },
#         "impor": {
#             "data": impor,
#             "komponen": "Impor Luar Negeri",
#         },
#         "impor_a": {
#             "data": impor_a,
#             "komponen": "Impor LN - Impor Barang",
#         },
#         "impor_b": {
#             "data": impor_b,
#             "komponen": "Impor LN - Impor Jasa",
#         },
#         "net_ekspor_daerah": {
#             "data": net_ekspor_daerah,
#             "komponen": "Net Ekspor Antar Daerah",
#         },
#         "net_ekspor_daerah_a": {
#             "data": net_ekspor_daerah_a,
#             "komponen": "Net Ekspor - Ekspor Antar Daerah",
#         },
#         "net_ekspor_daerah_b": {
#             "data": net_ekspor_daerah_b,
#             "komponen": "Net Ekspor - Impor Antar Daerah",
#         },
#         "net_ekspor_luar_negeri": {
#             "data": net_ekspor_luar_negeri,
#             "komponen": "Net Ekspor Luar Negeri",
#         },
#     }


start = time()

sheet_names = ["205", "209", "210", "212" "218", "219"]
for sheet in sheet_names:
    if sheet == "205":
        df = read(sheet)
        df_dist_inventori = df.iloc[848:898]
    elif sheet == "209":
        df = read(sheet)
        df_growth_qtoq_semua_komponen = df.iloc[0:50]
    elif sheet == "210":
        df = read(sheet)
        df_growth_yony_semua_komponen = df.iloc[0:50]
    # elif sheet == "212":
    #     df = read(sheet)
    #     df_growth_implisit_qtoq_pkrt = df.iloc[53:103]
    #     df_growth_implisit_qtoq_pkrt_a = df.iloc[106:156]
    #     df_growth_implisit_qtoq_pkrt_b = df.iloc[159:209]
    #     df_growth_implisit_qtoq_pkrt_c = df.iloc[212:262]
    #     df_growth_implisit_qtoq_pkrt_d = df.iloc[265:315]
    #     df_growth_implisit_qtoq_pkrt_e = df.iloc[318:368]
    #     df_growth_implisit_qtoq_pkrt_f = df.iloc[371:421]
    #     df_growth_implisit_qtoq_pkrt_g = df.iloc[424:474]
    #     df_growth_implisit_qtoq_lnprt = df.iloc[477:527]
    #     df_growth_implisit_qtoq_pkp = df.iloc[530:580]
    #     df_growth_implisit_qtoq_pkp_a = df.iloc[583:633]
    #     df_growth_implisit_qtoq_pkp_b = df.iloc[636:686]
    #     df_growth_implisit_qtoq_pmtb = df.iloc[689:739]
    #     df_growth_implisit_qtoq_pmtb_a = df.iloc[742:792]
    #     df_growth_implisit_qtoq_pmtb_b = df.iloc[795:845]
    #     df_growth_implisit_qtoq_inventori = df.iloc[848:898]
    #     df_growth_implisit_qtoq_ekspor = df.iloc[901:951]
    #     df_growth_implisit_qtoq_ekspor_a = df.iloc[954:1004]
    #     df_growth_implisit_qtoq_ekspor_b = df.iloc[1007:1057]
    #     df_growth_implisit_qtoq_impor = df.iloc[1060:1110]
    #     df_growth_implisit_qtoq_impor_a = df.iloc[1113:1163]
    #     df_growth_implisit_qtoq_impor_b = df.iloc[1166:1216]
    #     df_growth_implisit_qtoq_net_ekspor_daerah = df.iloc[1219:1269]
    #     df_growth_implisit_qtoq_net_ekspor_daerah_a = df.iloc[1272:1322]
    #     df_growth_implisit_qtoq_net_ekspor_daerah_b = df.iloc[1325:1375]
    #     df_growth_implisit_qtoq_net_ekspor_luar_negeri = df.iloc[1378:1428]
    elif sheet == "218":
        df = read(sheet)
        df_sog_qtoq_inventori = df.iloc[848:898]
        df_sog_qtoq_net_ekspor = df.iloc[1219:1269]
    elif sheet == "219":
        df_sog_yony_inventori = df.iloc[848:898]
        df_sog_yony_net_ekspor = df.iloc[1219:1269]

# Membuat DataFrame dengan header sesuai yang diminta
evaluasi = {
    "no": [],
    "kabkot": [],
    "komponen": [],
    "periode": [],
    "indikator": [],
    "nilai": [],
    "evaluasi": [],
    "keterangan": [],
    "respon": [],
}

# daftar pengecualian analisis
pulau = [
    "Sumatra",
    "Jawa ",
    "Bali & Nusa Tenggara",
    "Kalimantan",
    "Sulawesi",
    "Maluku & Papua",
]
lainnya = [
    "Kawasan Barat Indonesia",
    "Kawasan Timur Indonesia",
    "TOTAL 38 PROVINSI",
    "NASIONAL",
    "Diskrepansi (Total Prov thd Nas)",
    "Diskrepansi kumulatif tahunan",
]

# inisialisasi nomor urut evaluasi
num = 1

# daftar value pulau dan nasional
values = {
    "sumatra": 0,
    "jawa": 0,
    "bali_nt": 0,
    "kalimantan": 0,
    "sulawesi": 0,
    "maluku_papua": 0,
    "nasional": 0,
}

# daftar propinsi menurut pulau
provinsi = {
    "sumatra": [
        "1.Aceh",
        "2.Sumatra Utara",
        "3.Sumatra Barat",
        "4.Riau",
        "5.Jambi",
        "6.Sumatra Selatan",
        "7.Bengkulu",
        "8.Lampung",
        "9.Kepulauan Bangka Belitung",
        "10.Kepulauan Riau",
    ],
    "jawa": [
        "11.DKI Jakarta",
        "12.Jawa Barat",
        "13.Jawa Tengah",
        "14.DI Yogyakarta",
        "15.Jawa Timur",
        "16.Banten",
    ],
    "bali_nt": ["17.Bali", "18.Nusa Tenggara Barat", "19.Nusa Tenggara Timur"],
    "kalimantan": [
        "20.Kalimantan Barat",
        "21.Kalimantan Tengah",
        "22.Kalimantan Selatan",
        "23.Kalimantan Timur",
        "24.Kalimantan Utara",
    ],
    "sulawesi": [
        "25.Sulawesi Utara",
        "26.Sulawesi Tengah",
        "27.Sulawesi Selatan",
        "28.Sulawesi Tenggara",
        "29.Gorontalo",
        "30.Sulawesi Barat",
    ],
    "maluku_papua": [
        "31.Maluku",
        "32.Maluku Utara",
        "33.Papua Barat",
        "34.Papua Barat Daya",
        "35.Papua",
        "36.Papua Selatan",
        "37.Papua Tengah",
        "38.Papua Pegunungan",
    ],
}

# inisialisasi periode evaluasi
periode = quarter()

for index, row in df_dist_inventori.iterrows():
    if row["Komponen"] in set(pulau).union(lainnya):
        continue
    for col in df_dist_inventori.columns:
        if type(row[col]) != str and abs(row[col]) > 4 and col == periode:
            # print(row[df_inventori.columns[0]].strip(), col, row[col])
            data = {
                "no": num,
                "kabkot": re.sub(
                    r"^\d+\.", "", row[df_dist_inventori.columns[0]].strip()
                ),
                "komponen": "Inventori",
                "periode": col,
                "indikator": "Share",
                "nilai": row[col],
                "evaluasi": "Share inventori lebih besar dari 4%",
                "keterangan": "",
                "respon": "",
            }
            num += 1
            for key in evaluasi:
                evaluasi[key].append(data[key])

print(evaluasi)

# growth_implisit = data_growth_implisit(
#     df_growth_implisit_qtoq_pkrt,
#     df_growth_implisit_qtoq_pkrt_a,
#     df_growth_implisit_qtoq_pkrt_b,
#     df_growth_implisit_qtoq_pkrt_c,
#     df_growth_implisit_qtoq_pkrt_d,
#     df_growth_implisit_qtoq_pkrt_e,
#     df_growth_implisit_qtoq_pkrt_f,
#     df_growth_implisit_qtoq_pkrt_g,
#     df_growth_implisit_qtoq_lnprt,
#     df_growth_implisit_qtoq_pkp,
#     df_growth_implisit_qtoq_pkp_a,
#     df_growth_implisit_qtoq_pkp_b,
#     df_growth_implisit_qtoq_pmtb,
#     df_growth_implisit_qtoq_pmtb_a,
#     df_growth_implisit_qtoq_pmtb_b,
#     df_growth_implisit_qtoq_inventori,
#     df_growth_implisit_qtoq_ekspor,
#     df_growth_implisit_qtoq_ekspor_a,
#     df_growth_implisit_qtoq_ekspor_b,
#     df_growth_implisit_qtoq_impor,
#     df_growth_implisit_qtoq_impor_a,
#     df_growth_implisit_qtoq_impor_b,
#     df_growth_implisit_qtoq_net_ekspor_daerah,
#     df_growth_implisit_qtoq_net_ekspor_daerah_a,
#     df_growth_implisit_qtoq_net_ekspor_daerah_b,
#     df_growth_implisit_qtoq_net_ekspor_luar_negeri,
# )

# for growth in growth_implisit:
#     for komponen in pulau:
#         if komponen == "Sumatra":
#             values["sumatra"] = (
#                 growth_implisit[growth]["data"]
#                 .query(f"Komponen == '{komponen}'")[periode]
#                 .values[0]
#             )
#         elif komponen == "Jawa ":
#             values["jawa"] = (
#                 growth_implisit[growth]["data"]
#                 .query(f"Komponen == '{komponen}'")[periode]
#                 .values[0]
#             )
#         elif komponen == "Bali & Nusa Tenggara":
#             values["bali_nt"] = (
#                 growth_implisit[growth]["data"]
#                 .query(f"Komponen == '{komponen}'")[periode]
#                 .values[0]
#             )
#         elif komponen == "Kalimantan":
#             values["kalimantan"] = (
#                 growth_implisit[growth]["data"]
#                 .query(f"Komponen == '{komponen}'")[periode]
#                 .values[0]
#             )
#         elif komponen == "Sulawesi":
#             values["sulawesi"] = (
#                 growth_implisit[growth]["data"]
#                 .query(f"Komponen == '{komponen}'")[periode]
#                 .values[0]
#             )
#         elif komponen == "Maluku & Papua":
#             values["maluku_papua"] = (
#                 growth_implisit[growth]["data"]
#                 .query(f"Komponen == '{komponen}'")[periode]
#                 .values[0]
#             )
#     values["nasional"] = (
#         growth_implisit[growth]["data"]
#         .query(f"Komponen == 'NASIONAL'")[periode]
#         .values[0]
#     )

#     provinsi_keys = provinsi.keys()

#     for index, row in growth_implisit[growth]["data"].iterrows():
#         if row["Komponen"] in set(pulau).union(lainnya):
#             continue
#         for col in growth_implisit[growth]["data"].columns:
#             for provinsi_key in provinsi_keys:
#                 if row["Komponen"].strip() in provinsi[provinsi_key]:
#                     if type(row[col]) != str:
#                         if row[col] * values[provinsi_key] < 0 and col == periode:
#                             data = {
#                                 "no": num,
#                                 "kabkot": re.sub(
#                                     r"^\d+\.",
#                                     "",
#                                     row[
#                                         growth_implisit[growth]["data"].columns[0]
#                                     ].strip(),
#                                 ),
#                                 "komponen": growth_implisit[growth]["komponen"],
#                                 "periode": col,
#                                 "indikator": f"Growth implisit q-to-q {growth_implisit[growth]['komponen']}",
#                                 "nilai": row[col],
#                                 "evaluasi": "Growth implisit beda arah dengan growth pulau",
#                                 "keterangan": "",
#                                 "respon": "",
#                             }
#                             num += 1
#                             for key in evaluasi:
#                                 evaluasi[key].append(data[key])
#                         if row[col] * values["nasional"] < 0 and col == periode:
#                             data = {
#                                 "no": num,
#                                 "kabkot": re.sub(
#                                     r"^\d+\.",
#                                     "",
#                                     row[
#                                         growth_implisit[growth]["data"].columns[0]
#                                     ].strip(),
#                                 ),
#                                 "komponen": growth_implisit[growth]["komponen"],
#                                 "periode": col,
#                                 "indikator": f"Growth implisit q-to-q {growth_implisit[growth]['komponen']}",
#                                 "nilai": row[col],
#                                 "evaluasi": "Growth implisit beda arah dengan growth nasional",
#                                 "keterangan": "",
#                                 "respon": "",
#                             }
#                             num += 1
#                             for key in evaluasi:
#                                 evaluasi[key].append(data[key])
#                         if abs(row[col] - values[provinsi_key]) > 5 and col == periode:
#                             data = {
#                                 "no": num,
#                                 "kabkot": re.sub(
#                                     r"^\d+\.",
#                                     "",
#                                     row[
#                                         growth_implisit[growth]["data"].columns[0]
#                                     ].strip(),
#                                 ),
#                                 "komponen": growth_implisit[growth]["komponen"],
#                                 "periode": col,
#                                 "indikator": f"Growth implisit q-to-q {growth_implisit[growth]['komponen']}",
#                                 "nilai": row[col],
#                                 "evaluasi": "Growth implisit lebih besar 5 poin dari growth pulau",
#                                 "keterangan": "",
#                                 "respon": "",
#                             }
#                             num += 1
#                             for key in evaluasi:
#                                 evaluasi[key].append(data[key])
#                         if abs(row[col] - values["nasional"]) > 5 and col == periode:
#                             data = {
#                                 "no": num,
#                                 "kabkot": re.sub(
#                                     r"^\d+\.",
#                                     "",
#                                     row[
#                                         growth_implisit[growth]["data"].columns[0]
#                                     ].strip(),
#                                 ),
#                                 "komponen": growth_implisit[growth]["komponen"],
#                                 "periode": col,
#                                 "indikator": f"Growth implisit q-to-q {growth_implisit[growth]['komponen']}",
#                                 "nilai": row[col],
#                                 "evaluasi": "Growth implisit lebih besar 5 poin dari growth nasional",
#                                 "keterangan": "",
#                                 "respon": "",
#                             }
#                             num += 1
#                             for key in evaluasi:
#                                 evaluasi[key].append(data[key])

# print(evaluasi)

for (index1, row1), (index2, row2) in zip(
    df_sog_qtoq_inventori.iterrows(), df_growth_qtoq_semua_komponen.iterrows()
):
    if row1["Komponen"] in set(pulau).union(lainnya):
        continue
    for col in df_sog_qtoq_inventori.columns:
        if type(row1[col]) != str and row1[col] / row2[col] > 0.5 and col == periode:
            data = {
                "no": num,
                "kabkot": re.sub(
                    r"^\d+\.", "", row1[df_sog_qtoq_inventori.columns[0]].strip()
                ),
                "komponen": "Inventori",
                "periode": col,
                "indikator": "SoG q-to-q",
                "nilai": row1[col],
                "evaluasi": "SoG inventori lebih besar dari 50% pertumbuhan total",
                "keterangan": "",
                "respon": "",
            }
            num += 1
            for key in evaluasi:
                evaluasi[key].append(data[key])
        elif (
            type(row1[col]) != str
            and row1[col] > 0
            and row2[col] < 0
            and col == periode
        ):
            data = {
                "no": num,
                "kabkot": re.sub(
                    r"^\d+\.", "", row1[df_sog_qtoq_inventori.columns[0]].strip()
                ),
                "komponen": "Inventori",
                "periode": col,
                "indikator": "SoG q-to-q",
                "nilai": row1[col],
                "evaluasi": "SoG inventori positif sementara pertumbuhan total negatif",
                "keterangan": "",
                "respon": "",
            }
            num += 1
            for key in evaluasi:
                evaluasi[key].append(data[key])

print(evaluasi)

for (index1, row1), (index2, row2) in zip(
    df_sog_qtoq_net_ekspor.iterrows(), df_growth_qtoq_semua_komponen.iterrows()
):
    if row1["Komponen"] in set(pulau).union(lainnya):
        continue
    for col in df_sog_qtoq_net_ekspor.columns:
        if type(row1[col]) != str and row1[col] / row2[col] > 0.5 and col == periode:
            data = {
                "no": num,
                "kabkot": re.sub(
                    r"^\d+\.", "", row1[df_sog_qtoq_net_ekspor.columns[0]].strip()
                ),
                "komponen": "Net ekspor antar daerah",
                "periode": col,
                "indikator": "SoG q-to-q",
                "nilai": row1[col],
                "evaluasi": "SoG net ekspor antar daerah lebih besar dari 50% pertumbuhan total",
                "keterangan": "",
                "respon": "",
            }
            num += 1
            for key in evaluasi:
                evaluasi[key].append(data[key])
        elif (
            type(row1[col]) != str
            and row1[col] > 0
            and row2[col] < 0
            and col == periode
        ):
            data = {
                "no": num,
                "kabkot": re.sub(
                    r"^\d+\.", "", row1[df_sog_qtoq_net_ekspor.columns[0]].strip()
                ),
                "komponen": "Net ekspor antar daerah",
                "periode": col,
                "indikator": "SoG q-to-q",
                "nilai": row1[col],
                "evaluasi": "SoG net ekspor antar daerah positif sementara pertumbuhan total negatif",
                "keterangan": "",
                "respon": "",
            }
            num += 1
            for key in evaluasi:
                evaluasi[key].append(data[key])

print(evaluasi)

# Membuat DataFrame dengan header sesuai yang diminta
data = {
    "No": evaluasi["no"],
    "Kabkot": evaluasi["kabkot"],
    "Komponen": evaluasi["komponen"],
    "Periode": evaluasi["periode"],
    "Indikator ((qtq/yoy/ctc/SoG/implisit/share/dst...))": evaluasi["indikator"],
    "Nilai": evaluasi["nilai"],
    "Evaluasi": evaluasi["evaluasi"],
    "Keterangan": evaluasi["keterangan"],
    "Respon Daerah": evaluasi["respon"],
}

# Membuat DataFrame kosong dengan kolom yang sudah disesuaikan
df_write_to_excel = pd.DataFrame(data)

# Menyimpan DataFrame ke file Excel
file_name = "Evaluasi PDB.xlsx"

# Mengecek apakah file sudah ada atau belum
if os.path.exists(file_name):
    # Jika file sudah ada, menambah data ke file yang sudah ada
    with pd.ExcelWriter(
        file_name, mode="a", engine="openpyxl", if_sheet_exists="overlay"
    ) as writer:
        # Memuat workbook
        wb = load_workbook(file_name)
        df_write_to_excel.to_excel(writer, index=False, sheet_name=periode)
else:
    # Jika file belum ada, membuat file baru dan menulis data ke sheet
    with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
        df_write_to_excel.to_excel(writer, index=False, sheet_name=periode)

print(f"Elapsed time: {time()-start}")
