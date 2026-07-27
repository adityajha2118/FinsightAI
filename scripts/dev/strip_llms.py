import json
import re

def strip_llms():
    path = 'notebooks/01_data_understanding/11_complaint_sentiment.ipynb'
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

    # 1. Update the top markdown cell to remove LLM text
    if nb['cells'][0]['cell_type'] == 'markdown':
        nb['cells'][0]['source'] = [
            "# 11 — Complaint Sentiment & NLP Pipeline\n",
            "Processing 1,000 narratives via VADER Sentiment Analysis & Rules. \n"
        ]

    # 2. Re-write the code cell that defines LLMs
    # It is usually cell index 2 (the one after the imports)
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])
            if 'LLM_PROVIDER' in source or 'local_fallback_summary' in source:
                cell['source'] = [
                    "# ── VADER NLP Setup ──\n",
                    "from nltk.sentiment.vader import SentimentIntensityAnalyzer\n",
                    "import re\n",
                    "sia = SentimentIntensityAnalyzer()\n",
                    "\n",
                    "def nlp_summary(text):\n",
                    "    sentences = re.split(r'(?<=[.!?]) +', str(text))\n",
                    "    return sentences[0][:150] if sentences else str(text)[:150]\n",
                    "\n",
                    "def nlp_category(text, rule_cat):\n",
                    "    if rule_cat != 'Other': return rule_cat\n",
                    "    text_lower = str(text).lower()\n",
                    "    if any(k in text_lower for k in ['fee', 'interest', 'rate', 'payment']): return 'Billing'\n",
                    "    elif any(k in text_lower for k in ['unauthorized', 'scam', 'fraud']): return 'Fraud'\n",
                    "    elif any(k in text_lower for k in ['declined', 'card', 'block']): return 'Card Declined'\n",
                    "    elif any(k in text_lower for k in ['reward', 'point', 'bonus']): return 'Rewards'\n",
                    "    elif any(k in text_lower for k in ['agent', 'service', 'rude', 'rep']): return 'Customer Service'\n",
                    "    return 'Service Delay'\n",
                    "\n",
                    "def nlp_emotion(text):\n",
                    "    text_lower = str(text).lower()\n",
                    "    if any(w in text_lower for w in ['attorney', 'lawyer', 'sue', 'legal', 'cfpb', 'court', 'violation']): return 'Legal Threat'\n",
                    "    scores = sia.polarity_scores(str(text))\n",
                    "    if scores['compound'] <= -0.5: return 'Anger'\n",
                    "    elif scores['compound'] <= -0.1: return 'Frustration'\n",
                    "    return 'Neutral'\n"
                ]
            
            if 'get_llm_response' in source and 'df.iterrows()' in source:
                # The execution loop cell
                cell['source'] = [
                    "import time\n",
                    "start_time = time.time()\n",
                    "results = []\n",
                    "for idx, row in sample.iterrows():\n",
                    "    text = str(row['consumer_complaint_narrative'])\n",
                    "    rule_cat = row.get('complaint_category', 'Other')\n",
                    "\n",
                    "    res = {\n",
                    "        'summary': nlp_summary(text),\n",
                    "        'category': nlp_category(text, rule_cat),\n",
                    "        'emotion': nlp_emotion(text)\n",
                    "    }\n",
                    "    \n",
                    "    results.append({\n",
                    "        'complaint_id': row['complaint_id'],\n",
                    "        'llm_summary': res['summary'],\n",
                    "        'llm_category': res['category'],\n",
                    "        'llm_emotion': res['emotion']\n",
                    "    })\n",
                    "\n",
                    "    if (idx + 1) % 100 == 0:\n",
                    "        print(f\"Processing rows 0 to 1000... Checkpoint saved at row {idx+1}\")\n",
                    "\n",
                    "print(f\"\\nProcessed {len(sample)} rows in {time.time() - start_time:.2f} seconds.\")\n"
                ]

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

if __name__ == '__main__':
    strip_llms()
