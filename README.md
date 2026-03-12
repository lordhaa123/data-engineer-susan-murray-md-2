# Payment Prediction Engine for Digital Invoice Management

## Background
NovaPay is a leading digital payments platform serving mid-sized enterprises across Europe. Their finance team needs to forecast when outstanding invoices will be paid and proactively manage the risk of late or defaulted payments. Historically, manual processes have led to unreliable projections, suboptimal cash reserves, and strained supplier relationships.

Rayze AI has been engaged to deliver a production-grade, scalable payment prediction engine that processes historical and real-time transactional data. The system must predict (1) the expected days to pay for each open invoice, and (2) the likelihood of default, enabling proactive cash flow and risk management. Success will be measured by reducing forecast error, lowering false positives in default risk, and improving cash flow variance.

## Your Task
You have been given a baseline implementation that has bugs and missing functionality. Your job is to:
1. Run the code and analyze the output — identify what's wrong with the results
2. Find and fix the bugs (hint: you can't find these just by reading the code)
3. Implement the missing features (look for TODO comments in the code)
4. Document your findings and reasoning
5. Identify and address any architectural/design issues that would cause problems at scale

## What You Are Given
- `generate_dataset.py` - Generates the starting data (run this first: `python generate_dataset.py`)
- `baseline.py` - A flawed implementation that you need to analyze, fix, and extend
- `requirements.txt` - Python dependencies

## Setup Instructions
1. Install dependencies: `pip install -r requirements.txt`
2. Generate the data: `python generate_dataset.py`
3. Run the baseline: `python baseline.py`
4. Observe the output carefully — the results are not what they seem

## What You Need To Submit
1. `improved.py` - Your fixed and improved implementation
2. `EXPLANATION.md` - A writeup containing:
   - What bugs you found and how you discovered them (severity: CRITICAL / IMPORTANT / MINOR)
   - What features you implemented and your design decisions
   - What design/architectural improvements you made and why they matter at scale
   - Why each issue matters in a production environment
   - Your final results and how they compare to the baseline
3. Push all changes to this repository before the deadline

## What "Done" Looks Like
- All bugs are identified and fixed
- All TODO features are implemented and working
- Architectural issues are identified and addressed
- Your solution produces correct, reliable results
- Code is clean, readable, and production-ready
- EXPLANATION.md clearly communicates your findings and reasoning

## Time Limit
- Target: 90 minutes
- Grace period: 30 minutes (total 120 minutes)
- Your submission will be auto-graded at the 120-minute mark based on your latest push

## Rules
- You may use any libraries listed in requirements.txt
- You may add additional libraries if needed (add them to requirements.txt)
- Internet access is allowed (documentation, StackOverflow, etc.)
- AI tools (ChatGPT, Copilot, etc.) are allowed, but your EXPLANATION.md must demonstrate YOUR understanding
- Do NOT modify generate_dataset.py
