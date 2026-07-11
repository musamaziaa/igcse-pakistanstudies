import json

path = '/home/zia/igcse_pakstudies/backend/data/pak_studies/memorize_content.json'
with open(path, 'r') as f:
    data = json.load(f)

# Remove the fake tier cards
data['cards'] = [c for c in data['cards'] if not c['id'].startswith('tier')]

# Map existing group_ids to tiers
tier_map = {
    'constitution': 'Tier 1: Critical',
    'pakistan_movement': 'Tier 1: Critical',
    'foreign_policy': 'Tier 2: Most Important',
    'economy': 'Tier 2: Most Important',
    'current_perspectives': 'Tier 3: Nice to Learn'
}

for c in data['cards']:
    c['tier_label'] = tier_map.get(c['group_id'], 'Other Topics')

with open(path, 'w') as f:
    json.dump(data, f, indent=2)
print("Updated JSON structure!")
