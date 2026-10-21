#!/usr/bin/env bash
# MCDM Studio — Modelos Multicritério de Decisão
# Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
# E-mail: profbruanbima@gmail.com
#
# Esteira completa: testes -> pipeline -> telas -> i18n -> Rust -> conferência.
#
# Uso:
#   ./run_all.sh                    # esteira completa
#   ./run_all.sh --rapido           # pula Rust e i18n
#   ./run_all.sh --caso smartphone  # um caso só
#   ./run_all.sh --background       # roda em screen (política R3 de foundations.md)
#
# POLÍTICA R3: background SEMPRE com `screen`, NUNCA com `nohup`. O screen permite
# reatar a sessão (`screen -r mcdm`), ver a saída ao vivo e interagir; nohup só
# despeja em arquivo e perde o terminal.

set -euo pipefail

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$AQUI"
SESSAO="mcdm"
LOGS="$AQUI/logs"
RAPIDO=0
CASO=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --rapido)     RAPIDO=1; shift ;;
    --caso)       CASO="${2:?--caso exige um id}"; shift 2 ;;
    --background)
      mkdir -p "$LOGS"
      shift
      screen -dmS "$SESSAO" bash -c "'$AQUI/run_all.sh' $* 2>&1 | tee '$LOGS/pipeline_$(date +%Y%m%d_%H%M%S).log'"
      echo "▶️  esteira iniciada na sessão screen '$SESSAO'"
      echo "   reatar:   screen -r $SESSAO"
      echo "   listar:   screen -ls"
      echo "   encerrar: screen -S $SESSAO -X quit"
      exit 0 ;;
    -h|--help)    sed -n '2,20p' "$0"; exit 0 ;;
    *)            echo "❌ opção desconhecida: $1" >&2; exit 1 ;;
  esac
done

mkdir -p "$LOGS"
INICIO=$(date +%s)
etapa() { echo; echo "════════════════════════════════════════════════════════════════════"; echo " $1"; echo "════════════════════════════════════════════════════════════════════"; }

etapa "0/8 · Ambiente"
python3 config.py

etapa "1/8 · Verificação matemática (Passada 1 da tripla-checagem)"
python3 testes_nucleo.py

etapa "2/8 · Pipeline de decisão — 10 métodos + consenso + robustez"
if [[ -n "$CASO" ]]; then python3 pipeline.py "$CASO"; else python3 pipeline.py; fi

etapa "3/8 · Matriz BCG — quadrante de oportunidade"
if [[ -n "$CASO" ]]; then python3 bcg.py "$CASO"; else python3 bcg.py --silencioso; fi

etapa "4/8 · Telas (6 por caso)"
if [[ -n "$CASO" ]]; then python3 gerar_graficos.py "$CASO"; else python3 gerar_graficos.py; fi

if [[ $RAPIDO -eq 0 ]]; then
  etapa "5/8 · Internacionalização — 12 idiomas + TMX"
  python3 gerar_i18n.py --tudo

  etapa "6/8 · Motor Rust — testes e compilação"
  RUST="$AQUI/../rust/mcdm_core"
  if command -v cargo >/dev/null 2>&1; then
    ( cd "$RUST" && cargo test --release --quiet && cargo build --release --quiet )
    echo "✅ crate compilado e testado"

    etapa "7/8 · Verificação cruzada Python × Rust"
    python3 exportar_rust.py

    etapa "8/8 · Verificação do dashboard (se estiver no ar)"
    if (ss -tln 2>/dev/null | grep -q ':3010'); then
      python3 verificar_dashboard.py || true
    else
      echo "⏭️  dashboard fora do ar — suba com:"
      echo "    cd ../evidence && screen -dmS mcdm_evidence bash -c 'npx evidence dev --port 3010 --host 0.0.0.0'"
    fi
  else
    echo "⚠️  cargo não encontrado — etapas 5 e 6 puladas."
  fi
else
  echo; echo "⏭️  modo --rapido: i18n, Rust e verificação cruzada pulados."
fi

DURACAO=$(( $(date +%s) - INICIO ))
echo
echo "════════════════════════════════════════════════════════════════════"
printf " ✅ ESTEIRA CONCLUÍDA em %dm%02ds\n" $((DURACAO/60)) $((DURACAO%60))
echo "════════════════════════════════════════════════════════════════════"
echo " Dashboard:  cd ../evidence && npx evidence sources && \\"
echo "             screen -dmS mcdm_evidence bash -c 'npx evidence dev --port 3010 --host 0.0.0.0'"
echo "             → http://localhost:3010   (reatar: screen -r mcdm_evidence)"
echo " Telas:      ../evidence/static/mc/<caso>/"
echo "             ../../../_private/foundations/telas/<caso>/"
echo
echo " ⚠️  Antes de publicar: complete as Passadas 2 e 3 de"
echo "     _private/foundations/triplecheck.md (as telas PRECISAM ser olhadas)."
echo "════════════════════════════════════════════════════════════════════"
