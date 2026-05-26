---
title: SEC RAG
emoji: 📄
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---


#AI Engineer Portfolio

Documenting my transition from SDE → AI Engineer.

## Projects
- LoanBot RAG (in progress)
- LLM Inference Optimizer (coming June)
- Credit Risk ML Pipeline (coming July)

## Week 1 Progress
- Completed fast.ai Lessons 1–4 (model training, deployment basics)
- Read Attention Is All You Need (abstract + intro) and Karpathy's Intro to LLMs
- Wrote personal notes on tokens, embeddings, and attention
- Set up Python environment, HuggingFace account, GitHub repo (ai-portfolio)
- Deployed an image classifier to HuggingFace Spaces (live URL)
- Called Anthropic API to answer a question about a loan document
- Built LoanBot skeleton: FastAPI, ChromaDB, PDF loading
- First commit to ai-portfolio with README (goal + timeline)

## Week 2 Progress
- Watched LangChain RAGAS from scratch video (covered RAGAS metrics + re-ranking concept)
- Fixed XBRL garbage issue in 10-K parsing (stripped hidden div, found usable text start)
- Built and tested full QA chain — retrieval + Claude response + fallback
- Pushed to GitHub

What I got stuck on:
- Raw .htm file was 100KB of XBRL metadata, not text — had to strip hidden div and find real content start

What to carry forward tomorrow:
- Thu: Run RAGAS evaluation, record actual scores
- ## Evaluation — RAGAS Results
## Architecture

![RAG Pipeline](./rag-pipeline.png)


Evaluated on 10 questions: 5 answerable from indexed data, 5 requiring 
full 10-K (not in 100KB excerpt).

| Metric | Answerable | Unanswerable |
|--------|-----------|--------------|
| Faithfulness | 1.000 | 0.893 |
| Answer Relevancy | 0.765 | 0.000 |
| Context Precision | 0.500 | 0.628 |
| Context Recall | 0.800 | 0.800 |

### Findings

**Faithfulness (0.893 unanswerable):** Fallback instruction works but 
model occasionally adds unsupported suggestions (e.g. "refer to capital 
management section"). Its not in retrieved context — genuine faithfulness 
failure. Fix is to add stricter fallback instruction.

**Answer Relevancy (0.0 unanswerable):** This is because some fallback answers 
reference what IS in the document rather than addressing the question. 
This is a known RAGAS limitation on fallback responses, not a model failure.

**Context Precision (0.50 answerable):** Retrieved chunks contain 
significant irrelevant content. 500 token chunks are probably too large. This means relevant 
information shares chunks with noise. Week 3 will test 256/512/1024 
token sizes.

**Context Recall (0.0 — business segments):** Retrieval failure on an 
answerable question. Segment information exists in indexed data but 
ChromaDB probably returned wrong chunks. This is likely caused by chunking splitting 
the segment description across chunk boundaries. Will try to increase overlap to 10% of chunk size.

### Limitations
- Scores have run-to-run variance due to LLM-based evaluation
- Unanswerable ground truths artificially influence recall scores
- 100KB truncation excludes financial statements — revenue, capital 
  ratios, and income figures are not evaluable from this dataset


### Eval scores with langGraph (no re ranking)
## RAGAS Evaluation — Baseline (LangGraph query rewriter, no reranking)

### Overall
| Metric | Answerable | Unanswerable | Overall
|---|---|---|----|
| Faithfulness | 0.800 | 0.920 | 0.860
| Answer Relevancy | 0.771 | 0.000 | 0.385
| Context Precision | 0.533 | 0.500 | 0.517
| Context Recall | 0.800 | 0.800 | 0.800

### Per Question
| Question | Faithfulness | Answer Relevancy | Context Precision | Context Recall | Answerable |
|---|---|---|---|---|---|
| Where is JPMorgan Chase headquartered? | 1.00 | 0.986 | 1.000 | 1.0 | Yes |
| What is JPMorgan Chase's ticker symbol and on which exchange does it trade? | 0.50 | 0.940 | 0.333 | 1.0 | Yes |
| What are JPMorgan Chase's three reportable business segments? | 0.50 | 0.000 | 0.000 | 0.0 | Yes |
| How many employees does JPMorgan Chase have globally? | 1.00 | 0.927 | 1.000 | 1.0 | Yes |
| What were JPMorgan Chase's total assets as of December 31, 2025? | 1.00 | 1.000 | 0.333 | 1.0 | Yes |
| What is JPMorgan Chase's net interest income for 2025? | 1.00 | 0.000 | 0.639 | 1.0 | No |
| What is JPMorgan Chase's CET1 capital ratio? | 1.00 | 0.000 | 0.806 | 1.0 | No |
| Who is the CEO of JPMorgan Chase? | 1.00 | 0.000 | 0.000 | 0.0 | No |
| What is JPMorgan Chase's total revenue for 2025? | 1.00 | 0.000 | 0.417 | 1.0 | No |
| What is JPMorgan Chase's return on equity? | 0.60 | 0.000 | 0.639 | 1.0 | No |

### Averages by Answerability
| Answerable | Faithfulness | Answer Relevancy | Context Precision | Context Recall |
|---|---|---|---|---|
| Yes | 0.80 | 0.771 | 0.533 | 0.8 |
| No | 0.92 | 0.000 | 0.500 | 0.8 |

> Note: Answer Relevancy is 0.0 for unanswerable questions by design — the model correctly responds with "I don't have that information" which RAGAS scores as irrelevant.
