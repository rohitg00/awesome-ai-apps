# Remio Personal Knowledge Agent

A Streamlit app that uses the Remio desktop app as a local-first memory and RAG layer for personal knowledge.

## Overview

Remio indexes and parses local notes, files, webpages, recordings, emails, messages, images, and other knowledge sources. This example shows how an AI app can use Remio as its local knowledge base, retrieving targeted context through `remio rag` and `remio search_notes` instead of repeatedly scanning raw files or sending whole documents to an LLM.

## Features

- Local-first semantic retrieval over indexed personal knowledge
- RAG answers with `remio rag`
- Semantic note search with `remio search_notes`
- File, webpage, recording, email, message, and image coverage through Remio's parser/index
- Remio desktop app check with a download/open link to https://remio.ai/
- Smaller prompts by retrieving only relevant context before answer synthesis

## Tech Stack

- Python
- Streamlit
- Remio desktop app
- Remio CLI access to the local Remio knowledge base

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Install or open Remio:

   ```text
   https://remio.ai/
   ```

3. Verify Remio:

   ```bash
   remio doctor
   ```

4. Run the app:

   ```bash
   streamlit run app.py
   ```

## Usage

Choose **RAG answer** to ask a question over your Remio knowledge base, or **Search notes** to retrieve matching notes. If the Remio desktop app or CLI access is unavailable, the app displays a Remio download/open button.
