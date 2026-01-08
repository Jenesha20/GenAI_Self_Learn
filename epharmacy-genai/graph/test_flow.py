# test_complete_flow.py
from graph.workflow import build_workflow

def test_complete_flow():
    """Test the complete conversation flow"""
    workflow = build_workflow()
    
    print("=" * 60)
    print("TEST: Complete Cart Flow")
    print("=" * 60)
    
    # Initialize state
    state = {
        "messages": [],
        "cart_items": [],
        "context": {}
    }
    
    # Step 1: User asks for cold products
    print("\n👤 User: what are the products available for cold?")
    state["messages"] = [{"role": "user", "content": "what are the products available for cold?"}]
    
    result = workflow.invoke(state)
    print(f"🤖 Bot: {result.get('final_answer', 'No answer')[:100]}...")
    state = result
    
    # Step 2: User adds specific product to cart
    print("\n👤 User: add paracetamol to cart")
    state["messages"] = state.get("messages", []) + [{"role": "user", "content": "add paracetamol to cart"}]
    
    result = workflow.invoke(state)
    print(f"🤖 Bot: {result.get('final_answer', 'No answer')}")
    
    # Check if we're awaiting quantity
    if result.get("awaiting_quantity"):
        print(f"✅ System is awaiting quantity input")
        print(f"   Current product: {result.get('current_product', {}).get('name', 'None')}")
    
    state = result
    
    # Step 3: User provides quantity
    print("\n👤 User: 2")
    state["messages"] = state.get("messages", []) + [{"role": "user", "content": "2"}]
    
    result = workflow.invoke(state)
    print(f"🤖 Bot: {result.get('final_answer', 'No answer')}")
    
    # Check cart
    print(f"📦 Cart items: {result.get('cart_items', [])}")
    
    state = result
    
    # Step 4: User views cart
    print("\n👤 User: view cart")
    state["messages"] = state.get("messages", []) + [{"role": "user", "content": "view cart"}]
    
    result = workflow.invoke(state)
    print(f"🤖 Bot: {result.get('final_answer', 'No answer')}")

if __name__ == "__main__":
    test_complete_flow()