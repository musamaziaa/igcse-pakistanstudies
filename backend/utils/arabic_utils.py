import streamlit.components.v1 as components


def render_arabic(arabic_text: str, translation: str = "", transliteration: str = "", height: int = 130) -> None:
    """Render Arabic text RTL with transliteration and translation."""
    trans_html = f"<div style='font-style:italic;color:#666;font-size:0.9em;margin-top:4px;'>{transliteration}</div>" if transliteration else ""
    tran_html = f"<div style='color:#333;font-size:0.95em;margin-top:4px;'>{translation}</div>" if translation else ""
    html = f"""
    <link href='https://fonts.googleapis.com/css2?family=Amiri&display=swap' rel='stylesheet'>
    <div style='
        direction:rtl;
        font-family:Amiri,serif;
        font-size:1.5em;
        color:#1F3864;
        background:#F7F9FC;
        padding:16px;
        border-radius:6px;
        border-right:4px solid #2E5FA3;
        margin-bottom:8px;
        text-align:right;
    '>{arabic_text}</div>
    {trans_html}
    {tran_html}
    """
    components.html(html, height=height)


def arabic_badge(text: str) -> str:
    """Return inline HTML for a small Arabic badge (for use in markdown)."""
    return f"<span dir='rtl' style='font-family:Amiri,serif;font-size:1.2em;'>{text}</span>"
