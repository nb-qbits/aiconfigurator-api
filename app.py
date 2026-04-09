from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import re
import sys


app = FastAPI(title="AIConfigurator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EstimateRequest(BaseModel):
    model_path: str
    system: str
    isl: int
    osl: int
    batch_size: int

    backend: Optional[str] = None
    database_mode: Optional[str] = "HYBRID"

    tp_size: Optional[int] = None
    pp_size: Optional[int] = None

    attention_dp_size: Optional[int] = None
    moe_tp_size: Optional[int] = None
    moe_ep_size: Optional[int] = None

@app.get("/health")
def health():
    return {"status": "ok"}


def extract_float(pattern: str, text: str):
    m = re.search(pattern, text, re.MULTILINE)
    return float(m.group(1).replace(",", "")) if m else None


def extract_int(pattern: str, text: str):
    m = re.search(pattern, text, re.MULTILINE)
    return int(m.group(1).replace(",", "")) if m else None


@app.post("/estimate")
def estimate(req: EstimateRequest):
    cmd = [
        sys.executable,
        "-m",
        "aiconfigurator.main",
        "cli",
        "estimate",
        "--model-path", req.model_path,
        "--system", req.system,
        "--isl", str(req.isl),
        "--osl", str(req.osl),
        "--batch-size", str(req.batch_size),
    ]

    if req.database_mode:
        cmd.extend(["--database-mode", req.database_mode])

    if req.backend:
        cmd.extend(["--backend", req.backend])

    if req.tp_size is not None:
        cmd.extend(["--tp-size", str(req.tp_size)])

    if req.pp_size is not None:
        cmd.extend(["--pp-size", str(req.pp_size)])

    if req.attention_dp_size is not None:
        cmd.extend(["--attention-dp-size", str(req.attention_dp_size)])

    if req.moe_tp_size is not None:
        cmd.extend(["--moe-tp-size", str(req.moe_tp_size)])

    if req.moe_ep_size is not None:
        cmd.extend(["--moe-ep-size", str(req.moe_ep_size)])

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        return {
            "success": False,
            "command_used": " ".join(cmd),
            "error": result.stderr,
            "raw_output": result.stdout,
        }

    output = result.stdout

    return {
        "success": True,
        "model": req.model_path,
        "system": req.system,
        "backend": req.backend,
        "database_mode": req.database_mode,
        "isl": req.isl,
        "osl": req.osl,
        "batch_size": req.batch_size,
        "tp_size": req.tp_size,
        "pp_size": req.pp_size,
        "ttft_ms": extract_float(r"TTFT:\s+([\d.]+)\s+ms", output),
        "tpot_ms": extract_float(r"TPOT:\s+([\d.]+)\s+ms", output),
        "request_latency_ms": extract_float(r"Request Latency:\s+([\d.]+)\s+ms", output),
        "power_per_gpu_w": extract_float(r"Power \(per GPU\):\s+([\d.]+)\s+W", output),
        "tokens_per_sec": extract_float(r"tokens/s:\s+([\d,\.]+)", output),
        "tokens_per_sec_per_gpu": extract_float(r"tokens/s/gpu:\s+([\d,\.]+)", output),
        "tokens_per_sec_per_user": extract_float(r"tokens/s/user:\s+([\d,\.]+)", output),
        "seq_per_sec": extract_float(r"seq/s:\s+([\d.]+)", output),
        "concurrency": extract_int(r"Concurrency:\s+(\d+)", output),
        "gpu_memory_gb": extract_float(r"Memory \(GPU\):\s+([\d.]+)\s+GB", output),
        "command_used": " ".join(cmd)
    }


