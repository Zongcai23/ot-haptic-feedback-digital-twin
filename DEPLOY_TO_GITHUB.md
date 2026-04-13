# 🌐 Deploy to GitHub and GitHub Pages

## Option A — Easiest (web upload)
1. Unzip this package locally.
2. Go to GitHub and click **New repository**.
3. Create a public repository, for example: `ot-haptic-feedback-digital-twin`.
4. Open the new repository and click **uploading an existing file**.
5. Drag **all extracted files and folders** into the page and commit them.
6. Open **Settings → Pages**.
7. Under **Build and deployment**, choose:
   - **Source**: `Deploy from a branch`
   - **Branch**: `main`
   - **Folder**: `/docs`
8. Click **Save**.
9. Wait about 1–3 minutes.
10. Your website link will usually be:
    `https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPOSITORY_NAME/`

## Option B — Git command line
```bash
git init
git branch -M main
git add .
git commit -m "Initial public release for haptic-feedback module"
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME.git
git push -u origin main
```
Then enable GitHub Pages using the same **`main` + `/docs`** setting described above.

## Recommended links for your paper
- **Project website**: `https://YOUR_GITHUB_USERNAME.github.io/YOUR_REPOSITORY_NAME/`
- **Repository**: `https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPOSITORY_NAME`

## Optional final cleanup after deployment
After the site is live, you can replace placeholders such as:
- `YOUR_GITHUB_USERNAME`
- `YOUR_REPOSITORY_NAME`
inside `README.md` if you want the homepage button to point to the final GitHub Pages URL.
