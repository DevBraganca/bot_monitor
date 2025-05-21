import requests
import time
from datetime import datetime
import threading

# === CONFIGURAÇÕES ===
SITEMAP_URL = "https://artigos.libanoeducacional.com.br/sitemap.xml"

# 🔔 Webhooks do Discord
WEBHOOK_ALERTA_URL = "https://discord.com/api/webhooks/1374797538288205955/zz6VqTr_7u5IZ6fDOcTlDgObFRcfZ0_JhzPabn2ibK4SGbjmfGssNu7kseNP3_XnQZJB"
WEBHOOK_RELATORIO_URL = "https://discord.com/api/webhooks/1374797887208292392/JPWbxaU3zQSIqfWBIjgVsHPo11re94yQ_fjEdEp1WlvSHeBTK42IV6oeUyml3GB5Mcqi"

INTERVALO_MINUTOS = 60
HORARIO_RELATORIO = "18:00"

quedas_hoje = 0
data_atual = datetime.now().date()

# === Envia mensagens ao Discord ===
def enviar_mensagem(webhook_url, conteudo):
    mensagem = {"content": conteudo}
    try:
        requests.post(webhook_url, json=mensagem)
        print(f"[DISCORD] Mensagem enviada: {conteudo}")
    except Exception as e:
        print(f"[ERRO] Falha ao enviar mensagem ao Discord: {e}")

# === Verifica status do sitemap ===
def verificar_sitemap():
    global quedas_hoje, data_atual

    if datetime.now().date() != data_atual:
        quedas_hoje = 0
        data_atual = datetime.now().date()

    try:
        response = requests.get(SITEMAP_URL, timeout=10)
        if response.status_code != 200:
            quedas_hoje += 1
            enviar_mensagem(WEBHOOK_ALERTA_URL, f"⚠️ Sitemap fora do ar!\nStatus: {response.status_code}\nURL: {SITEMAP_URL}")
        else:
            enviar_mensagem(WEBHOOK_ALERTA_URL, f"✅ Sitemap está online!\nStatus: {response.status_code}\nURL: {SITEMAP_URL}")
    except Exception as e:
        quedas_hoje += 1
        enviar_mensagem(WEBHOOK_ALERTA_URL, f"⚠️ Erro ao acessar o sitemap:\n{e}\nURL: {SITEMAP_URL}")

# === Envia relatório diário às 18h ===
def enviar_relatorio_diario():
    mensagem = f"📉 Relatório diário ({data_atual}):\nTotal de quedas detectadas: {quedas_hoje}"
    enviar_mensagem(WEBHOOK_RELATORIO_URL, mensagem)

# === Loop que agenda o relatório ===
def agendar_relatorio():
    while True:
        agora = datetime.now().strftime("%H:%M")
        if agora == HORARIO_RELATORIO:
            enviar_relatorio_diario()
            time.sleep(60)
        time.sleep(30)

# === Execução principal ===
if __name__ == "__main__":
    threading.Thread(target=agendar_relatorio, daemon=True).start()
    while True:
        verificar_sitemap()
        time.sleep(INTERVALO_MINUTOS * 60)
