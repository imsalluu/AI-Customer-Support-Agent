import json
from typing import Any, Dict, List, Optional
import httpx
from app.core.config import settings


class LLMClient:
    @staticmethod
    async def generate_response(
        system_prompt: str,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        grounded_context: Optional[str] = None,
        tool_results: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        """Calls external LLM if configured, or uses structured context generator."""
        # Check for OpenAI API key
        if settings.OPENAI_API_KEY:
            try:
                messages = [{"role": "system", "content": system_prompt}]
                
                # Add context as system instructions
                if grounded_context:
                    messages.append({
                        "role": "system",
                        "content": f"Use ONLY the following verified knowledge base documents to answer:\n\n{grounded_context}",
                    })
                if tool_results:
                    messages.append({
                        "role": "system",
                        "content": f"Use the following real-time database tool outputs:\n\n{json.dumps(tool_results, indent=2)}",
                    })

                # Append history
                for msg in conversation_history[-6:]:
                    messages.append({"role": msg["role"], "content": msg["content"]})

                messages.append({"role": "user", "content": user_message})

                async with httpx.AsyncClient(timeout=20.0) as client:
                    res = await client.post(
                        "https://api.openai.com/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": settings.DEFAULT_LLM_MODEL,
                            "messages": messages,
                            "temperature": 0.2,
                        },
                    )
                    if res.status_code == 200:
                        data = res.json()
                        return data["choices"][0]["message"]["content"].strip()
            except Exception:
                pass  # Fallback to local grounded generator

        # Built-in Intelligent Grounded Synthesizer
        return LLMClient._synthesize_grounded_response(user_message, grounded_context, tool_results)

    @staticmethod
    def _synthesize_grounded_response(
        user_message: str,
        grounded_context: Optional[str] = None,
        tool_results: Optional[List[Dict[str, Any]]] = None,
    ) -> str:
        parts = []

        # 1. Format Tool results if available
        if tool_results:
            for tr in tool_results:
                tool_name = tr.get("tool_name")
                out = tr.get("output", {})

                if tool_name == "get_order_status":
                    if out.get("found"):
                        items_str = ", ".join([f"{i['quantity']}x {i['title']}" for i in out.get("items", [])])
                        parts.append(
                            f"I've verified your order **{out.get('order_number')}**. Current status is **{out.get('status')}** (Payment: {out.get('payment_status')}).\n\n"
                            f"• **Carrier:** {out.get('carrier')}\n"
                            f"• **Tracking Number:** `{out.get('tracking_number')}`\n"
                            f"• **Estimated Delivery:** {out.get('estimated_delivery')}\n"
                            f"• **Items:** {items_str}\n"
                            f"• **Total:** {out.get('total')}"
                        )
                    else:
                        parts.append(out.get("message", "I could not locate this order in our records."))

                elif tool_name == "check_shipping":
                    if out.get("found"):
                        parts.append(
                            f"Your shipment for order **{out.get('order_number')}** is currently **{out.get('status')}** via **{out.get('carrier')}**.\n"
                            f"Tracking Number: `{out.get('tracking_number')}`. Estimated delivery date: **{out.get('estimated_delivery')}**."
                        )
                    else:
                        parts.append(out.get("message", "Shipping record not found."))

                elif tool_name == "search_products":
                    products = out.get("products", [])
                    if products:
                        prod_lines = [
                            f"• **{p['title']}** (SKU: `{p['sku']}`) — {p['price']} ({'In Stock' if p['in_stock'] else 'Out of Stock'})"
                            for p in products
                        ]
                        parts.append("Here are the matching products from our catalog:\n\n" + "\n".join(prod_lines))
                    else:
                        parts.append("I searched our product catalog but did not find exact matching items.")

                elif tool_name == "check_inventory":
                    parts.append(
                        f"**{out.get('title', 'Product')}** (SKU: `{out.get('sku')}`) is currently **{out.get('status')}** with {out.get('inventory_count', 0)} units in stock."
                    )

                elif tool_name == "create_support_ticket":
                    parts.append(
                        f"I have created an official support ticket for you:\n\n"
                        f"• **Ticket Number:** `{out.get('ticket_number')}`\n"
                        f"• **Status:** {out.get('status')}\n"
                        f"• **Priority:** {out.get('priority')}\n\n"
                        f"Our support specialists have been assigned and will follow up shortly."
                    )

                elif tool_name == "request_human_agent":
                    parts.append(out.get("handoff_message", "Connecting you to a human agent."))

        # 2. Format RAG Knowledge if available
        if grounded_context:
            clean_context = grounded_context.strip()
            if clean_context:
                if parts:
                    parts.append("\n**Additional Information:**\n" + clean_context)
                else:
                    parts.append(clean_context)

        # 3. Default fallback if no tools or RAG
        if not parts:
            parts.append(
                "Thank you for contacting support! How can I assist you with your order status, product inquiries, returns, or technical questions today?"
            )

        return "\n\n".join(parts)
