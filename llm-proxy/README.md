# LLM Proxy - Yerel Chat Backend

GitHub Pages sitesinden gelen istekleri Ollama'ya yönlendiren proxy. Rate limit (IP başına 5/gün), CORS, Origin/Referer kontrolü ve streaming desteği içerir.

## Hızlı Başlangıç

1. Ollama kur + `ollama pull qwen2.5:0.5b`
2. `pip install -r requirements.txt` (veya `pip install --user -r requirements.txt`)
3. `uvicorn main:app --host 0.0.0.0 --port 8765` ile proxy'yi başlat
4. Ayrı terminalde tünel: `cloudflared tunnel --url http://localhost:8765`
5. `_config.yml` içinde `llm_backend_url` değerini tünel URL ile güncelle
6. Siteyi deploy et veya `bundle exec jekyll serve` ile yerelde test et

## Kurulum

### 1. Ollama Kurulumu

1. [ollama.com](https://ollama.com) adresinden Ollama'yı indirip kurun.
2. Modeli indirin:

```bash
ollama pull qwen2.5:0.5b
```

### 2. Python Bağımlılıkları

```bash
cd llm-proxy
pip install -r requirements.txt
```

### 3. Proxy'yi Başlatma

```bash
uvicorn main:app --host 0.0.0.0 --port 8765
```

### 4. Tünel (Cloudflare veya ngrok)

**cloudflared (önerilen, kalıcı URL):**
- [cloudflared indir](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- `cloudflared tunnel --url http://localhost:8765` çalıştırın
- Verilen URL'i kopyalayın (örn. `https://xxx-xxx-xxx.trycloudflare.com`)

**ngrok:**
- [ngrok indir](https://ngrok.com/download)
- `ngrok http 8765` çalıştırın
- Her açılışta URL değişir; config'i güncellemeniz gerekir

**Config güncelleme:** `_config.yml` içindeki `llm_backend_url` değerini tünel URL'i ile değiştirin.

## Test

```bash
curl -X POST http://localhost:8765/chat \
  -H "Content-Type: application/json" \
  -H "Origin: https://oakati.github.io" \
  -d '{"message": "Merhaba"}'
```
