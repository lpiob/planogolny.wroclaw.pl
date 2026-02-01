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
        text_no_images = re.sub(r'!\[.*?\]\(.*?\)', '', raw_text)
        clean_answer = re.sub(r'\s+', ' ', text_no_images).strip()
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
        page.meta['faq_json_ld'] = json.dumps(structured_data)

    return markdown

def on_post_page(output, page, config):
    """
    Inject the JSON-LD script into the <head> of the rendered HTML.
    """
    if 'faq_json_ld' in page.meta:
        script = f'<script type="application/ld+json">\n{page.meta["faq_json_ld"]}\n</script>'
        output = output.replace('</head>', f'{script}\n</head>')
    return output
