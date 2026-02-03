import re
import json

def on_page_markdown(markdown, page, config, files):
    """
    Scrape '!!! question' blocks and store structured data in page metadata
    """
    pattern = r'!!!\s+question\s+"([^"]+)"\n((?:\s{4}.*\n?)+)'
    matches = re.findall(pattern, markdown)
    
    if not matches:
        return markdown

    questions = []
    for q, a in matches:
        raw_text = " ".join([line.strip() for line in a.splitlines()])

        # 1. Remove images
        text = re.sub(r'!\[.*?\]\(.*?\)', '', raw_text)
        # 2. Remove bold and italic (***, **, *)
        text = re.sub(r'(\*{1,3}|_{1,3})(.*?)\1', r'\2', text)
        # 3. Remove links but keep the label [label](url) -> label
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        # 4. Collapse whitespace
        clean_answer = re.sub(r'\s+', ' ', text).strip()

        questions.append({
            "@type": "Question",
            "name": q,
            "acceptedAnswer": {
                "@type": "Answer",
                "text": clean_answer
            }
        })

    if questions:
        structured_data = {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": questions
        }
        page.meta['faq_json_ld'] = json.dumps(structured_data, ensure_ascii=False)

    return markdown

def on_post_page(output, page, config):
    """
    Inject the JSON-LD script into the <head> of the rendered HTML.
    """
    if 'faq_json_ld' in page.meta:
        script = f'<script type="application/ld+json">\n{page.meta["faq_json_ld"]}\n</script>'
        output = output.replace('</head>', f'{script}\n</head>')
    return output
