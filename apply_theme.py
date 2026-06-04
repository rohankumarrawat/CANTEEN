import re

with open('app_enhanced.py', 'r') as f:
    code = f.read()

# Replace Palette definitions
replacements = {
    'SAFFRON   = "#FF9933"': 'SAFFRON   = "#C8960C"  # Army Gold',
    'IND_GREEN = "#138808"': 'IND_GREEN = "#6B7040"  # Army Med',
    'GOLD      = "#C9A84C"': 'GOLD      = "#C8960C"  # Army Gold',
    'GOLD_LT   = "#EDD97A"': 'GOLD_LT   = "#E8D595"  # Lighter Gold',
    'ARMY_BG   = "#1F3320"': 'ARMY_BG   = "#4B5320"  # Army Olive',
    'ARMY_HVR  = "#2C4A2A"': 'ARMY_HVR  = "#6B7040"  # Army Med',
    'ARMY_SEP  = "#2E4830"': 'ARMY_SEP  = "#3D4416"  # Dark Olive',
    'LIGHT  = "#F1F5F1"': 'LIGHT  = "#F5F0E8"  # Army Light / Warm off-white',
    'BORDER = "#DDE8DD"': 'BORDER = "#E8E4DA"  # Slate',
    'STRIPE = "#F5FAF5"': 'STRIPE = "#EDE9DE"  # Table Alt',
    
    # Change dynamic bg colours inside _show_login
    'bg="#1F3320"': 'bg="#4B5320"',
    'fill="#253D27"': 'fill="#454D1B"',
    'fill="#192A1C"': 'fill="#3D4416"',
    
    # Optional: we can change the Ashoka chakra colour
    'FGOLD = "#6B5A1E"': 'FGOLD = "#C8960C"',
}

for old, new in replacements.items():
    code = code.replace(old, new)

# Change hardcoded table backgrounds or text if they use STRIPE or ARMY_BG improperly
# Specifically if there's an explicit table head color, we might want Dark Olive:
# (If applicable in the code)

with open('app.py', 'w') as f:
    f.write(code)

print("Theme applied successfully to app.py")
