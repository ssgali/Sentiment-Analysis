from typing import Dict

def highlight_text(text: str, color: str) -> str:
    """
    Highlight text with a given color.
    
    Args:
        text (str): Text to highlight
        color (str): Color for highlighting
    
    Returns:
        str: Highlighted HTML text
    """
    return f'<span style="color: {color}; font-weight: bold;">{text}</span>' if text else ""

def render_review(review: Dict):
    """
    Render a single review with highlighted text.
    
    Args:
        review (Dict): Review dictionary
    
    Returns:
        str: HTML representation of the review
    """

    content = review["Content"]
    
    # Highlight Food-related text
    if review["Food"]:
        content = content.replace(review["Food"], highlight_text(review["Food"], "green"))
    
    # Highlight Service-related text
    if review["Service"]:
        content = content.replace(review["Service"], highlight_text(review["Service"], "blue"))
    
    # Highlight Other text
    if review["Other"]:
        content = content.replace(review["Other"], highlight_text(review["Other"], "red"))
    
    return f'''
    <div style="
        margin-bottom: 20px; 
        padding: 15px; 
        border: 1px solid #444; 
        border-radius: 8px; 
        background-color: #2c2c2c; 
        color: #f0f0f0;
    ">
        <h3 style="margin-bottom: 10px; color: #ffffff;">{review["Name"]} <small style="color: #aaa;">({review["Date"]})</small></h3>
        <p style="margin-bottom: 10px; color: #e0e0e0;">
            <strong>Ratings:</strong>
            <span style="margin-left: 10px;">
                Overall: {review["Rating"]["Overall"]} | 
                Food: {review["Rating"]["Food"]} | 
                Service: {review["Rating"]["Service"]} | 
                Ambience: {review["Rating"]["Ambience"]}
            </span>
        </p>
        <p style="color: #d0d0d0;">{content}</p>
    </div>
    '''