# SupportIQ AI — API Reference & Webhook Contracts

Base URL: `http://localhost:8000/api/v1`

---

## 1. Authentication Endpoints

### Register SaaS Tenant & Owner
`POST /auth/register`
```json
{
  "email": "owner@company.com",
  "password": "strongpassword123",
  "full_name": "Jane Owner",
  "organization_name": "Acme Retailers"
}
```

### User Login
`POST /auth/login`
```json
{
  "email": "owner@company.com",
  "password": "strongpassword123"
}
```

---

## 2. Public Chat Widget Endpoints

### Initialize Session
`POST /widget/init`
Header: `X-API-Key: spiq_live_apex_demo_key_9921`
```json
{
  "customer_name": "John Visitor",
  "customer_email": "john@visitor.com"
}
```

### Send Message
`POST /widget/send`
Header: `X-API-Key: spiq_live_apex_demo_key_9921`
```json
{
  "conversation_id": "conv_id_here",
  "message": "Where is my order ORD-10022?"
}
```

---

## 3. Support Tickets Endpoints

### Create Ticket
`POST /tickets`
Header: `Authorization: Bearer <TOKEN>`
```json
{
  "customer_id": "cust_id_here",
  "subject": "Missing items in shipment",
  "description": "Customer received 1 of 2 headphones.",
  "priority": "HIGH",
  "category": "SHIPPING"
}
```

---

## 4. Multi-Channel Webhooks

### Meta WhatsApp Cloud API Webhook
- Verification: `GET /webhooks/whatsapp?hub.mode=subscribe&hub.verify_token=supportiq_verify_token_secure&hub.challenge=112233`
- Inbound: `POST /webhooks/whatsapp`
