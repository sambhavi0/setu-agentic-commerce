# Setu Agent Commerce Interface

## Overview

Setu exposes a machine-readable commerce interface that allows an AI buyer
to discover products, inspect authoritative product information, and request
purchases.

The AI buyer does not interact with the merchant's visual storefront directly.

Instead, it interacts with explicit commerce capabilities.

---

## Tool 1 — list_products

### Purpose

Discover products matching buyer requirements.

### Signature

list_products(filters)

### Filters

- category
- min_price
- max_price
- search
- in_stock_only

### Example

```json
{
  "category": "sneakers",
  "max_price": 3000,
  "in_stock_only": true
}

Expected behavior

The catalog service returns only products satisfying all supplied filters.

The agent should use this tool for product discovery.

Tool 2 — get_product
Purpose

Retrieve authoritative information about a specific product.

Signature

get_product(id)

Example
{
  "id": "shoes-002"
}
Expected behavior

Returns the complete current product representation.

The agent should retrieve the product before initiating a purchase.

Tool 3 — initiate_purchase
Purpose

Request a purchase of a specific product.

Signature

initiate_purchase(id, quantity)

Example
{
  "id": "shoes-001",
  "quantity": 1
}
Important

A purchase request is not equivalent to authorization.

The request will eventually pass through Setu's policy and mandate engine
before being forwarded to a payment provider.

Currently the payment implementation uses a mock adapter.

Design Principle

The buyer agent should never receive unrestricted access to a payment API.

The intended architecture is:

Buyer Agent
↓
Commerce Tool
↓
Policy / Mandate Engine
↓
Payment Adapter
↓
Payment Provider