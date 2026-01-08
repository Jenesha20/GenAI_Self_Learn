# app.py
import streamlit as st
import json
from datetime import datetime
from graph.workflow import build_workflow

# Initialize session state
def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'workflow' not in st.session_state:
        st.session_state.workflow = build_workflow()
    
    if 'chat_state' not in st.session_state:
        st.session_state.chat_state = {
            "messages": [],
            "cart_items": [],
            "context": {},
            "product_data": None
        }
    
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    if 'show_cart' not in st.session_state:
        st.session_state.show_cart = False

# Main app
def main():
    st.set_page_config(
        page_title="E-Pharmacy AI Assistant",
        page_icon="💊",
        layout="wide"
    )
    
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("💊 E-Pharmacy")
        st.markdown("---")
        
        # Cart section
        cart_count = len(st.session_state.chat_state.get("cart_items", []))
        st.subheader(f"🛒 Cart ({cart_count} items)")
        
        if cart_count > 0:
            for item in st.session_state.chat_state.get("cart_items", []):
                st.markdown(f"• **{item['name']}** × {item['qty']} - ₹{item.get('price', 0) * item['qty']}")
            
            total = sum(item.get('price', 0) * item['qty'] for item in st.session_state.chat_state.get("cart_items", []))
            st.markdown(f"**Total: ₹{total}**")
            
            if st.button("Clear Cart", type="secondary"):
                st.session_state.chat_state["cart_items"] = []
                st.rerun()
        else:
            st.info("Your cart is empty")
        
        st.markdown("---")
        
        # Quick actions
        st.subheader("Quick Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🛒 View Cart", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": "view cart"})
                st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.chat_state = {
                    "messages": [],
                    "cart_items": st.session_state.chat_state.get("cart_items", []),
                    "context": {},
                    "product_data": None
                }
                st.rerun()
        
        st.markdown("---")
        
        # Common queries
        st.subheader("Common Queries")
        queries = [
            "What are the products for cold?",
            "Show me pain relief medicines",
            "Add paracetamol to cart",
            "What are the side effects of ibuprofen?",
            "View my cart",
            "Checkout"
        ]
        
        for query in queries:
            if st.button(query, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": query})
                st.rerun()
        
        st.markdown("---")
        st.caption("💡 Powered by LangGraph Multi-Agent System")

    # Main chat area
    st.title("💬 E-Pharmacy AI Assistant")
    st.markdown("Ask about medicines, add to cart, or get health advice")
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepare state for workflow
        state = {
            "messages": [{"role": "user", "content": prompt}],
            "cart_items": st.session_state.chat_state.get("cart_items", []),
            "context": st.session_state.chat_state.get("context", {}),
            "product_data": st.session_state.chat_state.get("product_data", None)
        }
        
        # Run workflow
        with st.spinner("Processing..."):
            try:
                result = st.session_state.workflow.invoke(state)
                
                # Update chat state
                st.session_state.chat_state.update({
                    "cart_items": result.get("cart_items", []),
                    "context": result.get("context", {}),
                    "product_data": result.get("product_data", None)
                })
                
                # Get bot response
                bot_response = result.get("final_answer", "I'm not sure how to respond to that.")
                
                # Add bot message to chat
                st.session_state.messages.append({"role": "assistant", "content": bot_response})
                
                # Display bot response
                with st.chat_message("assistant"):
                    st.markdown(bot_response)
                    
                    # Show product details if available
                    if result.get("product_data"):
                        st.markdown("---")
                        st.markdown("**Product Details:**")
                        
                        if isinstance(result["product_data"], list):
                            for product in result["product_data"][:3]:
                                display_product(product, st)
                        else:
                            display_product(result["product_data"], st)
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
                with st.chat_message("assistant"):
                    st.error(error_msg)
        
        st.rerun()

def display_product(product, streamlit_context):
    """Display product information in a nice format"""
    with streamlit_context.expander(f"📦 {product.get('name', 'Unknown Product')}", expanded=False):
        cols = st.columns(2)
        
        with cols[0]:
            st.metric("Price", f"₹{product.get('price', 'N/A')}")
            
            if product.get('requires_prescription', False):
                st.warning("⚠️ Prescription Required")
            else:
                st.success("✅ OTC (Over-the-counter)")
            
            stock = product.get('stock_qty', 0)
            if stock > 0:
                st.success(f"📦 In Stock: {stock} units")
            else:
                st.error("❌ Out of Stock")
        
        with cols[1]:
            # Quick add to cart
            if st.button(f"Add {product.get('name', '')} to cart", 
                        key=f"add_{product.get('product_id', '')}"):
                # Add to chat
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"add {product.get('name', '')} to cart"
                })
                st.rerun()

if __name__ == "__main__":
    main()