"""
Gera os 5 gráficos comparativos para o TCC, lendo os dados das tabelas .tex
existentes em chapters/tables/ e salvando PDFs em chapters/figures/.

Uso:
    source .venv/bin/activate
    python gerar_graficos.py
"""

import re
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# ─── Caminhos ─────────────────────────────────────────────────────────────────
ROOT = os.path.join(os.path.dirname(__file__), "..", "..", "..")
TABLES = os.path.join(ROOT, "chapters", "tables")
FIGURES = os.path.join(ROOT, "chapters", "figures")
os.makedirs(FIGURES, exist_ok=True)

# Estilo limpo e legível em preto-e-branco
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 10,
    "axes.titlesize": 11,
    "axes.labelsize": 10,
    "legend.fontsize": 9,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 150,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.1,
})

# ─── Helpers ──────────────────────────────────────────────────────────────────

def _clean(s):
    return s.strip().replace(r"\textbf{", "").replace("}", "")

def parse_metrics(tex_path):
    """
    Retorna dict com chaves:
      'accuracy', 'macro_f1', 'weighted_f1',
      'classes': {nome: {'precision', 'recall', 'f1'}}
    """
    result = {"accuracy": None, "macro_f1": None, "weighted_f1": None, "classes": {}}
    with open(tex_path, encoding="utf-8") as f:
        for line in f:
            if r"\\" not in line or "&" not in line:
                continue
            parts = [_clean(p) for p in line.split("&")]
            if len(parts) < 4:
                continue
            name = parts[0]
            if "Acur" in name:
                val = parts[2].replace(",", ".")
                if val not in ("-", ""):
                    result["accuracy"] = float(val)
            elif "Macro" in name:
                val = parts[3].replace(",", ".")
                if val not in ("-", ""):
                    result["macro_f1"] = float(val)
            elif "Ponderada" in name:
                val = parts[3].replace(",", ".")
                if val not in ("-", ""):
                    result["weighted_f1"] = float(val)
            elif name and not name.startswith("\\") and "Classe" not in name:
                # linha de classe
                try:
                    p = float(parts[1].replace(",", "."))
                    r = float(parts[2].replace(",", "."))
                    f = float(parts[3].replace(",", "."))
                    result["classes"][name] = {"precision": p, "recall": r, "f1": f}
                except ValueError:
                    pass
    return result

def parse_timing(tex_path):
    """Retorna [(cenário, dnn_s, rf_s), ...]"""
    rows = []
    with open(tex_path, encoding="utf-8") as f:
        for line in f:
            if r"\\" not in line or "&" not in line:
                continue
            parts = [_clean(p) for p in line.split("&")]
            if len(parts) < 3 or "Cen" in parts[0] or not parts[0]:
                continue
            try:
                dnn = float(parts[1].replace(",", "."))
                rf  = float(parts[2].replace(",", "."))
                rows.append((parts[0], dnn, rf))
            except ValueError:
                pass
    return rows

# ─── Dados ────────────────────────────────────────────────────────────────────
T = TABLES

experiments_completo = [
    ("DNN\nCICIDS",      os.path.join(T, "Baseline-CICIDS2017",       "DNN-Completo-Métricas.tex")),
    ("RF\nCICIDS",       os.path.join(T, "Baseline-CICIDS2017",       "RF-Completo-Métricas.tex")),
    ("DNN\nLycoS",       os.path.join(T, "MelhoriaA-LycoS",           "DNN-Completo-Métricas.tex")),
    ("RF\nLycoS",        os.path.join(T, "MelhoriaA-LycoS",           "RF-Completo-Métricas.tex")),
    ("DNN\nCICIDS+MDI",  os.path.join(T, "MelhoriaB-CICIDS2017-MDI",  "DNN-Completo-Métricas.tex")),
    ("DNN\nLycoS+MDI",   os.path.join(T, "MelhoriaC-LycoS-MDI",       "DNN-Completo-Métricas.tex")),
    ("AE\nCICIDS",       os.path.join(T, "MelhoriaD-G-Autoencoder",   "AE-CICIDS2017-Completo-Métricas.tex")),
    ("AE\nLycoS",        os.path.join(T, "MelhoriaD-G-Autoencoder",   "AE-LycoS-Completo-Métricas.tex")),
    ("AE+MDI\nCICIDS",   os.path.join(T, "MelhoriaD-G-Autoencoder",   "AE-CICIDS2017-MDI-Completo-Métricas.tex")),
    ("AE+MDI\nLycoS",    os.path.join(T, "MelhoriaD-G-Autoencoder",   "AE-LycoS-MDI-Completo-Métricas.tex")),
]

# ─── Gráfico 1 — Comparação Geral ─────────────────────────────────────────────
print("Gerando Gráfico 1 — Comparação Geral...")

labels, accs, macro_f1s, weighted_f1s = [], [], [], []
for label, path in experiments_completo:
    m = parse_metrics(path)
    labels.append(label)
    accs.append(m["accuracy"] or 0)
    macro_f1s.append(m["macro_f1"] or 0)
    weighted_f1s.append(m["weighted_f1"] or 0)

n = len(labels)
bar_h = 0.25
y = np.arange(n)
colors = ["#2c7bb6", "#d7191c", "#1a9641"]

fig, ax = plt.subplots(figsize=(10, 7))
b1 = ax.barh(y + bar_h,     accs,         bar_h, label="Acurácia",    color=colors[0], alpha=0.85)
b2 = ax.barh(y,             macro_f1s,    bar_h, label="Macro-F1",    color=colors[1], alpha=0.85)
b3 = ax.barh(y - bar_h,     weighted_f1s, bar_h, label="F1 Ponderado", color=colors[2], alpha=0.85)

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlim(0, 1.08)
ax.set_xlabel("Valor da Métrica")
ax.set_title("Comparação Geral de Métricas — Cenário Completo\n(todos os experimentos)")
ax.axvline(x=1.0, color="gray", linestyle="--", linewidth=0.7, alpha=0.5)
ax.legend(loc="lower right")

# Adicionar valores
for bar in b1: ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.2f}", va="center", ha="left", fontsize=7.5)
for bar in b2: ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.2f}", va="center", ha="left", fontsize=7.5)
for bar in b3: ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height()/2, f"{bar.get_width():.2f}", va="center", ha="left", fontsize=7.5)

# Linha separadora entre supervised e autoencoder
ax.axhline(y=5.5, color="black", linewidth=0.8, linestyle=":")
ax.text(0.01, 5.6, "▲ Supervisionado", fontsize=7.5, color="gray", transform=ax.get_yaxis_transform())
ax.text(0.01, 5.35, "▼ Autoencoder", fontsize=7.5, color="gray", transform=ax.get_yaxis_transform())

plt.tight_layout()
out1 = os.path.join(FIGURES, "grafico1_comparacao_geral.pdf")
plt.savefig(out1)
plt.close()
print(f"  → {out1}")

# ─── Gráfico 2 — Heatmap F1 por Classe (Baseline CICIDS2017) ──────────────────
print("Gerando Gráfico 2 — Heatmap F1 por Classe...")
import matplotlib.colors as mcolors

heatmap_files = [
    ("DNN\nCompleto",     os.path.join(T, "Baseline-CICIDS2017", "DNN-Completo-Métricas.tex")),
    ("DNN\nSem PortScan", os.path.join(T, "Baseline-CICIDS2017", "DNN-Sem-PortScan-Métricas.tex")),
    ("DNN\nSem XSS",      os.path.join(T, "Baseline-CICIDS2017", "DNN-Sem-XSS-Métricas.tex")),
    ("RF\nCompleto",      os.path.join(T, "Baseline-CICIDS2017", "RF-Completo-Métricas.tex")),
    ("RF\nSem PortScan",  os.path.join(T, "Baseline-CICIDS2017", "RF-Sem-PortScan-Métricas.tex")),
    ("RF\nSem XSS",       os.path.join(T, "Baseline-CICIDS2017", "RF-Sem-XSS-Métricas.tex")),
]

# Coletar todas as classes (union)
all_classes = []
parsed = []
for col_label, path in heatmap_files:
    m = parse_metrics(path)
    parsed.append((col_label, m["classes"]))
    for c in m["classes"]:
        if c not in all_classes:
            all_classes.append(c)

matrix = np.full((len(all_classes), len(heatmap_files)), np.nan)
for j, (col_label, classes) in enumerate(parsed):
    for i, cls in enumerate(all_classes):
        if cls in classes:
            matrix[i, j] = classes[cls]["f1"]

# Abreviações para as classes
abbrev = {
    "BENIGN": "BENIGN",
    "Bot": "Bot",
    "DDoS": "DDoS",
    "DoS GoldenEye": "DoS GoldEye",
    "DoS Hulk": "DoS Hulk",
    "DoS Slowhttptest": "DoS Slowhttp",
    "DoS slowloris": "DoS Slowloris",
    "FTP-Patator": "FTP-Patator",
    "Heartbleed": "Heartbleed",
    "Infiltration": "Infiltration",
    "PortScan": "PortScan",
    "SSH-Patator": "SSH-Patator",
    "Web Attack - Brute Force": "Web Brute Force",
    "Web Attack - Sql Injection": "Web SQL Inject.",
    "Web Attack - XSS": "Web XSS",
}
row_labels = [abbrev.get(c, c) for c in all_classes]
col_labels = [c for c, _ in heatmap_files]

fig, ax = plt.subplots(figsize=(12, 6))
cmap = plt.cm.RdYlGn
im = ax.imshow(matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")

ax.set_xticks(np.arange(len(col_labels)))
ax.set_xticklabels(col_labels, fontsize=9)
ax.set_yticks(np.arange(len(row_labels)))
ax.set_yticklabels(row_labels, fontsize=9)

# Linha vertical separando DNN e RF
ax.axvline(x=2.5, color="black", linewidth=1.5)

# Anotações de valor
for i in range(len(all_classes)):
    for j in range(len(heatmap_files)):
        v = matrix[i, j]
        if not np.isnan(v):
            txt_color = "black" if 0.3 < v < 0.85 else "white"
            ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                    fontsize=7.5, color=txt_color, fontweight="bold")

cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
cbar.set_label("F1-score")
ax.set_title("Heatmap de F1-score por Classe — Baseline CICIDS2017\n(DNN vs Random Forest × 3 cenários)")
plt.tight_layout()

out2 = os.path.join(FIGURES, "grafico2_heatmap_baseline.pdf")
plt.savefig(out2)
plt.close()
print(f"  → {out2}")

# ─── Gráfico 3 — Degradação por Cenário ───────────────────────────────────────
print("Gerando Gráfico 3 — Degradação por Cenário...")

degradation_data = {
    "DNN CICIDS": [
        parse_metrics(os.path.join(T, "Baseline-CICIDS2017", "DNN-Completo-Métricas.tex"))["macro_f1"],
        parse_metrics(os.path.join(T, "Baseline-CICIDS2017", "DNN-Sem-PortScan-Métricas.tex"))["macro_f1"],
        parse_metrics(os.path.join(T, "Baseline-CICIDS2017", "DNN-Sem-XSS-Métricas.tex"))["macro_f1"],
    ],
    "RF CICIDS": [
        parse_metrics(os.path.join(T, "Baseline-CICIDS2017", "RF-Completo-Métricas.tex"))["macro_f1"],
        parse_metrics(os.path.join(T, "Baseline-CICIDS2017", "RF-Sem-PortScan-Métricas.tex"))["macro_f1"],
        parse_metrics(os.path.join(T, "Baseline-CICIDS2017", "RF-Sem-XSS-Métricas.tex"))["macro_f1"],
    ],
    "DNN LycoS": [
        parse_metrics(os.path.join(T, "MelhoriaA-LycoS", "DNN-Completo-Métricas.tex"))["macro_f1"],
        parse_metrics(os.path.join(T, "MelhoriaA-LycoS", "DNN-Sem-PortScan-Métricas.tex"))["macro_f1"],
        parse_metrics(os.path.join(T, "MelhoriaA-LycoS", "DNN-Sem-XSS-Métricas.tex"))["macro_f1"],
    ],
    "RF LycoS": [
        parse_metrics(os.path.join(T, "MelhoriaA-LycoS", "RF-Completo-Métricas.tex"))["macro_f1"],
        parse_metrics(os.path.join(T, "MelhoriaA-LycoS", "RF-Sem-PortScan-Métricas.tex"))["macro_f1"],
        parse_metrics(os.path.join(T, "MelhoriaA-LycoS", "RF-Sem-XSS-Métricas.tex"))["macro_f1"],
    ],
}

scenarios = ["Completo", "Sem PortScan\nno treino", "Sem XSS\nno treino"]
x = np.arange(len(scenarios))
bar_w = 0.2
group_colors = ["#2c7bb6", "#abd9e9", "#d7191c", "#fdae61"]

fig, ax = plt.subplots(figsize=(10, 5.5))
for i, (name, vals) in enumerate(degradation_data.items()):
    offset = (i - 1.5) * bar_w
    bars = ax.bar(x + offset, vals, bar_w, label=name,
                  color=group_colors[i], alpha=0.85)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.008,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels(scenarios)
ax.set_ylim(0, 1.08)
ax.set_ylabel("Macro-F1")
ax.set_title("Degradação de Macro-F1 por Cenário (Open-Set Generalization)\nCICIDS2017 e LycoS-IDS2017")
ax.legend(ncol=2)
ax.axhline(y=1.0, color="gray", linestyle="--", linewidth=0.7, alpha=0.5)

# Anotação de queda de PortScan
for i, (name, vals) in enumerate(degradation_data.items()):
    drop = vals[0] - vals[1]
    if drop > 0.05:
        offset = (i - 1.5) * bar_w
        ax.annotate(f"−{drop:.2f}", xy=(x[1] + offset, vals[1] + 0.01),
                    xytext=(x[1] + offset, vals[1] + 0.08),
                    arrowprops=dict(arrowstyle="->", color="black", lw=0.8),
                    ha="center", fontsize=8, color="black")

plt.tight_layout()
out3 = os.path.join(FIGURES, "grafico3_degradacao_cenarios.pdf")
plt.savefig(out3)
plt.close()
print(f"  → {out3}")

# ─── Gráfico 4 — Tempo de Inferência ──────────────────────────────────────────
print("Gerando Gráfico 4 — Tempo de Inferência...")

timing_rows = parse_timing(os.path.join(T, "Baseline-CICIDS2017", "Total-Todos-Tempo-de-classificação.tex"))
if not timing_rows:
    # fallback para valores conhecidos
    timing_rows = [
        ("Completo",          17.3258, 3.3474),
        ("Sem PortScan",      19.5003, 3.4952),
        ("Sem XSS",           16.8805, 3.0954),
    ]

t_labels  = [r[0] for r in timing_rows]
t_dnn     = [r[1] for r in timing_rows]
t_rf      = [r[2] for r in timing_rows]

x = np.arange(len(t_labels))
bar_w = 0.35

fig, ax = plt.subplots(figsize=(8, 4.5))
b1 = ax.bar(x - bar_w/2, t_dnn, bar_w, label="DNN",           color="#2c7bb6", alpha=0.85)
b2 = ax.bar(x + bar_w/2, t_rf,  bar_w, label="Random Forest", color="#d7191c", alpha=0.85)

for bar in b1: ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15, f"{bar.get_height():.2f}s", ha="center", va="bottom", fontsize=8.5)
for bar in b2: ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15, f"{bar.get_height():.2f}s", ha="center", va="bottom", fontsize=8.5)

ax.set_xticks(x)
ax.set_xticklabels(t_labels)
ax.set_ylabel("Tempo de Classificação (s)")
ax.set_title("Tempo de Inferência — DNN vs Random Forest\n(CICIDS2017, conjunto de teste)")
ax.legend()

# Ratio anotation on top of tallest DNN bar
for i, (dnn, rf) in enumerate(zip(t_dnn, t_rf)):
    ratio = dnn / rf
    ax.text(i, max(dnn, rf) + 1.0, f"{ratio:.1f}×\nmaior", ha="center", fontsize=8, color="#2c7bb6", fontweight="bold")

plt.tight_layout()
out4 = os.path.join(FIGURES, "grafico4_tempo_inferencia.pdf")
plt.savefig(out4)
plt.close()
print(f"  → {out4}")

# ─── Gráfico 5 — Supervisionado vs Autoencoder ────────────────────────────────
print("Gerando Gráfico 5 — Supervisionado vs Autoencoder...")

sv_data = {
    "CICIDS2017": {
        "RF":       parse_metrics(os.path.join(T, "Baseline-CICIDS2017",       "RF-Completo-Métricas.tex"))["macro_f1"],
        "DNN":      parse_metrics(os.path.join(T, "Baseline-CICIDS2017",       "DNN-Completo-Métricas.tex"))["macro_f1"],
        "AE":       parse_metrics(os.path.join(T, "MelhoriaD-G-Autoencoder",   "AE-CICIDS2017-Completo-Métricas.tex"))["macro_f1"],
        "AE+MDI":   parse_metrics(os.path.join(T, "MelhoriaD-G-Autoencoder",   "AE-CICIDS2017-MDI-Completo-Métricas.tex"))["macro_f1"],
    },
    "LycoS-IDS2017": {
        "RF":       parse_metrics(os.path.join(T, "MelhoriaA-LycoS",           "RF-Completo-Métricas.tex"))["macro_f1"],
        "DNN":      parse_metrics(os.path.join(T, "MelhoriaA-LycoS",           "DNN-Completo-Métricas.tex"))["macro_f1"],
        "AE":       parse_metrics(os.path.join(T, "MelhoriaD-G-Autoencoder",   "AE-LycoS-Completo-Métricas.tex"))["macro_f1"],
        "AE+MDI":   parse_metrics(os.path.join(T, "MelhoriaD-G-Autoencoder",   "AE-LycoS-MDI-Completo-Métricas.tex"))["macro_f1"],
    },
}

model_names = ["RF", "DNN", "AE", "AE+MDI"]
datasets    = list(sv_data.keys())
bar_w = 0.18
x = np.arange(len(datasets))
sv_colors = ["#1a9641", "#2c7bb6", "#d7191c", "#fdae61"]

fig, ax = plt.subplots(figsize=(9, 5))
for i, model in enumerate(model_names):
    vals   = [sv_data[ds][model] for ds in datasets]
    offset = (i - 1.5) * bar_w
    bars   = ax.bar(x + offset, vals, bar_w, label=model,
                    color=sv_colors[i], alpha=0.85)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
                f"{bar.get_height():.2f}", ha="center", va="bottom", fontsize=8)

ax.set_xticks(x)
ax.set_xticklabels(datasets, fontsize=10)
ax.set_ylim(0, 1.12)
ax.set_ylabel("Macro-F1")
ax.set_title("Macro-F1 por Paradigma: Supervisionado vs Autoencoder\n(cenário completo)")
ax.legend(title="Modelo", ncol=4)
ax.axhline(y=1.0, color="gray", linestyle="--", linewidth=0.7, alpha=0.5)

# Anotação supervisonado vs AE
for i_ds, ds in enumerate(datasets):
    rf_val = sv_data[ds]["RF"]
    ae_val = sv_data[ds]["AE"]
    gap    = rf_val - ae_val
    ax.annotate("", xy=(i_ds + 2 * bar_w, ae_val + 0.02),
                xytext=(i_ds - 1.5 * bar_w, rf_val - 0.02),
                arrowprops=dict(arrowstyle="-", color="gray", lw=0.8, linestyle="dashed"))

plt.tight_layout()
out5 = os.path.join(FIGURES, "grafico5_supervisionado_vs_autoencoder.pdf")
plt.savefig(out5)
plt.close()
print(f"  → {out5}")

print("\nTodos os gráficos gerados com sucesso!")
print(f"  Diretório: {os.path.abspath(FIGURES)}")
