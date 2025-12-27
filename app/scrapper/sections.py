def split_into_sections(content: dict, source_url: str):
    sections = []

    # Headings section
    if content.get("headings"):
        sections.append({
            "id": "section-headings",
            "type": "section",
            "label": "Headings",
            "sourceUrl": source_url,
            "content": {
                "headings": [h["text"] for h in content["headings"]],
                "text": "",
                "links": [],
                "images": [],
                "lists": [],
                "tables": []
            },
            "rawHtml": "<section>Headings extracted</section>",
            "truncated": True
        })

    # Paragraphs section
    if content.get("paragraphs"):
        sections.append({
            "id": "section-text",
            "type": "section",
            "label": "Main Content",
            "sourceUrl": source_url,
            "content": {
                "headings": [],
                "text": " ".join(content["paragraphs"]),
                "links": [],
                "images": [],
                "lists": [],
                "tables": []
            },
            "rawHtml": "<section>Main text extracted</section>",
            "truncated": True
        })

    # Links section
    if content.get("links"):
        sections.append({
            "id": "section-links",
            "type": "list",
            "label": "Links",
            "sourceUrl": source_url,
            "content": {
                "headings": [],
                "text": "",
                "links": content["links"],
                "images": [],
                "lists": [],
                "tables": []
            },
            "rawHtml": "<section>Links extracted</section>",
            "truncated": True
        })

    # Images section
    if content.get("images"):
        sections.append({
            "id": "section-images",
            "type": "grid",
            "label": "Images",
            "sourceUrl": source_url,
            "content": {
                "headings": [],
                "text": "",
                "links": [],
                "images": content["images"],
                "lists": [],
                "tables": []
            },
            "rawHtml": "<section>Images extracted</section>",
            "truncated": True
        })

    return sections
