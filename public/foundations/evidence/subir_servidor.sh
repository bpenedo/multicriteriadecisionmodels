#!/usr/bin/env bash
# Sobe o dashboard Evidence em segundo plano, via screen (nunca nohup).
#
# Uso:   bash subir_servidor.sh            # (re)inicia na porta 3010
#        bash subir_servidor.sh --parar
#
# Vive DENTRO do projeto de propósito: um script de subida guardado em diretório
# temporário some entre sessões, e o próximo "reiniciar" derruba o servidor sem
# conseguir subi-lo de volta.
#
# Encerra pelo NOME da sessão screen, não por `pkill -f "evidence dev"` — o padrão
# casaria com a própria linha de comando de quem chama e mataria o shell.
#
# MCDM Studio — Autor: ProfBru - Bruno Penedo © 2026 - TODOS OS DIREITOS RESERVADOS
set -uo pipefail
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SESSAO="mcdm_evidence"
PORTA="${MCDM_PORTA:-3010}"
LOG="${TMPDIR:-/tmp}/mcdm_evidence.log"

screen -S "$SESSAO" -X quit >/dev/null 2>&1 || true
[[ "${1:-}" == "--parar" ]] && { echo "servidor parado"; exit 0; }
sleep 2

screen -dmS "$SESSAO" bash -c "cd '$AQUI' && npm run sources > '$LOG' 2>&1 && npx evidence dev --port $PORTA --host 0.0.0.0 >> '$LOG' 2>&1"

for _ in $(seq 1 60); do
  if curl -s -o /dev/null --max-time 5 "http://localhost:$PORTA/"; then
    echo "✅ servidor no ar: http://localhost:$PORTA  (log: $LOG)"
    exit 0
  fi
  if ! screen -ls | grep -q "$SESSAO"; then
    echo "❌ a sessão screen morreu antes de responder — veja $LOG"; tail -20 "$LOG"; exit 1
  fi
  sleep 5
done
echo "❌ sem resposta em 300 s — veja $LOG"; tail -20 "$LOG"; exit 1
