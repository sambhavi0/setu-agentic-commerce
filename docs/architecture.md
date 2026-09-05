# Setu — Architecture

## Flow
User (natural language)
│
▼
Buyer Agent (LangGraph + Groq / openai-gpt-oss-20b)
│ tool calls
▼
Agent Commerce Interface
- list_products(filters)
- get_product(id)
- initiate_purchase(id, quantity)
│
▼
Policy Engine ──── checks against ──── Spending Mandate
- max transaction limit - max_transaction
- allowed categories - allowed_categories
- confirmation threshold - require_confirmation_above
- expiry - expires_at
│
approved? ──── no ──→ blocked_* / needs_confirmation
│ (returned, logged, stops here)
│ yes
▼
Razorpay-shaped Mock Adapter
- create_order()
- create_payment_link()
│
▼
Audit Ledger (every decision logged, approved or not)

## Components

- **Catalog** (`app/services/catalog_service.py`) — product data as JSON,
  stock decremented on approved purchase.
- **Agent Commerce Interface** (`app/tools/catalog_tools.py`,
  `app/routes/catalog.py`) — the tool contract an AI buyer calls. Inspired
  by concepts from ACP/AP2, not a compliant implementation of either.
- **Policy Engine** (`app/services/policy_service.py`) — the core
  differentiator. Every purchase attempt is checked against a mandate
  before any money-related action happens. The buyer agent has no
  authority to override this — its system prompt explicitly requires it
  to always call `initiate_purchase` and report back whatever the policy
  engine decides, rather than deciding confirmation on its own.
- **Mandate** (`app/schemas/mandate.py`, `app/data/mandate.json`) — the
  explicit, inspectable rules the buyer agent operates under: max
  transaction, daily limit, allowed categories, confirmation threshold,
  expiry.
- **Razorpay Adapter** (`app/services/razorpay_adapter.py`) — schema-
  accurate mock matching Razorpay's real Orders/Payment Links API
  response shape (order IDs, payment links, amount in paise). Toggled via
  `USE_MOCK_RAZORPAY`; swappable for real keys with no changes to any
  calling code.
- **Audit Ledger** (`app/services/audit_service.py`) — every decision,
  approved or blocked, logged with its reason and timestamp. Exposed via
  `GET /agent/audit`.
- **Buyer Agent** (`app/agent/buyer_agent.py`) — LangGraph
  `create_react_agent`, bound to the three tools above.

## API endpoints

- `GET /agent/tools/products` — list/filter catalog
- `GET /agent/tools/products/{id}` — get one product
- `POST /agent/tools/initiate_purchase` — attempt a purchase directly
- `POST /agent/chat` — talk to the buyer agent in natural language
- `GET /agent/audit` — full audit log
- `GET /agent/mandate` — current active mandate

## Demo scenarios

| Scenario | Trigger | Result |
|---|---|---|
| Approved | In-category, under confirmation threshold | Auto-approved, real order/payment link generated |
| Blocked — category | Item outside allowed categories | Hard block, regardless of price |
| Needs confirmation | In-category, between confirmation threshold and max | Paused, requires explicit human confirmation |
| Blocked — over limit | Total exceeds max_transaction | Hard block, regardless of confirmation |
| Blocked — expired | Mandate's expires_at has passed | Hard block, regardless of price or category |

## What's mocked, and why

Razorpay's account-creation flow requires a company PAN even for test-mode
access, which wasn't obtainable on this timeline as an individual student
applicant. The adapter above is schema-accurate against Razorpay's real
API and designed for a one-line swap to live keys.

## What a production version would need

- Real Razorpay keys
- Cryptographically signed mandates (currently a plain JSON file)
- Agent identity attestation
- Dispute/chargeback handling for agent-initiated purchases
- Persistent audit storage (currently in-memory, resets on server restart)
