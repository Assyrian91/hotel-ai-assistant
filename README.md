> ⚠️ **This repo has moved.** It's now maintained as part of
> [`hotel-intelligence-suite`](https://github.com/Assyrian91/hotel-intelligence-suite),
> a consolidated collection of hotel operations projects, with full commit
> history preserved. This repo is archived and kept read-only for reference.

---



# 🏨 AI Hotel Operations Assistant

An intelligent chat-based hotel management assistant powered by RAG, SQL agents, and LLMs.

![Python](https://img.shields.io/badge/Python-3.11-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green) ![LangChain](https://img.shields.io/badge/LangChain-0.3-orange)

## Features
- 💬 **Chat interface** — ask questions in natural language
- 💰 **Revenue insights** — 30-day summaries, RevPAR, ADR
- 📈 **Pricing suggestions** — dynamic recommendations based on occupancy
- 🌍 **Guest analytics** — nationalities, loyalty tiers, stay duration
- 📋 **Policy Q&A** — RAG-powered hotel policy retrieval

## Architecture
User → FastAPI → LangChain Router → [SQL Agent | RAG Chain] → Groq LLM

## Quick Start
git clone https://github.com/YOUR_USERNAME/hotel-ai-assistant
cd hotel-ai-assistant
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your GROQ_API_KEY
python data/seed.py
uvicorn app.main:app --reload

## Tech Stack
LangChain · FAISS · FastAPI · SQLite · Groq (LLaMA 3.1) · HuggingFace Embeddings
