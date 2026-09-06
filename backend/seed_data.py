import asyncio
import json
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.core.database import AsyncSessionLocal, Base, async_engine
from app.core.security import get_password_hash
from app.models import (
    AgentConfig,
    AuditLog,
    Channel,
    Conversation,
    Customer,
    Feedback,
    KnowledgeChunk,
    KnowledgeDocument,
    Message,
    Order,
    OrderItem,
    Organization,
    Product,
    Subscription,
    Ticket,
    User,
)
from app.rag.embeddings import get_embedding


async def seed_database():
    print("Initializing database schema...")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # Check if already seeded
        res = await db.execute(select(Organization).where(Organization.slug == "apex-commerce"))
        existing_org = res.scalar_one_or_none()
        if existing_org:
            print("Database already seeded with demo organization. Skipping seed.")
            return

        print("Seeding demo organization: Apex Commerce Inc. ...")
        org = Organization(
            name="Apex Commerce Inc.",
            slug="apex-commerce",
            api_key="spiq_live_apex_demo_key_9921",
            plan="BUSINESS",
            is_active=True,
        )
        db.add(org)
        await db.flush()

        # Users
        owner = User(
            organization_id=org.id,
            email="alex@supportiq.ai",
            hashed_password=get_password_hash("password123"),
            full_name="Alex Mercer (Lead Admin)",
            role="OWNER",
            avatar_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
            is_active=True,
        )
        agent1 = User(
            organization_id=org.id,
            email="sarah.support@supportiq.ai",
            hashed_password=get_password_hash("password123"),
            full_name="Sarah Jenkins (Senior Agent)",
            role="SUPPORT_AGENT",
            avatar_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150&auto=format&fit=crop&q=80",
            is_active=True,
        )
        agent2 = User(
            organization_id=org.id,
            email="marcus.agent@supportiq.ai",
            hashed_password=get_password_hash("password123"),
            full_name="Marcus Vance (Technical Support)",
            role="SUPPORT_AGENT",
            avatar_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80",
            is_active=True,
        )
        db.add_all([owner, agent1, agent2])

        # Agent Configuration
        agent_cfg = AgentConfig(
            organization_id=org.id,
            name="Apex Assistant",
            tone="PROFESSIONAL",
            language="en",
            personality_prompt="You are Apex Assistant, an empathetic, highly knowledgeable customer support specialist for Apex Commerce.",
            greeting_message="Hello! Welcome to Apex Commerce Support. How can I assist you with orders, returns, or technical questions today?",
            confidence_threshold=0.75,
            is_active=True,
        )
        db.add(agent_cfg)

        # Subscription
        sub = Subscription(
            organization_id=org.id,
            plan="BUSINESS",
            max_monthly_messages=25000,
            current_month_messages=1420,
            max_knowledge_docs=100,
            max_agents=25,
            is_active=True,
        )
        db.add(sub)

        # Channels
        ch_web = Channel(
            organization_id=org.id,
            channel_type="WEBCHAT",
            name="Website Live Chat",
            is_enabled=True,
            config_json='{"theme": "indigo", "show_avatar": true}',
        )
        ch_wa = Channel(
            organization_id=org.id,
            channel_type="WHATSAPP",
            name="Official WhatsApp Line",
            is_enabled=True,
            config_json='{"phone_number": "+1 (555) 019-2834", "verified": true}',
        )
        db.add_all([ch_web, ch_wa])

        # Products
        products_data = [
            ("SKU-HP100", "Apex Pro Wireless Headphones", "Premium active noise-cancelling over-ear headphones with 40h battery.", "Audio", 249.99, 45),
            ("SKU-CH200", "Ergonomic Mesh Office Chair", "Adjustable lumbar support breathable high-back desk chair.", "Furniture", 329.00, 18),
            ("SKU-SW300", "Apex Smart Fitness Watch", "Waterproof GPS smartwatch with heart rate & SpO2 health tracking.", "Wearables", 179.50, 62),
            ("SKU-KB400", "Mechanical Gaming Keyboard RGB", "Hot-swappable custom mechanical keyboard with tactile switches.", "Accessories", 119.00, 30),
            ("SKU-DK500", "USB-C Dual 4K Monitor Dock", "12-in-1 universal Thunderbolt laptop docking station.", "Electronics", 149.00, 22),
            ("SKU-MS600", "Wireless Precision Ergonomic Mouse", "Multi-device ergonomic Bluetooth mouse with hyper-fast scroll.", "Accessories", 79.99, 50),
        ]
        products = []
        for sku, title, desc, cat, price, inv in products_data:
            p = Product(
                organization_id=org.id,
                sku=sku,
                title=title,
                description=desc,
                category=cat,
                price=price,
                currency="USD",
                inventory_count=inv,
                is_active=True,
            )
            db.add(p)
            products.append(p)
        await db.flush()

        # Customers
        customers_data = [
            ("Emma Watson", "emma.watson@example.com", "+1-555-0101", 3, 728.98, "VIP, Frequent Buyer"),
            ("David Miller", "david.miller@example.com", "+1-555-0102", 1, 249.99, "New Customer"),
            ("Sophia Chen", "sophia.chen@example.com", "+1-555-0103", 4, 1120.50, "VIP, Enterprise"),
            ("James Wilson", "james.wilson@example.com", "+1-555-0104", 2, 448.00, "Regular"),
            ("Olivia Taylor", "olivia.taylor@example.com", "+1-555-0105", 1, 119.00, "Support Active"),
        ]
        customers = []
        for name, email, phone, orders_cnt, ltv, tags in customers_data:
            c = Customer(
                organization_id=org.id,
                name=name,
                email=email,
                phone=phone,
                total_orders=orders_cnt,
                lifetime_value=ltv,
                tags=tags,
            )
            db.add(c)
            customers.append(c)
        await db.flush()

        # Orders
        orders_data = [
            ("ORD-10021", customers[0].id, "DELIVERED", 249.99, "FedEx", "FDX-998822", "123 Maple St, Boston MA", products[0]),
            ("ORD-10022", customers[0].id, "IN_TRANSIT", 478.99, "FedEx", "FDX-998823", "123 Maple St, Boston MA", products[1]),
            ("ORD-10023", customers[1].id, "PROCESSING", 249.99, "DHL", "DHL-441100", "456 Oak Ave, Seattle WA", products[0]),
            ("ORD-10024", customers[2].id, "IN_TRANSIT", 648.50, "FedEx", "FDX-332211", "789 Pine Blvd, Austin TX", products[2]),
            ("ORD-10025", customers[3].id, "DELIVERED", 119.00, "USPS", "9400111222", "321 Elm Rd, Denver CO", products[3]),
        ]
        for ord_num, cust_id, st, tot, carrier, trk, addr, prod in orders_data:
            o = Order(
                organization_id=org.id,
                customer_id=cust_id,
                order_number=ord_num,
                status=st,
                total_amount=tot,
                currency="USD",
                payment_status="PAID",
                carrier=carrier,
                tracking_number=trk,
                shipping_address=addr,
                estimated_delivery=datetime.now(timezone.utc) + timedelta(days=2),
                tracking_history_json=json.dumps([
                    {"status": "Shipment Picked Up", "location": "Warehouse Hub, Ohio", "timestamp": "2026-09-05T10:00:00Z"},
                    {"status": "In Transit to Regional Facility", "location": "Distribution Center, NJ", "timestamp": "2026-09-06T14:30:00Z"},
                ]),
            )
            db.add(o)
            await db.flush()

            item = OrderItem(
                order_id=o.id,
                product_id=prod.id,
                sku=prod.sku,
                title=prod.title,
                quantity=1,
                unit_price=prod.price,
                total_price=prod.price,
            )
            db.add(item)

        # Knowledge Base Documents & Chunks
        kb_docs = [
            (
                "30-Day Hassle-Free Return & Refund Policy",
                "POLICY",
                [
                    ("All items purchased directly from Apex Commerce can be returned within 30 days of delivery for a 100% full refund.", 1, "Return Eligibility"),
                    ("Items must be in original condition with original packaging and accessories. Return shipping labels are pre-paid and free for defective items.", 1, "Return Packaging & Labels"),
                    ("Once the return package is scanned at the carrier facility, refunds are automatically processed back to your original payment method within 3 to 5 business days.", 2, "Refund Processing Timeline"),
                ],
            ),
            (
                "Global Shipping & Delivery Timelines",
                "POLICY",
                [
                    ("Standard Shipping takes 3 to 5 business days across the continental US via FedEx Ground. Express 2-Day delivery is available at checkout.", 1, "Domestic Shipping"),
                    ("International orders ship via DHL Express and typically arrive within 5 to 8 business days. Customs duties and import taxes are calculated and collected at checkout.", 2, "International Delivery"),
                    ("Orders placed before 2:00 PM EST on business days are dispatched on the exact same day from our automated fulfillment center.", 2, "Same-Day Dispatch"),
                ],
            ),
            (
                "Apex Pro Headphones Troubleshooting & Warranty",
                "GUIDE",
                [
                    ("To factory reset your Apex Pro Headphones: Hold down the Power and Volume Down buttons simultaneously for 7 seconds until the LED flashes purple twice.", 1, "Factory Reset Instructions"),
                    ("All Apex audio hardware includes a 1-year comprehensive manufacturer warranty covering audio driver failure, Bluetooth connectivity issues, and battery defects.", 2, "1-Year Manufacturer Warranty"),
                ],
            ),
        ]

        for doc_title, ftype, chunks_info in kb_docs:
            doc = KnowledgeDocument(
                organization_id=org.id,
                title=doc_title,
                file_name=f"{doc_title.lower().replace(' ', '_')}.txt",
                file_type=ftype,
                file_size=len("".join([c[0] for c in chunks_info]).encode("utf-8")),
                status="READY",
                total_chunks=len(chunks_info),
            )
            db.add(doc)
            await db.flush()

            for idx, (content, page, section) in enumerate(chunks_info):
                emb = await get_embedding(content)
                chunk = KnowledgeChunk(
                    organization_id=org.id,
                    document_id=doc.id,
                    chunk_index=idx,
                    content=content,
                    embedding_json=json.dumps(emb),
                    token_count=len(content.split()),
                    source_name=doc_title,
                    page_number=page,
                    section_title=section,
                )
                db.add(chunk)

        # Conversations & Messages
        # Conv 1: Resolved Order tracking
        conv1 = Conversation(
            organization_id=org.id,
            customer_id=customers[0].id,
            channel="WEBCHAT",
            status="RESOLVED",
            current_intent="ORDER_STATUS",
            sentiment="POSITIVE",
            confidence_score=0.98,
            summary="Customer checked status of order ORD-10022. AI verified In Transit via FedEx.",
            resolved_at=datetime.now(timezone.utc),
        )
        db.add(conv1)
        await db.flush()

        msg1 = Message(
            organization_id=org.id,
            conversation_id=conv1.id,
            sender_type="CUSTOMER",
            sender_id=customers[0].id,
            content="Hi! Can you check the status of my order ORD-10022?",
            intent="ORDER_STATUS",
            sentiment="NEUTRAL",
        )
        msg2 = Message(
            organization_id=org.id,
            conversation_id=conv1.id,
            sender_type="AI",
            content="I've verified your order **ORD-10022**. Current status is **IN_TRANSIT** via **FedEx** (Tracking: `FDX-998823`). Estimated delivery is in 2 days to your address in Boston, MA.",
            intent="ORDER_STATUS",
            sentiment="POSITIVE",
            confidence=0.98,
            sources_json="[]",
            tool_calls_json=json.dumps([{"tool_name": "get_order_status", "arguments": {"order_id_or_number": "ORD-10022"}, "output": {"found": True, "status": "IN_TRANSIT"}}]),
        )
        msg3 = Message(
            organization_id=org.id,
            conversation_id=conv1.id,
            sender_type="CUSTOMER",
            sender_id=customers[0].id,
            content="Awesome, thank you so much!",
            intent="GENERAL",
            sentiment="POSITIVE",
        )
        db.add_all([msg1, msg2, msg3])

        # Conv 2: Waiting Human (Angry customer handoff)
        conv2 = Conversation(
            organization_id=org.id,
            customer_id=customers[1].id,
            channel="WHATSAPP",
            status="WAITING_HUMAN",
            current_intent="COMPLAINT",
            sentiment="ANGRY",
            confidence_score=1.0,
            summary="Customer reported receiving incorrect color item with high frustration. AI auto-escalated to human specialist.",
        )
        db.add(conv2)
        await db.flush()

        c2_m1 = Message(
            organization_id=org.id,
            conversation_id=conv2.id,
            sender_type="CUSTOMER",
            sender_id=customers[1].id,
            content="I ordered the Black headphones and you sent me Silver! This is completely unacceptable, connect me to a person right now!",
            intent="COMPLAINT",
            sentiment="ANGRY",
        )
        c2_m2 = Message(
            organization_id=org.id,
            conversation_id=conv2.id,
            sender_type="AI",
            content="I understand your frustration and I sincerely apologize for sending the wrong color. I have prioritized your request and am immediately transferring you to a human support specialist. An urgent ticket has been created.",
            intent="COMPLAINT",
            sentiment="ANGRY",
            confidence=1.0,
            tool_calls_json=json.dumps([{"tool_name": "request_human_agent", "arguments": {"reason": "Customer angry about wrong item", "urgency": "URGENT"}}]),
        )
        db.add_all([c2_m1, c2_m2])

        # Support Tickets
        tck1 = Ticket(
            organization_id=org.id,
            customer_id=customers[1].id,
            conversation_id=conv2.id,
            ticket_number="TCK-92811",
            subject="Urgent: Wrong color delivered (Silver instead of Black)",
            description="Customer received Silver headphones instead of Black on order ORD-10023. Urgent replacement needed.",
            status="OPEN",
            priority="URGENT",
            category="COMPLAINT",
            assigned_agent_id=agent1.id,
        )
        tck2 = Ticket(
            organization_id=org.id,
            customer_id=customers[2].id,
            ticket_number="TCK-92812",
            subject="Bulk invoice copy request for Q3 tax filing",
            description="Customer requesting PDF corporate tax invoice with VAT ID for order ORD-10024.",
            status="IN_PROGRESS",
            priority="MEDIUM",
            category="PAYMENT",
            assigned_agent_id=agent2.id,
        )
        db.add_all([tck1, tck2])

        # Feedbacks
        fb1 = Feedback(
            organization_id=org.id,
            conversation_id=conv1.id,
            customer_id=customers[0].id,
            rating=5,
            comment="Fastest support I've ever experienced! Instant order lookup.",
        )
        db.add(fb1)

        await db.commit()
        print("Demo data seeded successfully for Apex Commerce Inc. (API Key: spiq_live_apex_demo_key_9921)")


if __name__ == "__main__":
    asyncio.run(seed_database())
