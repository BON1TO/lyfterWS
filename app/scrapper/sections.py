def split_into_sections(content: dict):
    sections = []

    sections.append({
        "id": "headings",
        "type": "content",
        "label": "Headings",
        "items": content.get("headings", [])
    })

    sections.append({
        "id": "paragraphs",
        "type": "content",
        "label": "Paragraphs",
        "items": content.get("paragraphs", [])
    })

    sections.append({
        "id": "links",
        "type": "content",
        "label": "Links",
        "items": content.get("links", [])
    })

    sections.append({
        "id": "images",
        "type": "content",
        "label": "Images",
        "items": content.get("images", [])
    })

    return sections
