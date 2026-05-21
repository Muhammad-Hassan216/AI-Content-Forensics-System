Quick Git instructions for submission

1. Initialize repo (if not already):

```bash
git init
git add .
git commit -m "Initial competition-ready prototype"
```

2. Create GitHub repo and push:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

3. Recommended branch workflow during event:
- `main` — stable demo ready for judges
- `feature/*` — short-lived feature branches
