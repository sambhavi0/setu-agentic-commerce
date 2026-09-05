# Setu — Agent-Readable Commerce with a Spending Mandate

Setu lets an AI agent shop on a merchant's catalog and pay for things on a
person's behalf — but only within an explicit, enforced spending mandate,
with every decision logged.

## The problem

AI shopping agents are arriving fast — this is exactly the space emerging
protocols like ACP (OpenAI/Stripe), AP2 (Google), and x402 (Coinbase) are
racing to standardize, with no single standard having won yet. But most
demos of "an AI that can buy things" skip the harder question entirely:
**how do you let an AI spend money without giving it unrestricted authority
over that money?**

Setu is a minimal, working answer to that question — not a compliant
implementation of ACP/AP2/x402, but a real demonstration of the core idea:
an AI buyer that is explainable, bounded, and gated, with a full audit
trail, rather than a black box.

## What it does

1. A merchant catalog is exposed through a small, explicit tool contract —
   `list_products`, `get_product`, `initiate_purchase` — that any AI agent
   can call.
2. A buyer agent (LangGraph, running on Groq) takes a plain-English
   request, searches the catalog, and decides what to buy.
3. Every purchase attempt is checked against a **spending mandate**: a
   maximum transaction amount, a daily limit, an allowed-category list, a
   confirmation threshold, and an expiry date.
4. Depending on that check, the purchase is approved automatically,
   blocked outright (over the limit, wrong category, expired mandate), or
   held for explicit human confirmation.
5. Every decision — approved or not — is written to an audit trail.

## Tech stack

- **Backend:** FastAPI (Python)
- **Agent:** LangGraph, running on Groq (`openai/gpt-oss-20b`)
- **Frontend:** React (Vite)
- **Data:** JSON-based catalog and mandate (see "What's mocked" below)
- **Payments:** Schema-accurate mock adapter matching Razorpay's real
  Orders/Payment Links API response shape

## Project structure
backend/
app/
agent/ # LangGraph buyer agent
routes/ # FastAPI endpoints (catalog + agent)
schemas/ # Pydantic models (product, mandate)
services/ # catalog, policy engine, mandate, audit, Razorpay adapter
tools/ # agent-callable tool wrappers
data/ # products.json, mandate.json
frontend/
src/ # React chat UI + audit trail + mandate panel
docs/
architecture.md


## Setup

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create `backend/.env`:
GROQ_API_KEY=your_groq_key_here
USE_MOCK_RAZORPAY=true


Run:
```bash
uvicorn app.main:app --reload
```
API docs at `http://127.0.0.1:8000/docs`.

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```
App at `http://localhost:5173`.

## What's mocked, and why

Razorpay's account-creation flow currently requires a company PAN even for
test-mode API access, which wasn't available on this timeline as an
individual student applicant. The payment adapter
(`app/services/razorpay_adapter.py`) is built to Razorpay's actual
documented Orders/Payment Links API response schema, and swaps to real
test-mode keys via a single environment variable (`USE_MOCK_RAZORPAY`)
with no changes needed anywhere else in the codebase.

## What a production version would need

- Real Razorpay test/live keys, once account activation is possible
- Cryptographically signed mandates rather than a JSON file
- Agent identity attestation, so a merchant can verify which agent/buyer a
  request actually originates from
- A dispute/chargeback path for agent-initiated purchases
- Persistent, queryable audit storage instead of an in-memory list

See `docs/architecture.md` for the full system diagram and component
breakdown.
