import json
import os

mem_path = '/home/zia/igcse_pakstudies/backend/data/pak_studies/memorize_content.json'
mcq_path = '/home/zia/igcse_pakstudies/backend/data/pak_studies/question_bank/section_a/mcqs.json'

# Add Memorize Cards
with open(mem_path, 'r') as f:
    mem_data = json.load(f)

new_cards = [
    {
        "id": "tier1_critical",
        "section": "A",
        "category": "topic",
        "display_category": "tier1",
        "group_id": "tier1",
        "group_label": "Tier 1: Critical",
        "title": "History & Constitution of Pakistan",
        "arabic": "",
        "lines": [
            "Tier 1 covers the foundational elements of Pakistan's existence.",
            "The History of Pakistan spans from the Mughal decline to the post-independence era.",
            "Key events include the 1905 Partition of Bengal and the 1940 Lahore Resolution.",
            "The Constitutional history involves the 1956, 1962, and 1973 Constitutions.",
            "The 1973 Constitution established fundamental rights and a parliamentary federal system."
        ]
    },
    {
        "id": "tier2_important",
        "section": "B",
        "category": "topic",
        "display_category": "tier2",
        "group_id": "tier2",
        "group_label": "Tier 2: Most Important",
        "title": "Geography, Economy & Foreign Policy",
        "arabic": "",
        "lines": [
            "Tier 2 covers Pakistan's physical layout, resources, and international relations.",
            "Geography includes the Indus Water Treaty (1960) and agricultural/energy resources.",
            "Economics focuses on the roles of agriculture and industry in GDP and sustainable development.",
            "Foreign Policy prioritizes relations with India, USA, China, and Afghanistan.",
            "Pakistan's strategic location and nuclear program are vital to its foreign relations."
        ]
    },
    {
        "id": "tier3_nice",
        "section": "C",
        "category": "topic",
        "display_category": "tier3",
        "group_id": "tier3",
        "group_label": "Tier 3: Nice to Learn",
        "title": "Current Perspectives & Future",
        "arabic": "",
        "lines": [
            "Tier 3 focuses on contemporary socio-economic challenges and opportunities.",
            "Key challenges include poverty, unemployment, governance, and rural-urban migration.",
            "The youth population is seen as a major demographic dividend.",
            "Technological advancements and education are essential for 21st-century growth.",
            "Youth-led initiatives can significantly shape the future direction of Pakistan."
        ]
    }
]

mem_data['cards'].extend(new_cards)
with open(mem_path, 'w') as f:
    json.dump(mem_data, f, indent=2)

# Add Exam Questions
with open(mcq_path, 'r') as f:
    mcq_data = json.load(f)

new_mcqs = [
    {
        "section": "A",
        "type": "MCQ",
        "topic_number": 4,
        "topic_title": "Tier 1 - Constitution",
        "question": "Which Constitution of Pakistan first introduced a presidential system?",
        "options": {
            "A": "1956",
            "B": "1962",
            "C": "1973",
            "D": "1949 Objectives Resolution"
        },
        "model_answer": "B",
        "marks": 1
    },
    {
        "section": "A",
        "type": "MCQ",
        "topic_number": 3,
        "topic_title": "Tier 2 - Economics",
        "question": "Which sector is considered the backbone of Pakistan's economy, providing food security and employment?",
        "options": {
            "A": "Information Technology",
            "B": "Manufacturing",
            "C": "Agriculture",
            "D": "Tourism"
        },
        "model_answer": "C",
        "marks": 1
    },
    {
        "section": "A",
        "type": "MCQ",
        "topic_number": 6,
        "topic_title": "Tier 3 - Current Perspectives",
        "question": "What is widely regarded as a 'demographic dividend' for Pakistan's future development?",
        "options": {
            "A": "Its large youth population",
            "B": "Its aging workforce",
            "C": "High rates of rural migration",
            "D": "A declining birth rate"
        },
        "model_answer": "A",
        "marks": 1
    }
]

mcq_data['questions'].extend(new_mcqs)
with open(mcq_path, 'w') as f:
    json.dump(mcq_data, f, indent=2)

print("Successfully added Tier 1, 2, 3 topics to Memorize and Exam Bank!")
