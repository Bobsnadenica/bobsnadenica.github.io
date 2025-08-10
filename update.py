name: Daily ChatGPT and Grok Update

on:
  schedule:
    - cron: '0 6 * * *'  # Runs daily at 06:00 UTC
  workflow_dispatch:      # Allows manual trigger too

jobs:
  update:
    runs-on: ubuntu-latest
    permissions:
      contents: write  # Grant write permissions for GITHUB_TOKEN
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Fetch full history to ensure Git detects changes

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install openai requests

      - name: Create errors directory if it doesn't exist
        run: |
          mkdir -p errors
          git add errors
          git commit -m "Create errors directory" || echo "No changes to commit"

      - name: Run update script
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          GROK_API_KEY: ${{ secrets.GROK_API_KEY }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # Add GitHub token for error.txt upload
        run: python generate_conspiracy_pages.py

      - name: Debug Git status
        run: |
          git status
          git diff --name-only
          ls -la Chatgpt.html Grok.html error.txt || echo "One or more files missing"

      - name: Commit and push
        run: |
          git config user.name "github-actions"
          git config user.email "github-actions@github.com"
          # Add files only if they exist
          [ -f Chatgpt.html ] && git add Chatgpt.html || echo "Chatgpt.html not generated"
          [ -f Grok.html ] && git add Grok.html || echo "Grok.html not generated"
          [ -f error.txt ] && git add error.txt || echo "error.txt not generated"
          git commit -m "Daily ChatGPT and Grok update - $(date -u +%Y-%m-%d)" || echo "No changes to commit"
          git push origin ${{ github.ref_name }}
