# aiconfigurator-api

Thin FastAPI wrapper around `aiconfigurator` 

## What this does

This service:
- accepts a POST request with model + hardware + workload inputs
- runs `aiconfigurator` CLI under the hood
- parses key metrics
- returns clean JSON for frontend use

Typical outputs include:
- tokens/sec
- tokens/sec/GPU
- TTFT
- TPOT
- request latency
- GPU memory

---

## Repo contents

- `app.py` — FastAPI app
- `requirements.txt` — Python deps
- `build.sh` — native Render build script
- `Dockerfile` — Docker-based deploy path

---

## Local setup

### 1. Clone repo

```bash
git clone https://github.com/nb-qbits/aiconfigurator-api.git
cd aiconfigurator-api
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run locally
```bash
uvicorn app:app --reload
```

Service should come up on: http://127.0.0.1:8000

Health check
```bash
curl http://127.0.0.1:8000/health
```

```bash
curl -X POST http://127.0.0.1:8000/estimate \
  -H "Content-Type: application/json" \
  -d '{
    "model_path": "Qwen/Qwen2-7B",
    "system": "h100_sxm",
    "isl": 1024,
    "osl": 256,
    "batch_size": 16,
    "backend": "trtllm",
    "database_mode": "HYBRID",
    "tp_size": 1,
    "pp_size": 1
  }'

```
