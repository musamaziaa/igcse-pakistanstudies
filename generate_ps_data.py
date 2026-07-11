import json
import os

BASE = os.path.join(os.path.dirname(__file__), "backend", "data", "pak_studies")
os.makedirs(os.path.join(BASE, "question_bank", "section_a"), exist_ok=True)
os.makedirs(os.path.join(BASE, "question_bank", "section_b"), exist_ok=True)
os.makedirs(os.path.join(BASE, "question_bank", "section_c"), exist_ok=True)

# 1. Memorize Cards
cards = [
    {
        "id": "ps_const_dev",
        "section": "B",
        "category": "topic",
        "display_category": "history",
        "group_id": "constitution",
        "group_label": "Constitutional Development",
        "title": "Objectives Resolution & Constitutions",
        "arabic": "",
        "lines": [
            "Pakistan inherited the Government of India Act 1935 as its interim constitution.",
            "The Objectives Resolution (1949) was passed under PM Liaquat Ali Khan; it established Allah's sovereignty.",
            "The 1956 Constitution declared Pakistan an Islamic Republic and set up a parliamentary system.",
            "The 1962 Constitution, under Ayub Khan, created a presidential system with Basic Democracies.",
            "The 1973 Constitution, under Z.A. Bhutto, restored a parliamentary federal system by consensus.",
            "Key pattern: 1956 (parliamentary) -> 1962 (presidential) -> 1973 (parliamentary)."
        ]
    },
    {
        "id": "ps_foreign_policy",
        "section": "C",
        "category": "topic",
        "display_category": "foreign_policy",
        "group_id": "foreign_policy",
        "group_label": "Foreign Policy",
        "title": "Relations with India, USA & Neighbours",
        "arabic": "",
        "lines": [
            "Foreign policy protects national security, territorial integrity, and economic development.",
            "India relations are defined by the Kashmir dispute and three wars (1948, 1965, 1971).",
            "USA relations formed a strategic Cold-War alliance (SEATO, CENTO, War on Terror) but fluctuate.",
            "China is an 'all-weather' friend; cooperation includes major economic projects.",
            "Neighbour relations (Iran, Afghanistan) and SAARC membership promote peaceful borders and trade."
        ]
    },
    {
        "id": "ps_pakistan_movement",
        "section": "A",
        "category": "topic",
        "display_category": "history",
        "group_id": "pakistan_movement",
        "group_label": "Pakistan Movement",
        "title": "The Struggle for Pakistan (1905-1947)",
        "arabic": "",
        "lines": [
            "Two-Nation Theory: Hindus and Muslims were distinct nations deserving separate states.",
            "Partition of Bengal (1905) benefited Muslims; its annulment (1911) sparked political organisation.",
            "All-India Muslim League founded in 1906 at Dhaka to safeguard Muslim rights.",
            "Khilafat Movement (1919-24) built mass Muslim political consciousness.",
            "Jinnah's Fourteen Points (1929) demanded constitutional safeguards; Iqbal (1930) proposed a separate state.",
            "Lahore Resolution (23 March 1940) formally demanded independent Muslim states."
        ]
    },
    {
        "id": "ps_current_perspectives",
        "section": "C",
        "category": "topic",
        "display_category": "current_perspectives",
        "group_id": "current_perspectives",
        "group_label": "Current Perspectives",
        "title": "Youth, Environment & Governance",
        "arabic": "",
        "lines": [
            "Pakistan has a large youth population, offering a potential 'demographic dividend'.",
            "Education and civic engagement turn youth into drivers of innovation and entrepreneurship.",
            "Climate change threatens agriculture through floods, droughts, and water scarcity.",
            "Solutions include renewable energy (hydel, solar, wind) and sustainable environmental policies.",
            "Poverty, unemployment, and weak governance require stable institutions and inclusive growth."
        ]
    },
    {
        "id": "ps_economy_geography",
        "section": "B",
        "category": "topic",
        "display_category": "geography",
        "group_id": "economy",
        "group_label": "Economy & Geography",
        "title": "Agriculture, Water & Resources",
        "arabic": "",
        "lines": [
            "Agriculture provides employment, GDP, food security, and exports; cotton supplies the textile industry.",
            "Irrigation relies on the Indus River system; the Indus Water Treaty (1960) was mediated by the World Bank.",
            "Balochistan is the largest province by area; Punjab has the highest population density.",
            "Energy comes from non-renewables (coal, Sui gas) and renewables.",
            "Trade and transportation facilitate movement of goods, boosting economic growth."
        ]
    }
]

with open(os.path.join(BASE, "memorize_content.json"), "w") as f:
    json.dump({"cards": cards}, f, indent=2)


# 2. Syllabus
syllabus = {
    "topics": [
        {"id": "topic_1", "title": "History of Pakistan", "description": "Pakistan Movement, Constitutional Development"},
        {"id": "topic_2", "title": "Geography of Pakistan", "description": "Physical geography, climate, resources"},
        {"id": "topic_3", "title": "Economics of Pakistan", "description": "Agriculture, industry, trade"},
        {"id": "topic_4", "title": "Constitution of Pakistan", "description": "1956, 1962, 1973 Constitutions"},
        {"id": "topic_5", "title": "Foreign Policy", "description": "Relations with India, USA, China"},
        {"id": "topic_6", "title": "Current Perspectives", "description": "Youth, Environment, Governance"}
    ]
}

with open(os.path.join(BASE, "syllabus.json"), "w") as f:
    json.dump(syllabus, f, indent=2)


# 3. Question Bank - MCQs (Section A)
mcqs = [
    {
        "section": "A",
        "type": "MCQ",
        "topic_number": 1,
        "topic_title": "History of Pakistan",
        "question": "The Partition of Bengal was carried out in which year?",
        "options": {"A": "1905", "B": "1906", "C": "1911", "D": "1940"},
        "model_answer": "A",
        "marks": 1
    },
    {
        "section": "A",
        "type": "MCQ",
        "topic_number": 1,
        "topic_title": "History of Pakistan",
        "question": "Where and when was the All-India Muslim League founded?",
        "options": {"A": "Lahore, 1940", "B": "Dhaka, 1906", "C": "Delhi, 1905", "D": "Aligarh, 1906"},
        "model_answer": "B",
        "marks": 1
    },
    {
        "section": "A",
        "type": "MCQ",
        "topic_number": 2,
        "topic_title": "Geography of Pakistan",
        "question": "Which is Pakistan's largest province by area?",
        "options": {"A": "Punjab", "B": "Sindh", "C": "Balochistan", "D": "KPK"},
        "model_answer": "C",
        "marks": 1
    },
    {
        "section": "A",
        "type": "MCQ",
        "topic_number": 2,
        "topic_title": "Geography of Pakistan",
        "question": "When was the Indus Water Treaty signed and who mediated it?",
        "options": {"A": "1948, UN", "B": "1960, World Bank", "C": "1962, USA", "D": "1971, World Bank"},
        "model_answer": "B",
        "marks": 1
    }
]

with open(os.path.join(BASE, "question_bank", "section_a", "mcqs.json"), "w") as f:
    json.dump({"questions": mcqs}, f, indent=2)


# 4. Question Bank - Short Answers (Section B)
short_answers = [
    {
        "section": "B",
        "type": "short_answer",
        "topic_number": 4,
        "topic_title": "Constitution of Pakistan",
        "question": "What were the key objectives of the Objectives Resolution (1949)? [5]",
        "model_answer": "Allah's sovereignty over the universe; democracy, freedom, equality and social justice as enunciated by Islam; fundamental rights for all citizens; Muslims to live according to the Qur'an and Sunnah; protection of minority rights; and an independent judiciary.",
        "marks": 5
    },
    {
        "section": "B",
        "type": "short_answer",
        "topic_number": 3,
        "topic_title": "Economics of Pakistan",
        "question": "Explain how trade and transportation contribute to Pakistan's economy. [5]",
        "model_answer": "They facilitate the movement of goods and services; encourage domestic and international trade; support industrial and agricultural development; generate employment; and improve regional connectivity and economic growth.",
        "marks": 5
    }
]

with open(os.path.join(BASE, "question_bank", "section_b", "short_answers.json"), "w") as f:
    json.dump({"questions": short_answers}, f, indent=2)


# 5. Question Bank - Long Answers (Section C)
long_answers = [
    {
        "section": "C",
        "type": "extended",
        "topic_number": 5,
        "topic_title": "Foreign Policy",
        "question": "Analyse Pakistan's relations with India and the USA. How have these relationships influenced its foreign policy and regional security? [8]",
        "model_answer": "Pakistan's foreign policy has been shaped above all by its relations with India and the USA. With India, the relationship has been dominated by historical disputes (Kashmir) and three wars (1948, 1965, 1971). These tensions forced Pakistan to make national security the centre of its policy. With the USA, Pakistan built a strategic Cold-War alliance (SEATO, CENTO) receiving military/economic aid, but this relationship fluctuated with shifting interests. Overall, India pushed Pakistan toward a security-driven posture while the USA brought resources but also unpredictability.",
        "marks": 8
    },
    {
        "section": "C",
        "type": "extended",
        "topic_number": 6,
        "topic_title": "Current Perspectives",
        "question": "Evaluate the role of youth in shaping Pakistan's future. [7]",
        "model_answer": "Youth are decisive because they form a large share of the population (demographic dividend). Education gives them skills, civic engagement makes them responsible citizens, and they drive innovation and entrepreneurship. However, this potential depends on investment - without it, a youth bulge can worsen instability. On balance, youth are Pakistan's greatest asset provided the state educates and engages them.",
        "marks": 7
    }
]

with open(os.path.join(BASE, "question_bank", "section_c", "long_answers.json"), "w") as f:
    json.dump({"questions": long_answers}, f, indent=2)

print("Pakistan Studies data generated successfully!")
