INTENT_EXAMPLES = {

    # =====================================================
    # PRODUCT INFO — must hit DB / catalog
    # =====================================================
    "product_info": [

        # --- direct product queries (pattern-based) ---
        "I want to buy this medicine",
        "Tell me the price of this tablet",
        "How much does this medicine cost?",
        "Give me info about this drug",
        "Do you have this medicine in stock?",
        "Is this tablet available today?",

        # keep a FEW real examples only for grounding
        "I want to buy paracetamol",
        "Tell me the price of crocin",

        # --- category based ---
        "What medicines do you have for this problem?",
        "Show products for this condition",
        "List medicines for this illness",
        "What are the products available for this symptom?",
        "Do you have medicines for this allergy?",
        "Which medicines are there for stomach pain?",

        # --- alternatives / substitutes (GENERALIZED) ---
        "What are the alternatives for this medicine?",
        "Any substitute for this tablet?",
        "Similar medicines to this drug?",
        "What can I take instead of this medicine?",
        "Other options instead of this tablet",
        "Cheaper alternatives for this medicine",

        # keep 1–2 real examples only
        "What are the alternatives for paracetamol?",
        "Any substitute for crocin?",

        # --- availability / stock ---
        "Is this medicine in stock?",
        "Do you have this tablet right now?",
        "Which medicines are available today?",
    ],

    # =====================================================
    # CART ACTION
    # =====================================================
    "cart_action": [
        "Add this to my cart",
        "Put this in my cart",
        "Remove this item from my cart",
        "Delete this from my cart",
        "Show my cart",
        "What is in my cart?",
        "Clear my cart",
    ],

    # =====================================================
    # DRUG INTERACTION — safety-critical
    # =====================================================
    "drug_interaction": [

        # generalized patterns
        "Can I take this medicine with another one?",
        "Is it safe to combine these medicines?",
        "What happens if I mix two medicines?",
        "Can I take this tablet with alcohol?",
        "Is it okay to take one medicine with another?",

        # keep a few real examples
        "Can I take dolo with ibuprofen?",
        "Is paracetamol safe with alcohol?",
        "Can I take aspirin and warfarin together?",
    ],

    # =====================================================
    # FAQ — business / support
    # =====================================================
    "faq": [
        "What are your delivery timings?",
        "How to upload prescription?",
        "What is your return policy?",
        "How can I cancel my order?",
        "Do you support cash on delivery?",
        "How long does delivery take?",
        "How can I track my order?",
        "What if I receive a damaged product?",
    ],

    # =====================================================
    # GENERAL CHAT — explanations, chit-chat, education
    # =====================================================
    "general_chat": [

        # --- chit-chat ---
        "Hello",
        "Thanks",
        "Good morning",
        "How are you?",
        "Nice to meet you",

        # --- health education (NOT shopping) ---
        "What is fever?",
        "What are the symptoms of cold?",
        "How does this medicine work?",
        "What causes headache?",
        "Why do people get allergies?",
        "What is the difference between viral and bacterial infection?",

        # --- general advice (not product lookup) ---
        "How to reduce fever naturally?",
        "What home remedies help with cold?",
        "How to take care during flu?",
        "When should I see a doctor for fever?",
    ],
}
