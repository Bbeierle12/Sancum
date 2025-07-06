
# Phase 2: Usage Walk-Through

This document provides a sample interaction flow for using the new local micro-services with your Custom GPT.

### Setup

1.  Start the services and the `ngrok` tunnel by running `./scripts/run_ngrok.sh`.
2.  Copy the public HTTPS URLs provided by `ngrok`.
3.  In the ChatGPT "Create-a-GPT" interface, go to **Configure > Actions**.
4.  Create two new actions, one for each service.
5.  For the schema of each action, copy the content from `docs/function_specs.json`.
6.  In the schema for each action, replace the placeholder server URL with your `ngrok` URL for the corresponding service (e.g., `https://<random-id>.ngrok.io`).
7.  Under **Authentication**, select "API Key", paste your `${SANCTUM_API_KEY}` value, choose "Bearer" as the Auth Type, and save.

---

### Demo 1: Adding a Verse

**Your Prompt to SanctumGPT:**
> "Please add John 3:16 to my memory. The text is 'For God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life.' Tags are Atonement, Love, and Grace. Emotions are Love, Hope, Gratitude. My note is 'The gospel in miniature.'"

**Expected Assistant Action:**
The GPT will call the `add_verse_to_memory` function, sending a request to your `cme_service` ngrok endpoint. The body of the request will look like this:
```json
{
  "verse_id": "John_3_16",
  "text": "For God so loved the world...",
  "covenant_tags": ["Atonement", "Love", "Grace"],
  "emotion_codes": ["Love", "Hope", "Gratitude"],
  "notes": "The gospel in miniature."
}
```

---

### Demo 2: Requesting Flashcards

**Your Prompt to SanctumGPT:**
> "Show me my flashcards for today."

**Expected Assistant Action:**
The GPT will make a GET request to the `/flashcards` endpoint of your `cme_service`. It will then display the verse(s) that are due for review.

---

### Demo 3: Analyzing a Psalm

**Your Prompt to SanctumGPT:**
> "Analyze the structure of Psalm 23."

**Expected Assistant Action:**
The GPT will first find the text of Psalm 23 from its internal knowledge, then call the `analyze_scripture_structure` function, sending the full text to your `pivot_service` ngrok endpoint. It will receive back the analysis and present it to you.
```json
{
  "text_to_analyze": "The Lord is my shepherd; I shall not want. He maketh me to lie down in green pastures..."
}
```
