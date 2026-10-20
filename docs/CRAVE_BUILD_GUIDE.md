# Complete Free Build Guide: Crave.io + GitHub Actions for Tecno KJ7

This guide provides the complete, step-by-step instructions to compile **PixelOS Android 17** for the **Tecno Spark 20 Pro+ (KJ7)** 100% for free using **Crave.io FOSS** and **GitHub Actions**.

No local disk space is consumed, and no credit card is required.

---

## 1. Prerequisites (All Free)
1. A **GitHub Account**.
2. This project directory: `KJ7-PixelOS17/`.

---

## 2. Step 1: Create Your Free Crave Account
1. Open your browser and navigate to **[foss.crave.io](https://foss.crave.io/app/#/)**.
2. Click **Sign in with GitHub** and authorize the Crave FOSS application.
3. Once logged in to the dashboard:
   - Click on your profile avatar in the top-right corner.
   - Click **Manage API Keys** or **Settings**.
   - Click **Generate New Key** / **Download crave.conf**.
   - Open the downloaded `crave.conf` in Notepad. It will look like this:
     ```json
     {
       "username": "your_github_username",
       "auth_token": "your_unique_crave_auth_token"
     }
     ```
   - Keep this text ready for Step 3.

---

## 3. Step 2: Push Your Project to GitHub
1. Create a new empty repository on GitHub:
   - Go to [github.com/new](https://github.com/new).
   - Name it `PixelOS-KJ7`.
   - Set visibility to **Public** (required for Crave FOSS free tier).
   - Do **not** initialize with README or .gitignore (we already have them).
   - Click **Create repository**.

2. In PowerShell, push this local directory to your new GitHub repository:
   ```powershell
   cd "c:\Users\User\Documents\Tecno KJ7 PixelOS\KJ7-PixelOS17"

   git init
   git branch -M main
   git add .
   git commit -m "feat(kj7): initial PixelOS Android 17 device tree, vendor, and Crave workflow"
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/PixelOS-KJ7.git
   git push -u origin main
   ```

---

## 4. Step 3: Add Your Crave API Key to GitHub Secrets
1. In your GitHub repository (`PixelOS-KJ7`), click **Settings** (gear icon on the top tab).
2. On the left sidebar, click **Secrets and variables** → **Actions**.
3. Click the green button: **New repository secret**.
4. Fill in:
   - **Name:** `CRAVE_CONF`
   - **Secret:** Paste the entire contents of your `crave.conf` file (the JSON text from Step 1).
5. Click **Add secret**.

---

## 5. Step 4: Run the Build with One Click
1. On your GitHub repository, click the **Actions** tab at the top.
2. On the left menu, click **Build PixelOS 17 on Crave**.
3. On the right side, click the **Run workflow** dropdown button.
4. Leave `userdebug` selected and click the green **Run workflow** button.

---

## 6. What Happens During the Build?
- GitHub Actions connects to the Crave high-performance cloud cluster.
- Crave clones the official **PixelOS Android 17** source tree onto its massive NVMe storage pool.
- It injects your verified **Tecno KJ7** device tree, proprietary vendor blobs, and GKI kernel.
- 16 to 32 vCPUs compile the entire operating system in **~1 to 2 hours**.
- Once compilation is complete, GitHub Actions downloads the finished flashable `.zip` (e.g. `PixelOS_kj7-17.0-*.zip`) and attaches it directly to the GitHub Actions run under **Artifacts** for you to download with one click!
