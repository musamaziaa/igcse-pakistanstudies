#!/usr/bin/env python3
"""
Updates memorize_content.json and question bank JSON files with:
1. display_category field on all existing cards
2. New memorize cards for all requested topics
3. New fill-in-blank + short_answer quiz questions
"""
import json, os

BASE = os.path.join(os.path.dirname(__file__), "islamiyat_prep", "data")

# ── Category mapping for existing groups ────────────────────────────────────
GROUP_CAT = {
    "topic_1_birth":         "prophets_life",
    "topic_1_revelation":    "prophets_life",
    "topic_1_persecution":   "prophets_life",
    "topic_1_isra":          "prophets_life",
    "topic_1_hijrah":        "prophets_life",
    "topic_2_revelation":    "quran_law",
    "topic_2_preservation":  "quran_law",
    "topic_2_abubakar":      "quran_law",
    "topic_2_uthman":        "quran_law",
    "topic_3_companions":    "companions",
    "topic_3_wives":         "wives",
    "topic_3_daughters":     "ahl_e_bayt",
    "topic_4_six_articles":  "islamic_faith",
    "topic_4_tawheed":       "islamic_faith",
    "topic_4_books":         "islamic_faith",
    "topic_4_judgement":     "islamic_faith",
    "topic_5_madinah":       "treaties_events",
    "topic_5_badr":          "battles",
    "topic_5_uhud":          "battles",
    "topic_5_khandaq":       "battles",
    "topic_5_hudaybiyah":    "treaties_events",
    "topic_5_emperors":      "treaties_events",
    "topic_5_khyber":        "battles",
    "topic_5_hunain":        "battles",
    "topic_5_farewell":      "treaties_events",
    "topic_6_sunnah":        "quran_law",
    "topic_6_parts":         "quran_law",
    "topic_7_family":        "society_law",
    "topic_7_rulers":        "society_law",
    "topic_8_shahadah_salah":"pillars",
    "topic_8_zakat_sawm":    "pillars",
    "topic_8_hajj":          "pillars",
}

# ── New memorize cards ───────────────────────────────────────────────────────
NEW_CARDS = [

    # ── Prophet's Life & Mission ─────────────────────────────────────────────
    {
        "id": "prophets_caves",
        "section": "B",
        "category": "topic",
        "display_category": "prophets_life",
        "group_id": "prophets_caves",
        "group_label": "Prophet's Experience in Caves",
        "title": "Prophet's Experience in Caves — Hira & Thawr",
        "arabic": "",
        "lines": [
            "Cave of Hira: situated on Jabal al-Nour near Makkah; the Prophet retreated here regularly for prayer and contemplation (Tahannuth).",
            "It was in Cave Hira that Angel Jibreel appeared in 610 CE and commanded 'Iqra!' (Read/Recite) three times.",
            "The first five verses of Surah Al-Alaq were revealed here — the beginning of prophethood.",
            "Cave of Thawr: located south of Makkah; the Prophet and Abu Bakr (RA) hid here for three days during the Hijrah in 622 CE.",
            "The Quraysh searched everywhere but could not find them — Allah miraculously protected them.",
            "According to tradition, a spider wove its web and a pigeon laid eggs at the cave entrance, deterring the pursuers.",
            "Both caves represent pivotal moments: Hira marks the start of prophethood; Thawr marks the start of the Islamic state.",
        ],
    },
    {
        "id": "early_preaching",
        "section": "B",
        "category": "topic",
        "display_category": "prophets_life",
        "group_id": "early_preaching",
        "group_label": "Early Preaching of Islam",
        "title": "Early Preaching — Secret and Public",
        "arabic": "",
        "lines": [
            "After the first revelation in 610 CE, the Prophet preached Islam secretly for three years to protect early Muslims.",
            "Meetings were held at the house of Arqam ibn Abi al-Arqam (Dar al-Arqam) in Makkah.",
            "First converts: Khadijah (RA) — wife; Ali (RA) — child; Abu Bakr (RA) — adult male; Zayd ibn Harithah (RA) — freed slave.",
            "The message focused on Tawhid (one God), abandoning idols, honesty, and caring for the poor and orphans.",
            "After three years, Allah revealed: 'And warn your closest relatives' (Surah Ash-Shu'ara 26:214).",
            "The Prophet gathered the Quraysh on Mount Safa and publicly declared his prophethood.",
            "Most Quraysh leaders rejected him and began active persecution of the Muslims.",
        ],
    },
    {
        "id": "first_revelation_detail",
        "section": "B",
        "category": "topic",
        "display_category": "prophets_life",
        "group_id": "first_revelation_detail",
        "group_label": "The First Revelation",
        "title": "The First Revelation — Cave of Hira (610 CE)",
        "arabic": "",
        "lines": [
            "In 610 CE, the Prophet was 40 years old and meditating alone in Cave Hira during the month of Ramadan.",
            "Angel Jibreel appeared and commanded 'Iqra!' (Read/Recite!); the Prophet replied 'I cannot read' — three times.",
            "On the third embrace, the angel revealed the first five verses of Surah Al-Alaq (96:1–5): 'Read in the name of your Lord who created...'",
            "The Prophet returned home trembling with fear; Khadijah (RA) wrapped him in a blanket and comforted him.",
            "She took him to her cousin Waraqah ibn Nawfal — a Christian scholar — who confirmed it was the same angel that came to Prophet Musa (AS).",
            "Waraqah said: 'Your people will drive you out' — predicting the hardships of the mission ahead.",
            "This event marked the beginning of prophethood and the revelation of the Quran over the next 23 years.",
        ],
    },
    {
        "id": "isra_miraj_detail",
        "section": "B",
        "category": "topic",
        "display_category": "prophets_life",
        "group_id": "isra_miraj_detail",
        "group_label": "Isra and Mi'raj (Night Journey)",
        "title": "Isra and Mi'raj — The Night Journey & Heavenly Ascension",
        "arabic": "",
        "lines": [
            "Isra: the miraculous night journey in 620 CE from Masjid al-Haram (Makkah) to Masjid al-Aqsa (Jerusalem) on the Buraq.",
            "At Masjid al-Aqsa, the Prophet led all previous prophets in prayer — confirming his status as the final and greatest prophet.",
            "Mi'raj: the ascension through the seven heavens, accompanied by Angel Jibreel.",
            "The Prophet met and exchanged greetings with: Adam (AS), Yahya & Isa (AS), Yusuf (AS), Idris (AS), Harun (AS), Musa (AS), and Ibrahim (AS).",
            "He reached Sidrat al-Muntaha (Lote Tree of the Utmost Boundary) — the farthest limit any creation can reach.",
            "Allah prescribed 50 daily prayers; at Musa's (AS) advice, the Prophet repeatedly requested reduction until five were finalised.",
            "Abu Bakr (RA) immediately believed the Prophet's account, earning the title 'As-Siddiq' (The Confirmer of Truth).",
        ],
    },
    {
        "id": "visit_taif",
        "section": "B",
        "category": "topic",
        "display_category": "prophets_life",
        "group_id": "visit_taif",
        "group_label": "Visit to Ta'if",
        "title": "The Prophet's Mission to Ta'if (619 CE)",
        "arabic": "",
        "lines": [
            "After the Year of Grief (619 CE), with no protection in Makkah, the Prophet traveled to Ta'if seeking support.",
            "He was accompanied by his loyal companion and adopted son Zayd ibn Harithah (RA).",
            "He met the three leaders of the Banu Thaqif tribe — all three mocked and rejected him.",
            "The leaders incited the children and slaves to chase and stone him out of the city; both the Prophet and Zayd were injured and bleeding.",
            "Taking refuge in a garden near Ta'if, the Prophet made his famous heartfelt dua: 'O Allah, I complain to You of my weakness and helplessness...'",
            "An angel appeared offering to crush Ta'if between two mountains; the Prophet refused, praying that their descendants might one day accept Islam.",
            "This event is a powerful example of the Prophet's extraordinary patience, mercy, and absolute trust in Allah.",
        ],
    },
    {
        "id": "causes_hijrah",
        "section": "B",
        "category": "topic",
        "display_category": "prophets_life",
        "group_id": "causes_hijrah",
        "group_label": "Causes of Migration to Madinah",
        "title": "Causes of the Hijrah to Madinah",
        "arabic": "",
        "lines": [
            "The Quraysh subjected Muslims to years of physical torture, economic boycott, and social isolation in Makkah.",
            "The three-year social and economic boycott of Banu Hashim (616–619 CE) caused extreme suffering and starvation.",
            "In the Year of Grief (619 CE), Khadijah (RA) and Abu Talib both died — the Prophet lost his greatest emotional and tribal protection.",
            "The mission to Ta'if (619 CE) failed completely, leaving no prospect of support elsewhere in Arabia.",
            "The Pledges of Aqabah (621–622 CE): people of Yathrib accepted Islam and pledged to protect the Prophet — creating a viable new base.",
            "The Quraysh held a secret council and plotted to assassinate the Prophet simultaneously so no single tribe could be blamed.",
            "Allah commanded the Prophet to migrate; the Hijrah became both a necessity and a divine command.",
        ],
    },
    {
        "id": "events_hijrah",
        "section": "B",
        "category": "topic",
        "display_category": "prophets_life",
        "group_id": "events_hijrah",
        "group_label": "Events of the Hijrah",
        "title": "Events of the Hijrah — The Migration to Madinah (622 CE)",
        "arabic": "",
        "lines": [
            "The Quraysh surrounded the Prophet's house planning to kill him at dawn; Hazrat Ali (RA) slept in his bed to deceive them.",
            "The Prophet and Abu Bakr (RA) slipped away secretly at night and hid in Cave Thawr for three days.",
            "Asma bint Abu Bakr (RA) brought them food and news daily; Abdullah ibn Abu Bakr gathered intelligence from Makkah.",
            "After three days they traveled south then northwest, guided by Abdullah ibn Urayqit along an unfamiliar coastal route.",
            "Suraqah ibn Malik pursued them for reward; his horse sank into the sand three times — he accepted it as a divine sign and turned back.",
            "They arrived at Quba on the outskirts of Madinah, where the Prophet built Masjid Quba — the first mosque in Islamic history.",
            "The Prophet formally entered Madinah on 12 Rabi al-Awwal 1 AH; the Ansar welcomed him with great joy and the Hijrah marks the start of the Islamic calendar.",
        ],
    },

    # ── Treaties & Key Events ────────────────────────────────────────────────
    {
        "id": "charter_madinah",
        "section": "C",
        "category": "topic",
        "display_category": "treaties_events",
        "group_id": "charter_madinah",
        "group_label": "Charter of Madinah",
        "title": "The Charter of Madinah (622 CE)",
        "arabic": "",
        "lines": [
            "Written by the Prophet (pbuh) shortly after the Hijrah in 622 CE — considered the first written constitution in history.",
            "Declared all Muslims (Muhajirun and Ansar) as one unified Ummah, with equal rights and mutual support.",
            "Granted full religious freedom to Jewish tribes, Christians, and other groups living in Madinah.",
            "All citizens — regardless of religion — were required to defend Madinah jointly against any external attack.",
            "No group could make a separate peace treaty with the enemy; all disputes were to be referred to the Prophet (pbuh).",
            "Prohibited treachery, injustice, and wrongdoing within the city; established principles of justice and equality.",
            "Demonstrated the Prophet's remarkable wisdom as a statesman and laid the foundation of the first Islamic state.",
        ],
    },
    {
        "id": "events_after_hijrah",
        "section": "C",
        "category": "topic",
        "display_category": "treaties_events",
        "group_id": "events_after_hijrah",
        "group_label": "Events After Migration to Madinah",
        "title": "Key Events After the Hijrah to Madinah",
        "arabic": "",
        "lines": [
            "The Prophet built Masjid al-Nabawi in Madinah — the second mosque in Islam and the centre of the new Islamic community.",
            "Brotherhood (Mu'akhat) was established between Muhajirun (migrants) and Ansar (helpers) — each Ansar shared home and wealth.",
            "The Charter of Madinah was signed, uniting all tribes and establishing Madinah as an Islamic state.",
            "The Adhan (call to prayer) was introduced and the Qiblah was changed from Jerusalem to Makkah in 2 AH.",
            "Three major battles tested the new community: Badr (2 AH), Uhud (3 AH), and Khandaq (5 AH).",
            "The Treaty of Hudaybiya (6 AH) and Conquest of Makkah (8 AH) extended Muslim power across Arabia.",
            "The Prophet passed away in 11 AH / 632 CE having completed the mission of Islam throughout the Arabian Peninsula.",
        ],
    },
    {
        "id": "treaty_hudaibiya_detail",
        "section": "C",
        "category": "topic",
        "display_category": "treaties_events",
        "group_id": "treaty_hudaibiya_detail",
        "group_label": "Treaty of Hudaibiya (Detailed)",
        "title": "Treaty of Hudaibiya — A Clear Victory (6 AH / 628 CE)",
        "arabic": "",
        "lines": [
            "In 6 AH, the Prophet marched with 1,400 companions intending to perform Umrah; the Quraysh blocked their entry near Hudaibiya.",
            "Key terms: a 10-year peace, Muslims to return that year and come the following year; any Muslim fleeing to Makkah not to be returned.",
            "Many companions were upset, feeling the terms favoured the Quraysh; Umar (RA) questioned the agreement openly.",
            "The Prophet accepted the treaty with wisdom; Allah revealed: 'Indeed We have granted you a clear victory' (Surah Al-Fath 48:1).",
            "During the peace, Islam spread rapidly through preaching — more people accepted Islam than in all previous years combined.",
            "In 8 AH, Quraysh allies attacked a Muslim-allied tribe, breaking the treaty; the Prophet marched on Makkah with 10,000.",
            "The treaty demonstrated that diplomacy and patience can achieve greater results than force.",
        ],
    },
    {
        "id": "battle_trench_detail",
        "section": "C",
        "category": "topic",
        "display_category": "battles",
        "group_id": "battle_trench_detail",
        "group_label": "Battle of the Trench (Detailed)",
        "title": "Battle of the Trench (Khandaq) — 5 AH / 627 CE",
        "arabic": "",
        "lines": [
            "The Quraysh formed a massive confederacy (Ahzab) of approximately 10,000 soldiers from multiple tribes to destroy Madinah.",
            "Salman al-Farsi (RA) suggested digging a trench on the exposed northern side — an innovative Persian defensive strategy.",
            "The trench was dug by 3,000 Muslims in just six days; the Prophet worked alongside them, boosting morale.",
            "The confederacy laid siege for nearly a month but could not cross the trench; cavalry was rendered completely ineffective.",
            "Harsh winter, food shortages, and growing internal divisions weakened the confederacy's resolve.",
            "The Banu Qurayza tribe violated their treaty with the Muslims during the siege — they were later dealt with after the battle.",
            "The enemy forces retreated in failure; the Quraysh threat to Madinah was ended permanently — a decisive strategic victory.",
        ],
    },

    # ── Companions ───────────────────────────────────────────────────────────
    {
        "id": "bio_abubakar",
        "section": "B",
        "category": "topic",
        "display_category": "companions",
        "group_id": "bio_abubakar",
        "group_label": "Biography: Hazrat Abu Bakr (RA)",
        "title": "Hazrat Abu Bakr al-Siddiq (RA) — First Caliph",
        "arabic": "",
        "lines": [
            "Full name: Abdullah ibn Abi Quhafa; titled 'As-Siddiq' (The Confirmer of Truth) for immediately believing the Isra & Mi'raj.",
            "First adult male to accept Islam; closest and most trusted companion of the Prophet throughout his life.",
            "Used his personal wealth to free tortured Muslim slaves including Bilal (RA), Ammar (RA), and others.",
            "Accompanied the Prophet during the Hijrah, hiding with him in Cave Thawr for three days at great personal risk.",
            "Led the congregational prayers during the Prophet's final illness — a sign of his designated leadership.",
            "Became the First Caliph (632–634 CE); united the Muslims, crushed apostasy (Riddah wars), and initiated the first written compilation of the Quran.",
            "Died in 13 AH / 634 CE after just two years as Caliph; buried beside the Prophet in Madinah.",
        ],
    },
    {
        "id": "bio_usman",
        "section": "B",
        "category": "topic",
        "display_category": "companions",
        "group_id": "bio_usman",
        "group_label": "Biography: Hazrat Usman (RA)",
        "title": "Hazrat Uthman ibn Affan (RA) — Dhul-Nurayn",
        "arabic": "",
        "lines": [
            "Full name: Uthman ibn Affan; titled 'Dhul-Nurayn' (Holder of Two Lights) for marrying two daughters of the Prophet.",
            "One of the earliest converts to Islam; gave up wealth and comfort and migrated twice — to Abyssinia and to Madinah.",
            "Known for extraordinary generosity — personally financed the entire Muslim army for the Battle of Tabuk.",
            "Third Caliph of Islam (644–656 CE); his caliphate saw Islam expand into Persia, North Africa, and Central Asia.",
            "Greatest achievement: standardised the Quran into one authoritative Mushaf based on the Qurayshi dialect.",
            "Sent official copies to all major cities and ordered all other dialect versions burned to prevent division.",
            "Martyred in 35 AH / 656 CE while reciting the Quran in his home; his blood fell on the Mushaf.",
        ],
    },
    {
        "id": "bio_ali",
        "section": "B",
        "category": "topic",
        "display_category": "companions",
        "group_id": "bio_ali",
        "group_label": "Biography: Hazrat Ali (RA)",
        "title": "Hazrat Ali ibn Abi Talib (RA) — Fourth Caliph",
        "arabic": "",
        "lines": [
            "Cousin and son-in-law of the Prophet; raised in the Prophet's own household from a young age.",
            "First child to accept Islam; his faith and dedication to the Prophet were lifelong and unwavering.",
            "Married Fatimah al-Zahra (RA), the Prophet's most beloved daughter; father of Hasan and Husain (RA).",
            "Slept in the Prophet's bed on the night of Hijrah to deceive Quraysh assassins — risking his own life.",
            "Known as 'Asadullah' (Lion of Allah) for exceptional bravery in battles including Badr, Uhud, and Khandaq.",
            "Renowned for deep Islamic knowledge and wisdom; called 'Bab al-Ilm' (Gate of Knowledge) by the Prophet.",
            "Fourth Caliph (656–661 CE); martyred while performing Fajr prayer in the mosque of Kufa in 40 AH.",
        ],
    },
    {
        "id": "bio_abdulrahman",
        "section": "B",
        "category": "topic",
        "display_category": "companions",
        "group_id": "bio_abdulrahman",
        "group_label": "Biography: Hazrat Abdul Rahman bin Auf (RA)",
        "title": "Hazrat Abdul Rahman ibn Awf (RA) — One of the Ten Promised Paradise",
        "arabic": "",
        "lines": [
            "One of the Asharah Mubasharah (Ten Companions promised Paradise); among the earliest converts to Islam.",
            "A highly successful merchant in Makkah; left all his wealth behind for the sake of Islam during the Hijrah.",
            "In Madinah, was paired with Sa'd ibn Rabi (RA) as a brother; declined to accept charity, preferring to earn independently.",
            "Within a short time rebuilt his entire fortune through honest trade — a model of self-reliance and trust in Allah.",
            "Famous for extraordinary generosity: on one occasion donated a caravan of 700 camels loaded with goods for the cause of Islam.",
            "Fought in all major battles alongside the Prophet and was known for his bravery and sound judgement.",
            "Died approximately 32 AH; left behind enormous charitable endowments benefiting the entire Muslim community.",
        ],
    },
    {
        "id": "bio_talha",
        "section": "B",
        "category": "topic",
        "display_category": "companions",
        "group_id": "bio_talha",
        "group_label": "Biography: Hazrat Talha bin Ubaidullah (RA)",
        "title": "Hazrat Talha ibn Ubaydillah (RA) — One of the Ten Promised Paradise",
        "arabic": "",
        "lines": [
            "One of the Asharah Mubasharah (Ten Companions promised Paradise); among the first eight people to accept Islam.",
            "Accepted Islam at the invitation of Abu Bakr (RA) before the Prophet had even begun public preaching.",
            "At the Battle of Uhud, he used his own body as a human shield to protect the Prophet during the fiercest fighting.",
            "His hand was permanently injured — paralysed from deflecting sword blows aimed at the Prophet — earning him undying honour.",
            "The Prophet (pbuh) named him 'Talha al-Khayr' (Talha the Good) and 'Talha al-Fayyad' (Talha the Overflowing) for his generosity.",
            "Known for regularly distributing his wealth among the poor of Madinah — sometimes giving away everything he owned.",
            "Martyred at the Battle of the Camel in 36 AH / 656 CE; buried in Basra.",
        ],
    },

    # ── Wives of the Prophet ─────────────────────────────────────────────────
    {
        "id": "bio_khadijah",
        "section": "B",
        "category": "topic",
        "display_category": "wives",
        "group_id": "bio_khadijah",
        "group_label": "Biography: Hazrat Khadijah (RA)",
        "title": "Hazrat Khadijah bint Khuwaylid (RA) — First Wife",
        "arabic": "",
        "lines": [
            "First and most beloved wife of the Prophet; married him when she was 40 and he was 25 years old (595 CE).",
            "A respected, wealthy, and successful businesswoman in Makkah who had witnessed his honesty firsthand.",
            "First person to accept Islam — she immediately believed and supported the Prophet without hesitation.",
            "When the first revelation came, she comforted him, wrapped him in a blanket, and took him to Waraqah ibn Nawfal for guidance.",
            "Spent her entire personal fortune supporting the Prophet's mission and relieving the suffering of poor Muslims.",
            "Mother of all the Prophet's children except Ibrahim: Zainab, Ruqayyah, Umm Kulthum, and Fatimah (RA).",
            "Died in 619 CE (Year of Grief); her death devastated the Prophet who continued to honour her memory throughout his life.",
        ],
    },
    {
        "id": "bio_sawda",
        "section": "B",
        "category": "topic",
        "display_category": "wives",
        "group_id": "bio_sawda",
        "group_label": "Biography: Hazrat Sawda (RA)",
        "title": "Hazrat Sawda bint Zam'a (RA) — Second Wife",
        "arabic": "",
        "lines": [
            "Second wife of the Prophet, married after the death of Khadijah (RA) in 619 CE to provide a mother's care for his children.",
            "A widow who had accepted Islam in its earliest days and endured hardship and persecution for her faith.",
            "Migrated to Abyssinia with the first group of Muslims to escape Quraysh oppression.",
            "Known for her extraordinary generosity, warmth, cheerful nature, and strong sense of humour.",
            "In an act of remarkable selflessness, she gave her designated day with the Prophet to Aisha (RA) out of love and respect.",
            "Lived a simple, humble life devoted entirely to worship, charity, and service to the Prophet's household.",
            "A model of patience, selflessness, and sincere devotion; she asked only to die as a Muslim in the Prophet's care.",
        ],
    },
    {
        "id": "bio_aisha",
        "section": "B",
        "category": "topic",
        "display_category": "wives",
        "group_id": "bio_aisha",
        "group_label": "Biography: Hazrat Aisha (RA)",
        "title": "Hazrat Aisha bint Abi Bakr (RA) — Scholar of Islam",
        "arabic": "",
        "lines": [
            "Daughter of Abu Bakr (RA); the Prophet called her the most knowledgeable woman in Islamic history.",
            "Gifted with exceptional intelligence, a sharp memory, and a deep understanding of Quranic rulings.",
            "Narrated over 2,200 hadiths — one of the top five hadith narrators among all companions.",
            "Scholars, companions, and later generations came to her to learn about the Prophet's daily life, worship, and rulings.",
            "Her knowledge covered Islamic jurisprudence, Quranic commentary, medicine, poetry, and genealogy.",
            "After the Prophet's death, she taught both men and women for over 40 years, becoming a pillar of Islamic scholarship.",
            "Died 58 AH / 678 CE; buried in Jannat al-Baqi, Madinah — her legacy of knowledge continues to benefit Muslims today.",
        ],
    },
    {
        "id": "bio_hafsa",
        "section": "B",
        "category": "topic",
        "display_category": "wives",
        "group_id": "bio_hafsa",
        "group_label": "Biography: Hazrat Hafsa (RA)",
        "title": "Hazrat Hafsa bint Umar (RA) — Guardian of the Quran",
        "arabic": "",
        "lines": [
            "Daughter of Umar ibn al-Khattab (RA); married the Prophet after her first husband Khunays was martyred at Badr.",
            "One of the very few people of her era who had memorised the entire Quran — a rare achievement for any Muslim.",
            "The official written Mushaf compiled under Abu Bakr (RA) was entrusted to her custody — a reflection of the companions' trust in her piety.",
            "Known for her deep devotion to worship: she spent long nights in prayer and regularly observed voluntary fasts.",
            "The Prophet once divorced her, then took her back at the command of Angel Jibreel — a sign of her high rank.",
            "Played a crucial role in the physical preservation of the Quran for all of humanity.",
            "Died 45 AH; buried in Jannat al-Baqi, Madinah — remembered as a model of knowledge, piety, and service to Islam.",
        ],
    },

    # ── Qur'an & Islamic Law ─────────────────────────────────────────────────
    {
        "id": "primary_sources_law",
        "section": "B",
        "category": "topic",
        "display_category": "quran_law",
        "group_id": "primary_sources_law",
        "group_label": "Primary Sources of Islamic Law",
        "title": "Primary Sources of Islamic Law (Shariah)",
        "arabic": "",
        "lines": [
            "The Quran is the first and most authoritative source of Islamic law — the direct and unaltered word of Allah.",
            "The Sunnah (recorded in Hadith) is the second source — the Prophet's sayings, actions, and silent approvals.",
            "Together, Quran and Sunnah form the foundation of Shariah; no ruling can contradict either of them.",
            "The Quran provides general principles and broad commands; the Sunnah explains, details, and demonstrates their application.",
            "Scholars use the Quran and Sunnah to derive rulings for all aspects of life: worship, family, trade, and governance.",
            "Secondary sources — Ijma (scholarly consensus) and Qiyas (analogy) — are derived from and must align with the primary sources.",
            "The science of deriving rulings from these sources is called Fiqh (Islamic jurisprudence), practised by qualified scholars.",
        ],
    },
    {
        "id": "ijma",
        "section": "B",
        "category": "topic",
        "display_category": "quran_law",
        "group_id": "ijma",
        "group_label": "Ijma (Scholarly Consensus)",
        "title": "Ijma — The Third Source of Islamic Law",
        "arabic": "",
        "lines": [
            "Ijma means the consensus or unanimous agreement of qualified Muslim scholars on a religious ruling.",
            "It is the third source of Islamic law, used after the Quran and Sunnah fail to provide an explicit ruling.",
            "Its authority is based on the hadith: 'My Ummah will never agree upon an error.' (Ibn Majah)",
            "The strongest form is Ijma of the Companions (Sahabah) — their consensus carries the greatest weight in Islamic law.",
            "Other forms include Ijma of scholars of a particular era or recognised school of jurisprudence.",
            "Ijma allows Islamic law to address new situations not explicitly covered in the Quran or Sunnah.",
            "Decisions reached through Ijma become binding on the Muslim community and cannot be overturned by individual opinions.",
        ],
    },
]

# ── New Quiz Questions ───────────────────────────────────────────────────────
NEW_SECTION_B_QUESTIONS = [

    # ── First Revelation ─────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"The First Revelation",
     "question":"The Prophet Muhammad (pbuh) received the first revelation in the Cave of _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Hira","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"The First Revelation",
     "question":"The Prophet was _______ years old when he received the first revelation.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"40","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"The First Revelation",
     "question":"The first word revealed to the Prophet by Angel Jibreel was '_______'.","arabic_text":"اِقْرَأْ","transliteration":"Iqra","english_translation":"Read/Recite","model_answer":"Iqra","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"The First Revelation",
     "question":"After the first revelation, Khadijah (RA) took the Prophet to her cousin _______ ibn Nawfal for guidance.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Waraqah","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"The First Revelation",
     "question":"The first verses revealed belonged to Surah _______.","arabic_text":"العلق","transliteration":"Al-Alaq","english_translation":"The Clot","model_answer":"Al-Alaq","marks":1},
    {"section":"B","type":"short_answer","topic_number":1,"topic_title":"The First Revelation",
     "question":"Describe the circumstances of the first revelation received by the Prophet (pbuh). [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"In 610 CE the Prophet (pbuh) was meditating in Cave Hira during Ramadan. Angel Jibreel appeared and commanded 'Iqra!' three times; each time the Prophet replied he could not read. On the third time the first five verses of Surah Al-Alaq were revealed. The Prophet returned home trembling; Khadijah (RA) comforted him and took him to Waraqah ibn Nawfal who confirmed it was prophethood. This marked the beginning of the 23-year revelation of the Quran.","marks":4},

    # ── Early Preaching ───────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Early Preaching",
     "question":"For the first _______ years after the first revelation, the Prophet preached Islam secretly.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"three","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Early Preaching",
     "question":"The secret meeting place of early Muslims in Makkah was the house of _______ ibn Abi al-Arqam.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Arqam","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Early Preaching",
     "question":"The Prophet gathered the Quraysh on Mount _______ to publicly proclaim Islam.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Safa","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Early Preaching",
     "question":"The first freed slave to accept Islam was _______ ibn Harithah.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Zayd","marks":1},
    {"section":"B","type":"short_answer","topic_number":1,"topic_title":"Early Preaching",
     "question":"Explain the transition from secret to public preaching and the Quraysh's reaction. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"For the first three years the Prophet preached secretly, holding meetings at Dar al-Arqam. First converts were Khadijah, Ali, Abu Bakr, and Zayd (RA). When Allah commanded 'warn your nearest relatives' (26:214), the Prophet gathered the Quraysh on Mount Safa and publicly proclaimed Islam. The Quraysh leaders rejected him and began persecuting Muslims because Islam threatened their idols, trade, and social status. His uncle Abu Lahab was among the most hostile opponents.","marks":4},

    # ── Caves ────────────────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Prophet's Experience in Caves",
     "question":"Cave Hira is situated on a mountain near Makkah called Jabal al-_______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Nour","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Prophet's Experience in Caves",
     "question":"During the Hijrah, the Prophet and Abu Bakr (RA) hid in Cave _______ for three days.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Thawr","marks":1},
    {"section":"B","type":"short_answer","topic_number":1,"topic_title":"Prophet's Experience in Caves",
     "question":"Explain the significance of Cave Hira and Cave Thawr in the life of the Prophet (pbuh). [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"Cave Hira on Jabal al-Nour was where the Prophet regularly retreated for prayer and contemplation before prophethood. It was here in 610 CE that Angel Jibreel revealed the first verses of Surah Al-Alaq, marking the beginning of prophethood. Cave Thawr is located south of Makkah where the Prophet and Abu Bakr hid for three days in 622 CE while escaping the Quraysh assassination plot during the Hijrah. Allah miraculously protected them — Hira represents the beginning of prophethood; Thawr the beginning of the Islamic state.","marks":4},

    # ── Isra & Mi'raj ────────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Isra and Mi'raj",
     "question":"During the Isra, the Prophet travelled from Masjid al-Haram to Masjid al-_______ in Jerusalem.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Aqsa","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Isra and Mi'raj",
     "question":"The Prophet travelled on a heavenly creature called the _______ during the Isra.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Buraq","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Isra and Mi'raj",
     "question":"During Mi'raj, Allah initially prescribed _______ daily prayers before reducing them to five.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"fifty","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Isra and Mi'raj",
     "question":"The highest point the Prophet reached in the heavens is called Sidrat al-_______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Muntaha","marks":1},
    {"section":"B","type":"short_answer","topic_number":1,"topic_title":"Isra and Mi'raj",
     "question":"Describe the Isra and Mi'raj and explain their significance for the Muslim community. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"The Isra was the miraculous night journey from Makkah to Jerusalem on the Buraq, where the Prophet led all prophets in prayer. The Mi'raj was the ascension through the seven heavens where he met prophets including Adam, Musa, and Ibrahim. He reached Sidrat al-Muntaha and received the command for five daily prayers (reduced from fifty on Musa's advice). The significance: it honoured the Prophet after the Year of Grief, established Salah as an obligation, connected Islam to previous prophets, and demonstrated Allah's power and support.","marks":4},

    # ── Visit to Ta'if ───────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Visit to Ta'if",
     "question":"The Prophet's companion during the visit to Ta'if was _______ ibn Harithah (RA).","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Zayd","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Visit to Ta'if",
     "question":"The tribe whose leaders the Prophet met in Ta'if was Banu _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Thaqif","marks":1},
    {"section":"B","type":"short_answer","topic_number":1,"topic_title":"Visit to Ta'if",
     "question":"Describe the Prophet's visit to Ta'if and what it reveals about his character. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"After the Year of Grief (619 CE), the Prophet traveled to Ta'if with Zayd ibn Harithah seeking support. The three leaders of Banu Thaqif rejected and mocked him, setting slaves and children to stone them out of the city. Both were injured and bleeding. Despite being offered revenge by an angel, the Prophet refused and made a dua praying for their future guidance. This reveals his extraordinary patience, mercy, forgiveness, and complete trust in Allah — he prioritised the guidance of people over personal revenge.","marks":4},

    # ── Causes of Hijrah ─────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Causes of Hijrah",
     "question":"The year in which both Khadijah (RA) and Abu Talib died is known as the Year of _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Grief","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Causes of Hijrah",
     "question":"The people of _______ (later called Madinah) pledged to protect the Prophet in the Pledges of Aqabah.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Yathrib","marks":1},
    {"section":"B","type":"short_answer","topic_number":1,"topic_title":"Causes of Hijrah",
     "question":"Explain the main causes that led the Prophet (pbuh) to migrate from Makkah to Madinah. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"The main causes were: continuous Quraysh persecution including torture, economic boycott of Banu Hashim (616–619 CE), and social isolation. The Year of Grief (619 CE) saw the deaths of Khadijah (RA) and Abu Talib, leaving the Prophet without emotional and tribal protection. The mission to Ta'if failed completely. Most importantly, the Pledges of Aqabah (621–622 CE) provided a willing community in Yathrib ready to receive and protect him. The Quraysh then plotted to assassinate him, and Allah commanded the Hijrah.","marks":4},

    # ── Events of Hijrah ─────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Events of Hijrah",
     "question":"Hazrat _______ (RA) slept in the Prophet's bed to deceive the Quraysh assassins on the night of Hijrah.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Ali","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Events of Hijrah",
     "question":"The first mosque built by the Prophet upon arriving near Madinah was Masjid _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Quba","marks":1},
    {"section":"B","type":"fill_blank","topic_number":1,"topic_title":"Events of Hijrah",
     "question":"The guide who led the Prophet and Abu Bakr safely to Madinah was Abdullah ibn _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Urayqit","marks":1},
    {"section":"B","type":"short_answer","topic_number":1,"topic_title":"Events of Hijrah",
     "question":"Describe the main events that took place during the Hijrah journey. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"On the night of Hijrah, Ali (RA) slept in the Prophet's bed while he and Abu Bakr quietly escaped. They hid in Cave Thawr for three days; Asma (RA) brought food and news. They then traveled south via an unfamiliar route guided by Abdullah ibn Urayqit. Suraqah ibn Malik pursued them for a reward but his horse sank miraculously and he turned back. They arrived at Quba, built the first mosque, then entered Madinah on 12 Rabi al-Awwal 1 AH. The Ansar welcomed them joyfully. This Hijrah marks the start of the Islamic calendar.","marks":4},

    # ── Biography: Abu Bakr ───────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Abu Bakr (RA)",
     "question":"Hazrat Abu Bakr (RA) was given the title '_______ ' for immediately believing in the Isra & Mi'raj.","arabic_text":"الصِّدِّيق","transliteration":"As-Siddiq","english_translation":"The Confirmer of Truth","model_answer":"As-Siddiq","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Abu Bakr (RA)",
     "question":"Abu Bakr (RA) used his wealth to free the Muslim slave _______ (RA) from his tormentor.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Bilal","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Abu Bakr (RA)",
     "question":"Abu Bakr (RA) was the _______ Caliph of Islam after the Prophet's death.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"First","marks":1},
    {"section":"B","type":"short_answer","topic_number":3,"topic_title":"Biography: Hazrat Abu Bakr (RA)",
     "question":"Describe the contribution of Hazrat Abu Bakr (RA) to the early Muslim community. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"Abu Bakr (RA) was the first adult male convert and the Prophet's closest companion. He spent his wealth freeing tortured Muslims including Bilal (RA). He accompanied the Prophet during the Hijrah and hid with him in Cave Thawr. As First Caliph he united the Muslims after the Prophet's death, crushed the apostasy (Riddah) movements, and initiated the first written compilation of the Quran. He died after only two years as Caliph but left a lasting legacy of loyalty, sacrifice, and leadership.","marks":4},

    # ── Biography: Usman ─────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Usman (RA)",
     "question":"Hazrat Usman (RA) was titled 'Dhul-Nurayn' because he married _______ daughters of the Prophet.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"two","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Usman (RA)",
     "question":"Usman (RA) was the _______ Caliph of Islam.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Third","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Usman (RA)",
     "question":"Usman (RA)'s greatest contribution was standardising the Quran into one official written copy called the _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Mushaf","marks":1},
    {"section":"B","type":"short_answer","topic_number":3,"topic_title":"Biography: Hazrat Usman (RA)",
     "question":"Explain why the standardisation of the Quran under Uthman (RA) was important for the Muslim Ummah. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"As Islam spread to many regions, different dialect versions of the Quran caused disagreements over recitation. Uthman (RA) formed a committee led by Zayd ibn Thabit to produce one authoritative Mushaf in the Qurayshi dialect. Official copies were sent to all major cities and other versions burned to prevent division. This ensured the Quran remained unified and unchanged throughout the Muslim world. The Uthmanic Mushaf is the Quran Muslims use today — a lasting contribution that preserved Islamic unity.","marks":4},

    # ── Biography: Ali ───────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Ali (RA)",
     "question":"Hazrat Ali (RA) was the _______ Caliph of Islam.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Fourth","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Ali (RA)",
     "question":"Hazrat Ali (RA) was known as 'Asadullah' meaning _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Lion of Allah","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Ali (RA)",
     "question":"Hazrat Ali (RA) married _______ (RA), the youngest daughter of the Prophet.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Fatimah","marks":1},

    # ── Biographies: Khadijah ─────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Khadijah (RA)",
     "question":"Khadijah (RA) was _______ years old when she married the Prophet.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"40","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Khadijah (RA)",
     "question":"Khadijah (RA) was the _______ person to accept Islam.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"first","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Khadijah (RA)",
     "question":"Khadijah (RA) died in _______ CE, a year known as the Year of Grief.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"619","marks":1},
    {"section":"B","type":"short_answer","topic_number":3,"topic_title":"Biography: Hazrat Khadijah (RA)",
     "question":"Describe the role of Hazrat Khadijah (RA) in supporting the Prophet (pbuh) and spreading Islam. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"Khadijah (RA) was the first person to accept Islam and provided the Prophet with immediate emotional, financial, and moral support. When the first revelation came, she comforted him in his fear and took him to Waraqah ibn Nawfal for confirmation. She spent her entire fortune supporting early Muslims and the Prophet's mission. She was the mother of all his children except Ibrahim. Her death in 619 CE was a devastating loss for the Prophet. He honoured her memory throughout his life, sending gifts to her friends and speaking of her with deep love.","marks":4},

    # ── Biography: Aisha ─────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Aisha (RA)",
     "question":"Hazrat Aisha (RA) narrated over _______ hadiths, making her one of the greatest narrators of hadith.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"2000","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Aisha (RA)",
     "question":"Hazrat Aisha (RA) was the daughter of _______ (RA), the First Caliph of Islam.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Abu Bakr","marks":1},
    {"section":"B","type":"short_answer","topic_number":3,"topic_title":"Biography: Hazrat Aisha (RA)",
     "question":"Explain the contribution of Hazrat Aisha (RA) to Islamic knowledge and scholarship. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"Hazrat Aisha (RA) was among the most learned companions, narrating over 2,200 hadiths. Her sharp memory and intelligence meant companions visited her to learn about the Prophet's daily life, worship, and rulings on family matters. Her knowledge extended to Islamic jurisprudence, Quranic commentary, medicine, and poetry. She taught men and women for over 40 years after the Prophet's death, becoming a cornerstone of Islamic scholarship. The Prophet himself declared: 'Take half of your religion from this red-cheeked woman.'","marks":4},

    # ── Biography: Hafsa ─────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Hafsa (RA)",
     "question":"Hazrat Hafsa (RA) was the daughter of _______ ibn al-Khattab (RA).","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Umar","marks":1},
    {"section":"B","type":"fill_blank","topic_number":3,"topic_title":"Biography: Hazrat Hafsa (RA)",
     "question":"The first official written Mushaf of the Quran was kept in the custody of Hazrat _______ (RA).","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Hafsa","marks":1},

    # ── Primary Sources of Law ────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":6,"topic_title":"Primary Sources of Islamic Law",
     "question":"The first and most authoritative source of Islamic law is the _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Quran","marks":1},
    {"section":"B","type":"fill_blank","topic_number":6,"topic_title":"Primary Sources of Islamic Law",
     "question":"The second primary source of Islamic law, recording the Prophet's sayings and actions, is the _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Sunnah","marks":1},
    {"section":"B","type":"fill_blank","topic_number":6,"topic_title":"Primary Sources of Islamic Law",
     "question":"The science of deriving Islamic rulings from the Quran and Sunnah is called _______.","arabic_text":"الفِقْه","transliteration":"Fiqh","english_translation":"Islamic Jurisprudence","model_answer":"Fiqh","marks":1},
    {"section":"B","type":"short_answer","topic_number":6,"topic_title":"Primary Sources of Islamic Law",
     "question":"Explain the relationship between the Quran and Sunnah as the primary sources of Islamic law. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"The Quran is the direct word of Allah and provides the general principles and broad commands of Islamic law. The Sunnah, recorded in Hadith, is the Prophet's sayings, actions, and approvals, which explain and apply Quranic principles in practical situations. Together they form the foundation of Shariah — no ruling can contradict either. Where the Quran provides a general command (e.g. pray), the Sunnah provides the details (how, when, and how many times). Secondary sources like Ijma and Qiyas are only valid when aligned with these two primary sources.","marks":4},

    # ── Ijma ─────────────────────────────────────────────────────────────────
    {"section":"B","type":"fill_blank","topic_number":6,"topic_title":"Ijma",
     "question":"Ijma refers to the _______ of qualified Muslim scholars on a religious ruling.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"consensus","marks":1},
    {"section":"B","type":"fill_blank","topic_number":6,"topic_title":"Ijma",
     "question":"Ijma is the _______ source of Islamic law after the Quran and Sunnah.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"third","marks":1},
    {"section":"B","type":"short_answer","topic_number":6,"topic_title":"Ijma",
     "question":"Define Ijma and explain its importance as a source of Islamic law. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"Ijma is the unanimous consensus of qualified Muslim scholars on a religious ruling not explicitly stated in the Quran or Sunnah. Its authority is derived from the hadith 'My Ummah will never agree upon an error.' The strongest form is the Ijma of the Companions (Sahabah). Ijma allows Islamic law to remain relevant and address new situations that arise in every generation. Decisions reached through Ijma are binding on the Muslim community. It represents the collective wisdom of Islamic scholarship and prevents division over new religious questions.","marks":4},
]

NEW_SECTION_C_QUESTIONS = [

    # ── Battle of Trench ──────────────────────────────────────────────────────
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Battle of the Trench",
     "question":"The idea of digging a trench around Madinah was suggested by _______ al-Farsi (RA).","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Salman","marks":1},
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Battle of the Trench",
     "question":"The Battle of the Trench took place in _______ AH (627 CE).","arabic_text":"","transliteration":"","english_translation":"","model_answer":"5","marks":1},
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Battle of the Trench",
     "question":"The confederacy that attacked Madinah during the Battle of the Trench numbered approximately _______ soldiers.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"10,000","marks":1},
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Battle of the Trench",
     "question":"The tribe that betrayed the Muslims by breaking their treaty during the siege was Banu _______.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Qurayza","marks":1},
    {"section":"C","type":"short_answer","topic_number":5,"topic_title":"Battle of the Trench",
     "question":"Describe the Battle of the Trench and explain its outcome for the Muslim community. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"In 5 AH, the Quraysh formed a confederacy of approximately 10,000 soldiers from multiple tribes to destroy Madinah. Salman al-Farsi (RA) suggested digging a trench on the exposed northern side — a Persian defensive strategy. The Muslims dug it in six days; the Prophet worked alongside them. The confederacy could not cross the trench and laid siege for nearly a month. Harsh weather, food shortages, and internal divisions weakened them and they retreated. The Quraysh threat to Madinah was permanently ended, showing the importance of strategy, unity, and patience.","marks":4},

    # ── Treaty of Hudaibiya ───────────────────────────────────────────────────
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Treaty of Hudaibiya",
     "question":"The Treaty of Hudaibiya was signed between the Prophet (pbuh) and the Quraysh in _______ AH.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"6","marks":1},
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Treaty of Hudaibiya",
     "question":"The Treaty of Hudaibiya established a _______ -year peace between Muslims and Quraysh.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"10","marks":1},
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Treaty of Hudaibiya",
     "question":"Allah referred to the Treaty of Hudaibiya as a 'clear _______' in Surah Al-Fath.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"victory","marks":1},
    {"section":"C","type":"short_answer","topic_number":5,"topic_title":"Treaty of Hudaibiya",
     "question":"Why is the Treaty of Hudaibiya considered a victory for the Muslims despite its unfavourable terms? [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"Although the terms appeared to favour the Quraysh — Muslims had to return without performing Umrah and return any Muslim fugitives — the treaty proved to be a strategic victory. It ended hostilities for 10 years, giving Islam space to spread rapidly through peaceful preaching. More people accepted Islam during this peace than in all previous years combined. The Prophet's acceptance of the terms showed wisdom and trust in Allah. Allah revealed: 'Indeed We have granted you a clear victory' (48:1). The Quraysh breaking the treaty two years later led directly to the Conquest of Makkah.","marks":4},

    # ── Charter of Madinah ────────────────────────────────────────────────────
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Charter of Madinah",
     "question":"The Charter of Madinah is considered the first written _______ in history.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"constitution","marks":1},
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Charter of Madinah",
     "question":"The Charter of Madinah declared all Muslims as one united _______.","arabic_text":"أُمَّة","transliteration":"Ummah","english_translation":"Community/Nation","model_answer":"Ummah","marks":1},
    {"section":"C","type":"short_answer","topic_number":5,"topic_title":"Charter of Madinah",
     "question":"Describe the key features of the Charter of Madinah and its importance. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"The Charter of Madinah was written by the Prophet (pbuh) in 622 CE shortly after the Hijrah — considered history's first written constitution. It declared all Muslims as one Ummah and established mutual rights and responsibilities. Non-Muslim tribes — Jews, Christians, and others — were granted full religious freedom and equal protection under the law. All citizens were required to defend Madinah jointly. Disputes were to be referred to the Prophet. It established justice, equality, and cooperation among all citizens regardless of religion, demonstrating the Prophet's remarkable wisdom as both religious and political leader.","marks":4},

    # ── Events After Hijrah ───────────────────────────────────────────────────
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Events After Migration to Madinah",
     "question":"The brotherhood established between Muhajirun and Ansar after the Hijrah was called _______.","arabic_text":"المُؤَاخَاة","transliteration":"Mu'akhat","english_translation":"Brotherhood","model_answer":"Mu'akhat","marks":1},
    {"section":"C","type":"fill_blank","topic_number":5,"topic_title":"Events After Migration to Madinah",
     "question":"The direction of prayer (Qiblah) was changed from Jerusalem to _______ in 2 AH.","arabic_text":"","transliteration":"","english_translation":"","model_answer":"Makkah","marks":1},
    {"section":"C","type":"short_answer","topic_number":5,"topic_title":"Events After Migration to Madinah",
     "question":"Describe the steps taken by the Prophet (pbuh) to establish the Muslim community in Madinah. [4 marks]","arabic_text":"","transliteration":"","english_translation":"",
     "model_answer":"Upon arriving in Madinah, the Prophet first built Masjid al-Nabawi as the centre of the new community. He established Mu'akhat (brotherhood) between Muhajirun (migrants) and Ansar (helpers), with each Ansar sharing their wealth and home. The Charter of Madinah united all tribes — Muslim, Jewish, and others — under one constitution ensuring justice and mutual defence. The Adhan was introduced for the call to prayer and the Qiblah was changed to Makkah. These steps built a strong, unified Islamic community and transformed Madinah into the world's first Islamic state.","marks":4},
]


def main():
    # ── 1. Update memorize_content.json ──────────────────────────────────────
    mem_path = os.path.join(BASE, "memorize_content.json")
    with open(mem_path, "r", encoding="utf-8") as f:
        mem_data = json.load(f)

    # Add display_category to existing cards
    for card in mem_data["cards"]:
        gid = card.get("group_id", "")
        cat = card.get("category", "")
        if cat == "quran":
            card["display_category"] = "quran_surahs"
        elif cat == "hadith":
            card["display_category"] = "ahadith"
        else:
            card["display_category"] = GROUP_CAT.get(gid, "other")

    # Append new cards (avoid duplicates by group_id)
    existing_ids = {c["group_id"] for c in mem_data["cards"]}
    added = 0
    for card in NEW_CARDS:
        if card["group_id"] not in existing_ids:
            mem_data["cards"].append(card)
            existing_ids.add(card["group_id"])
            added += 1

    with open(mem_path, "w", encoding="utf-8") as f:
        json.dump(mem_data, f, ensure_ascii=False, indent=2)
    print(f"memorize_content.json: {added} new cards added, display_category set on all cards.")

    # ── 2. Update Section B questions ────────────────────────────────────────
    sb_path = os.path.join(BASE, "question_bank", "section_b", "sample_extended.json")
    with open(sb_path, "r", encoding="utf-8") as f:
        sb_data = json.load(f)

    existing_qs = {q["question"] for q in sb_data}
    added_b = 0
    for q in NEW_SECTION_B_QUESTIONS:
        if q["question"] not in existing_qs:
            sb_data.append(q)
            existing_qs.add(q["question"])
            added_b += 1

    with open(sb_path, "w", encoding="utf-8") as f:
        json.dump(sb_data, f, ensure_ascii=False, indent=2)
    print(f"section_b/sample_extended.json: {added_b} new questions added.")

    # ── 3. Update Section C questions ────────────────────────────────────────
    sc_path = os.path.join(BASE, "question_bank", "section_c", "sample_extended.json")
    with open(sc_path, "r", encoding="utf-8") as f:
        sc_data = json.load(f)

    existing_qs = {q["question"] for q in sc_data}
    added_c = 0
    for q in NEW_SECTION_C_QUESTIONS:
        if q["question"] not in existing_qs:
            sc_data.append(q)
            existing_qs.add(q["question"])
            added_c += 1

    with open(sc_path, "w", encoding="utf-8") as f:
        json.dump(sc_data, f, ensure_ascii=False, indent=2)
    print(f"section_c/sample_extended.json: {added_c} new questions added.")


if __name__ == "__main__":
    main()
