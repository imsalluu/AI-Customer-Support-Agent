# SupportIQ AI — Technical Architecture & Design Document

## 1. System Overview

SupportIQ AI is structured around a modular, multi-tenant B2B SaaS architecture:

```
                  +----------------------------------------------+
                  |               Client Channels                |
                  |  (WebChat Widget / WhatsApp Cloud API / Mail)|
                  +----------------------+-----------------------+
                                         |
                                         v
                  +----------------------------------------------+
                  |         Multi-Channel Gateway Layer          |
                  +----------------------+-----------------------+
                                         |
                                         v
+-------------------------------------------------------------------------------+
|                             FastAPI Backend Core                              |
|                                                                               |
|  +-----------------------+ +--------------------+ +------------------------+  |
|  | JWT & RBAC Middleware | | Tenant Isolation   | | Rate Limiting & Audit  |  |
|  +-----------------------+ +--------------------+ +------------------------+  |
|                                                                               |
|  +-------------------------------------------------------------------------+  |
|  |                   LangGraph Support Agent Workflow                      |  |
|  |                                                                         |  |
|  |   [User Message]                                                        |  |
|  |         |                                                               |  |
|  |         v                                                               |  |
|  |   (Intent & Sentiment Node)                                             |  |
|  |         |                                                               |  |
|  |         v                                                               |  |
|  |   {Safety Gate: Angry / Human Request?} ---> [Trigger Human Escalation] |  |
|  |         | (No)                                                          |  |
|  |         v                                                               |  |
|  |   (Tool & RAG Execution Node) <---> [11 Controlled Database Tools]      |  |
|  |         |                     <---> [pgvector Semantic Chunk Retriever] |  |
|  |         v                                                               |  |
|  |   (Grounded Response Generator)                                         |  |
|  |         |                                                               |  |
|  |         v                                                               |  |
|  |   {Confidence >= Threshold?}                                            |  |
|  |     /               \                                                   |  |
|  |  (Yes)              (No)                                                |  |
|  |   v                  v                                                  |  |
|  | [Deliver Answer   [Safe Human Handoff Fallback]                         |  |
|  |  + Citations]                                                           |  |
|  +-------------------------------------------------------------------------+  |
+-------------------------------------------------------------------------------+
                                         |
               +-------------------------+-------------------------+
               |                                                   |
               v                                                   v
+-----------------------------+                     +-----------------------------+
|    PostgreSQL + pgvector    |                     |      Redis Worker Cache     |
| (Tenants, CRM, Orders, KB)  |                     | (Sessions, Message Streams) |
+-----------------------------+                     +-----------------------------+
```

---

## 2. The 11 Controlled Business Tools

1. `search_customer(query)`: Finds customer profiles by name, email, or phone.
2. `get_customer(customer_id)`: Fetches 360-degree customer profile, LTV, and past orders.
3. `search_order(order_number, customer_id)`: Validates order existence without guessing.
4. `get_order_status(order_id_or_number)`: Returns live status, carrier, tracking ID, line items, and delivery estimate.
5. `search_products(query, category)`: Queries active product catalog for matching specs and prices.
6. `get_product(product_id_or_sku)`: Fetches product details and SKU information.
7. `check_inventory(product_id_or_sku)`: Validates real-time inventory count and in-stock status.
8. `create_support_ticket(customer_id, subject, description, priority, category)`: Creates an official ticket in the database.
9. `update_support_ticket(ticket_id, status, notes)`: Appends resolution notes or escalates ticket status.
10. `check_shipping(tracking_number_or_order)`: Fetches transit milestones, carrier, and destination ETA.
11. `request_human_agent(reason, urgency)`: Marks conversation as `WAITING_HUMAN` and halts automated AI generation.

---

## 3. Human-in-the-Loop (HITL) State Machine

Conversations progress through four strict states:

- **`AI_ACTIVE`**: The AI Support Agent processes customer messages autonomously via tools and RAG.
- **`WAITING_HUMAN`**: AI confidence was low or customer expressed high frustration/requested agent. AI halts generation.
- **`HUMAN_ACTIVE`**: Support agent took over the thread. The AI remains completely dormant while human messages stream.
- **`RESOLVED`**: Conversation is marked resolved, and an automated CSAT rating prompt is displayed.
