# AcmeBot: intro to AI security

Chatbot toko online (RAG + SQL + email + file) yang sengaja rentan. Serang, pasang guard, bandingkan.

```bash
poetry install
cp .env.example .env                # isi OPENROUTER_API_KEY
poetry run python attacks.py   # 7 serangan + 2 tes normal, tanpa guard vs dengan guard
poetry run python chat.py      # coba sendiri (tambah --guarded untuk versi aman)
```

| File | Isi |
|---|---|
| `app.py` | bot: agent loop, 3 tool, RAG sederhana, dataclass `Guards` (kosong = rentan) |
| `guards.py` | guard: input, dokumen, tool (least agency + approval), output |
| `guardrails.py` | bikin guardrail OpenRouter (limit, model allowlist, filter prompt-injection + PII) lalu pasang ke API key baru. Butuh `OPENROUTER_MANAGEMENT_KEY` |
| `attacks.py` | daftar serangan + hasil before/after |
| `docs/`, `samples/`, `public_files/`, `secrets/` | data palsu; `invoice_poisoned.txt` berisi indirect injection |

| Serangan | OWASP LLM | Guard yang menahan |
|---|---|---|
| A1 curi system prompt | LLM01/08 | input_check + secret dihapus dari prompt |
| A2 baca gaji, A3 hapus order | LLM03 | `sql_tables`: read-only + allowlist tabel |
| A4 baca file credentials | LLM03 | `tool_check`: hanya folder `public_files/` |
| A5 invoice beracun | LLM01 / ASI01 | `doc_check` + email eksternal diblok, internal perlu approval |
| A6 dokumen internal bocor | LLM09 | `doc_filter`: customer hanya dokumen public |
| A7 PII pelanggan | LLM02 | `output_filter` (regex) |

Model default `deepseek/deepseek-v3.2` (ganti lewat env `MODEL`). `poetry run python guardrails.py` = layer tambahan di sisi provider: key hasil script punya budget dan filter yang jalan sebelum request sampai ke model.

Catatan: regex mudah dilewati (parafrase, bahasa lain), tabel `customers` masih bisa dibaca semua user (butuh otorisasi per user). Itu residual risk. Rate limit tidak diimplementasi, hanya `max_steps` dan `max_tokens`.

Hanya untuk data palsu di lab ini. Jangan dipakai ke sistem yang bukan milikmu.
