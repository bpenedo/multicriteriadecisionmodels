"""
Exporta um caso para o formato do motor Rust e confere os dois motores.

A verificação cruzada é o item mais forte da diretriz de tripla-checagem: dois
motores escritos em linguagens diferentes, com álgebra linear independente
(NumPy/LAPACK contra eliminação gaussiana e método das potências escritos à mão),
que concordam no ranking, são evidência de que a matemática está certa — não
apenas de que o código roda.

Uso:  python3 exportar_rust.py [caso ...]

MCDM Studio — Modelos Multicritério de Decisão
Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
E-mail: profbruanbima@gmail.com
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np

from casos import CATALOGO, obter
from config import ENCODING, FOUNDATIONS_DIR
from db import carregar_caso, get_conn
from nucleo import (ahp_topsis_2n, dematel, electre_i, maut, mcda_c,
                    promethee_ii, ranks)
from metodos_br import electre_ii, todim, vikor

RUST_DIR = FOUNDATIONS_DIR / "rust" / "mcdm_core"
BINARIO = RUST_DIR / "target" / "release" / "mcdm"
SAIDA = RUST_DIR / "problemas"


def exportar(conn, id_caso: str) -> Path:
    """Grava o caso no formato .mcdm lido pelo binário Rust."""
    caso = obter(id_caso)
    alternativas, criterios, rotulos, direcoes, X = carregar_caso(conn, id_caso)
    SAIDA.mkdir(parents=True, exist_ok=True)
    destino = SAIDA / f"{id_caso}.mcdm"

    linhas = [
        f"# {caso['nome']}",
        f"# domínio: {caso['dominio']} · decisor: {caso['decisor']}",
        "# Gerado por exportar_rust.py — não edite à mão.",
        "",
        "criterios: " + " ".join(f"{c}:{d}" for c, d in zip(criterios, direcoes)),
        "alternativas: " + " ".join(alternativas),
        "",
        "matriz:",
    ]
    # `.17g` e não `.6g` (que é o padrão de `{v:g}`).
    #
    # Dezessete dígitos significativos é o mínimo que garante ROUND-TRIP EXATO de
    # um f64: o Rust relê exatamente o mesmo número que o Python escreveu. Com o
    # `:g` padrão, a matriz chegava ao Rust truncada em 6 dígitos — 2508.167 virava
    # 2508.17 — e a verificação cruzada, que é a maior garantia de corretude deste
    # projeto, comparava o Python contra um Rust alimentado com dados DIFERENTES.
    #
    # Passou despercebido em 34 casos porque os valores eram redondos o bastante
    # para caber em 6 dígitos. O primeiro caso com dado real de 7 dígitos revelou
    # a perda. Ver bugs.md #BUG-034.
    linhas += [" ".join(f"{v:.17g}" for v in linha) for linha in X]
    linhas += ["", "dematel:"]
    linhas += [" ".join(f"{v:.17g}" for v in linha) for linha in caso["dematel"]]
    destino.write_text("\n".join(linhas) + "\n", encoding=ENCODING)
    return destino


def conferir(conn, id_caso: str) -> dict:
    """Roda os dois motores no mesmo caso e compara os rankings método a método."""
    arquivo = exportar(conn, id_caso)
    saida = subprocess.run([str(BINARIO), str(arquivo), "--json"],
                           capture_output=True, text=True, check=True)
    rust = json.loads(saida.stdout)

    caso = obter(id_caso)
    alternativas, criterios, _, direcoes, X = carregar_caso(conn, id_caso)
    *_, pesos, _T, _lim = dematel(caso["dematel"])

    py = {
        "AHP-TOPSIS 2n": ahp_topsis_2n(X, pesos, direcoes)[2],
        "ELECTRE I":     electre_i(X, pesos, direcoes)[0],
        "ELECTRE II":    electre_ii(X, pesos, direcoes)[0],
        "MAUT":          maut(X, pesos, direcoes),
        "MCDA-C":        mcda_c(X, pesos, direcoes),
        "PROMETHEE II":  promethee_ii(X, pesos, direcoes),
        "TODIM":         todim(X, pesos, direcoes)[0],
        "VIKOR":         vikor(X, pesos, direcoes)[0],
    }

    divergencias = []
    max_delta_peso = float(np.abs(np.array(rust["pesos"]) - pesos).max())
    if max_delta_peso > 1e-9:
        divergencias.append(f"pesos DEMATEL divergem em {max_delta_peso:.2e}")

    for metodo, score_py in py.items():
        rk_py = ranks(score_py)
        rk_rs = np.array(rust["metodos"][metodo]["rank"])
        sc_rs = np.array(rust["metodos"][metodo]["score"])
        delta = float(np.abs(np.asarray(score_py) - sc_rs).max())
        if not np.array_equal(rk_py, rk_rs):
            divergencias.append(f"{metodo}: rank py={list(rk_py)} rs={list(rk_rs)}")
        elif delta > 1e-9:
            divergencias.append(f"{metodo}: mesmo rank, score difere em {delta:.2e}")
    return {"caso": id_caso, "divergencias": divergencias,
            "vencedor_rust": rust["vencedor"], "n_metodos": len(py),
            "max_delta_peso": max_delta_peso}


def main():
    if not BINARIO.exists():
        print(f"❌ binário Rust não encontrado em {BINARIO}", file=sys.stderr)
        print(f"   compile com: cd {RUST_DIR} && cargo build --release", file=sys.stderr)
        return 1
    alvos = sys.argv[1:] or list(CATALOGO)
    conn = get_conn()
    print("VERIFICAÇÃO CRUZADA — motor Python (NumPy/numba) × motor Rust")
    print("=" * 78)
    falhas = 0
    try:
        for id_caso in alvos:
            r = conferir(conn, id_caso)
            if r["divergencias"]:
                falhas += 1
                print(f"❌ {id_caso}")
                for d in r["divergencias"]:
                    print(f"     {d}")
            else:
                print(f"✅ {id_caso:<20} {r['n_metodos']} métodos idênticos · "
                      f"vencedor={r['vencedor_rust']:<8} "
                      f"(Δpesos ≤ {r['max_delta_peso']:.1e})")
    finally:
        conn.close()
    print("=" * 78)
    if falhas:
        print(f"❌ {falhas}/{len(alvos)} caso(s) com divergência entre os motores.")
        return 1
    print(f"✅ {len(alvos)}/{len(alvos)} casos: os dois motores concordam em TODOS "
          f"os métodos e em todos os rankings.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
