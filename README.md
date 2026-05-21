# AI Engineer Portfolio

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
