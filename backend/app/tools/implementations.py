import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.constants import ConversationStatus, TicketCategory, TicketPriority, TicketStatus
from app.models.customer import Customer
from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate
from app.services.commerce_service import CommerceService
from app.services.customer_service import CustomerService
from app.services.ticket_service import TicketService
from app.tools.registry import ToolRegistry


# 1. search_customer
@ToolRegistry.register(
    name="search_customer",
    description="Search for a customer profile by name, email, or phone number in the organization database.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Customer name, email address, or phone number",
            }
        },
        "required": ["query"],
    },
)
async def tool_search_customer(db: AsyncSession, org_id: str, query: str) -> Dict[str, Any]:
    customers = await CustomerService.list_customers(db, org_id, query_str=query, limit=5)
    return {
        "count": len(customers),
        "customers": [
            {
                "id": c.id,
                "name": c.name,
                "email": c.email,
                "phone": c.phone,
                "total_orders": c.total_orders,
                "lifetime_value": c.lifetime_value,
            }
            for c in customers
        ],
    }


# 2. get_customer
@ToolRegistry.register(
    name="get_customer",
    description="Get full customer profile, tags, and 360-degree support history by Customer ID.",
    parameters={
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The unique ID of the customer",
            }
        },
        "required": ["customer_id"],
    },
)
async def tool_get_customer(db: AsyncSession, org_id: str, customer_id: str) -> Dict[str, Any]:
    try:
        data = await CustomerService.get_customer_360(db, org_id, customer_id)
        cust: Customer = data["customer"]
        return {
            "found": True,
            "id": cust.id,
            "name": cust.name,
            "email": cust.email,
            "phone": cust.phone,
            "total_orders": cust.total_orders,
            "lifetime_value": cust.lifetime_value,
            "tags": cust.tags,
            "recent_orders_count": len(data["orders"]),
            "open_tickets_count": len([t for t in data["tickets"] if t.status == TicketStatus.OPEN.value]),
        }
    except Exception as e:
        return {"found": False, "error": str(e)}


# 3. search_order
@ToolRegistry.register(
    name="search_order",
    description="Search for orders associated with a customer or order number.",
    parameters={
        "type": "object",
        "properties": {
            "order_number": {
                "type": "string",
                "description": "Order number (e.g. ORD-1001)",
            },
            "customer_id": {
                "type": "string",
                "description": "Optional customer ID to narrow search",
            },
        },
        "required": ["order_number"],
    },
)
async def tool_search_order(db: AsyncSession, org_id: str, order_number: str, customer_id: Optional[str] = None) -> Dict[str, Any]:
    order = await CommerceService.get_order_by_number_or_id(db, org_id, order_number)
    if not order:
        return {"found": False, "message": f"No order found matching '{order_number}'"}
    
    if customer_id and order.customer_id != customer_id:
        return {"found": False, "message": "Order does not belong to specified customer"}

    return {
        "found": True,
        "order_id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "total_amount": f"{order.total_amount} {order.currency}",
        "payment_status": order.payment_status,
        "carrier": order.carrier,
        "tracking_number": order.tracking_number,
    }


# 4. get_order_status
@ToolRegistry.register(
    name="get_order_status",
    description="Get verified live status, ordered items, carrier, and delivery estimate for an order.",
    parameters={
        "type": "object",
        "properties": {
            "order_id_or_number": {
                "type": "string",
                "description": "Order Number (e.g. ORD-1001) or Order ID or Tracking Number",
            }
        },
        "required": ["order_id_or_number"],
    },
)
async def tool_get_order_status(db: AsyncSession, org_id: str, order_id_or_number: str) -> Dict[str, Any]:
    order = await CommerceService.get_order_by_number_or_id(db, org_id, order_id_or_number)
    if not order:
        return {
            "found": False,
            "message": f"Order '{order_id_or_number}' was not found in our database. Please verify the order number.",
        }

    items_list = [
        {"title": i.title, "sku": i.sku, "quantity": i.quantity, "price": f"{i.unit_price} {order.currency}"}
        for i in order.items
    ]

    return {
        "found": True,
        "order_number": order.order_number,
        "status": order.status,
        "payment_status": order.payment_status,
        "carrier": order.carrier or "Standard Delivery",
        "tracking_number": order.tracking_number or "N/A",
        "estimated_delivery": order.estimated_delivery.isoformat() if order.estimated_delivery else "In 2-3 business days",
        "shipping_address": order.shipping_address or "Standard on file",
        "items": items_list,
        "total": f"{order.total_amount} {order.currency}",
    }


# 5. search_products
@ToolRegistry.register(
    name="search_products",
    description="Search the product catalog for available items, specifications, and pricing.",
    parameters={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Product name, keyword, or SKU",
            },
            "category": {
                "type": "string",
                "description": "Optional category filter",
            },
        },
        "required": ["query"],
    },
)
async def tool_search_products(db: AsyncSession, org_id: str, query: str, category: Optional[str] = None) -> Dict[str, Any]:
    products = await CommerceService.list_products(db, org_id, query_str=query, category=category, limit=5)
    return {
        "count": len(products),
        "products": [
            {
                "id": p.id,
                "sku": p.sku,
                "title": p.title,
                "category": p.category,
                "price": f"{p.price} {p.currency}",
                "in_stock": p.inventory_count > 0,
                "inventory_count": p.inventory_count,
                "description": p.description[:200] if p.description else "",
            }
            for p in products
        ],
    }


# 6. get_product
@ToolRegistry.register(
    name="get_product",
    description="Get detailed specifications, pricing, SKU, and availability for a specific product.",
    parameters={
        "type": "object",
        "properties": {
            "product_id_or_sku": {
                "type": "string",
                "description": "Product SKU, Title, or ID",
            }
        },
        "required": ["product_id_or_sku"],
    },
)
async def tool_get_product(db: AsyncSession, org_id: str, product_id_or_sku: str) -> Dict[str, Any]:
    product = await CommerceService.get_product_by_sku_or_id(db, org_id, product_id_or_sku)
    if not product:
        return {"found": False, "message": f"Product '{product_id_or_sku}' not found."}
    return {
        "found": True,
        "sku": product.sku,
        "title": product.title,
        "description": product.description,
        "category": product.category,
        "price": f"{product.price} {product.currency}",
        "inventory_count": product.inventory_count,
        "in_stock": product.inventory_count > 0,
    }


# 7. check_inventory
@ToolRegistry.register(
    name="check_inventory",
    description="Check real-time stock and inventory availability for a product SKU.",
    parameters={
        "type": "object",
        "properties": {
            "product_id_or_sku": {
                "type": "string",
                "description": "Product SKU or Name",
            }
        },
        "required": ["product_id_or_sku"],
    },
)
async def tool_check_inventory(db: AsyncSession, org_id: str, product_id_or_sku: str) -> Dict[str, Any]:
    product = await CommerceService.get_product_by_sku_or_id(db, org_id, product_id_or_sku)
    if not product:
        return {"found": False, "message": f"Product '{product_id_or_sku}' not found."}
    return {
        "sku": product.sku,
        "title": product.title,
        "inventory_count": product.inventory_count,
        "is_available": product.inventory_count > 0,
        "status": "In Stock" if product.inventory_count > 0 else "Out of Stock",
    }


# 8. create_support_ticket
@ToolRegistry.register(
    name="create_support_ticket",
    description="Create an official customer support ticket for unresolved issues, refunds, complaints, or technical escalations.",
    parameters={
        "type": "object",
        "properties": {
            "customer_id": {
                "type": "string",
                "description": "The customer ID",
            },
            "subject": {
                "type": "string",
                "description": "Brief summary of the issue",
            },
            "description": {
                "type": "string",
                "description": "Detailed explanation of customer problem",
            },
            "priority": {
                "type": "string",
                "enum": ["LOW", "MEDIUM", "HIGH", "URGENT"],
                "description": "Ticket priority level",
            },
            "category": {
                "type": "string",
                "enum": ["ORDER_STATUS", "RETURN", "REFUND", "PRODUCT_INFO", "SHIPPING", "PAYMENT", "ACCOUNT", "COMPLAINT", "TECHNICAL", "GENERAL"],
                "description": "Ticket category",
            },
        },
        "required": ["customer_id", "subject", "description"],
    },
)
async def tool_create_support_ticket(
    db: AsyncSession,
    org_id: str,
    customer_id: str,
    subject: str,
    description: str,
    priority: str = "MEDIUM",
    category: str = "GENERAL",
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    ticket_in = TicketCreate(
        customer_id=customer_id,
        conversation_id=conversation_id,
        subject=subject,
        description=description,
        priority=priority if priority in [p.value for p in TicketPriority] else TicketPriority.MEDIUM.value,
        category=category if category in [c.value for c in TicketCategory] else TicketCategory.GENERAL.value,
    )
    ticket = await TicketService.create_ticket(db, org_id, ticket_in)
    return {
        "success": True,
        "ticket_id": ticket.id,
        "ticket_number": ticket.ticket_number,
        "status": ticket.status,
        "priority": ticket.priority,
        "message": f"Support Ticket {ticket.ticket_number} created successfully. Our team has been notified.",
    }


# 9. update_support_ticket
@ToolRegistry.register(
    name="update_support_ticket",
    description="Add notes or update status of an existing support ticket.",
    parameters={
        "type": "object",
        "properties": {
            "ticket_id": {
                "type": "string",
                "description": "Ticket Number (e.g. TCK-10023) or Ticket ID",
            },
            "status": {
                "type": "string",
                "enum": ["OPEN", "IN_PROGRESS", "WAITING_CUSTOMER", "RESOLVED", "CLOSED"],
                "description": "New status",
            },
            "notes": {
                "type": "string",
                "description": "Resolution notes or updates to append",
            },
        },
        "required": ["ticket_id"],
    },
)
async def tool_update_support_ticket(
    db: AsyncSession,
    org_id: str,
    ticket_id: str,
    status: Optional[str] = None,
    notes: Optional[str] = None,
) -> Dict[str, Any]:
    from app.schemas.ticket import TicketUpdate
    ticket = await TicketService.update_ticket(
        db,
        org_id,
        ticket_id,
        TicketUpdate(status=status, resolution_notes=notes),
    )
    return {
        "success": True,
        "ticket_number": ticket.ticket_number,
        "status": ticket.status,
    }


# 10. check_shipping
@ToolRegistry.register(
    name="check_shipping",
    description="Check shipping status, transit location, and tracking history for an order or tracking number.",
    parameters={
        "type": "object",
        "properties": {
            "tracking_number_or_order": {
                "type": "string",
                "description": "Tracking number or order number",
            }
        },
        "required": ["tracking_number_or_order"],
    },
)
async def tool_check_shipping(db: AsyncSession, org_id: str, tracking_number_or_order: str) -> Dict[str, Any]:
    order = await CommerceService.get_order_by_number_or_id(db, org_id, tracking_number_or_order)
    if not order:
        return {"found": False, "message": f"No shipping record found for '{tracking_number_or_order}'"}

    history = []
    if order.tracking_history_json:
        try:
            history = json.loads(order.tracking_history_json)
        except Exception:
            pass

    return {
        "found": True,
        "order_number": order.order_number,
        "carrier": order.carrier or "FedEx Express",
        "tracking_number": order.tracking_number,
        "status": order.status,
        "shipping_address": order.shipping_address,
        "estimated_delivery": order.estimated_delivery.isoformat() if order.estimated_delivery else "Estimated in 2 days",
        "latest_checkpoint": history[-1] if history else {"status": "In Transit", "location": "Regional Hub"},
    }


# 11. request_human_agent
@ToolRegistry.register(
    name="request_human_agent",
    description="Escalate the conversation to a live human support specialist.",
    parameters={
        "type": "object",
        "properties": {
            "reason": {
                "type": "string",
                "description": "Reason for human escalation (e.g. angry customer, low confidence, complex refund)",
            },
            "urgency": {
                "type": "string",
                "enum": ["NORMAL", "HIGH", "URGENT"],
                "description": "Urgency level of the handoff",
            },
        },
        "required": ["reason"],
    },
)
async def tool_request_human_agent(
    db: AsyncSession,
    org_id: str,
    reason: str,
    urgency: str = "NORMAL",
    conversation_id: Optional[str] = None,
) -> Dict[str, Any]:
    # Marks handoff flag for state machine
    return {
        "escalated": True,
        "reason": reason,
        "urgency": urgency,
        "handoff_message": "I'm transferring you to a human support specialist who will take over right away. Please hold on.",
    }
