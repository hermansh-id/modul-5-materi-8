# AcmeBot: intro to AI security

Chatbot toko online (RAG + SQL + email + file) yang sengaja rentan. Serang, pasang guard, bandingkan.

```bash
poetry install
export OPENAI_API_KEY=sk-...        # pakai project key dengan spend limit kecil
poetry run python attacks.py   # 7 serangan + 2 tes normal, tanpa guard vs dengan guard
poetry run python chat.py      # coba sendiri (tambah --guarded untuk versi aman)
```

| File | Isi |
|---|---|
| `app.py` | bot: agent loop, 3 tool, RAG sederhana, dataclass `Guards` (kosong = rentan) |
| `guards.py` | guard: input, dokumen, tool (least agency + approval), output |
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

Catatan: regex mudah dilewati (parafrase, bahasa lain), tabel `customers` masih bisa dibaca semua user (butuh otorisasi per user). Itu residual risk. Rate limit tidak diimplementasi, hanya `max_steps` dan `max_tokens`.

Hanya untuk data palsu di lab ini. Jangan dipakai ke sistem yang bukan milikmu.
