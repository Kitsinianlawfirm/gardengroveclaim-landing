# Landing Page Deployment Guide

## Files
- `index.html` — the page (single file, all CSS inline)
- `hero.jpg` — hero background photo
- `logo.png` — Kitsinian Law Firm white logo

## Two things to do before going live

### 1. Set up Formspree (3 min) — so the form actually sends emails

The form currently has a placeholder action URL. Replace it:

1. Go to **https://formspree.io** → Sign up (free plan = 50 submissions/month)
2. Click **New Form**
3. Name: `Garden Grove Tank Leak Landing`
4. Email destination: `occlaim@kitsinianlaw.com`
5. Formspree shows you a URL like `https://formspree.io/f/abc1234`
6. Open `index.html` in any text editor
7. Find this line:
   ```
   action="https://formspree.io/f/REPLACE_ME_WITH_FORMSPREE_ID"
   ```
8. Replace `REPLACE_ME_WITH_FORMSPREE_ID` with your actual ID (just the `abc1234` part)
9. Save

First submission triggers a Formspree verification email — click the link to confirm `occlaim@kitsinianlaw.com` as the destination.

### 2. Deploy the files

You bought just the domain on GoDaddy. You need hosting. **Three options**, ranked by ease:

#### Option A: Netlify Drop (recommended — 2 min, free, no signup needed)

1. Go to **https://app.netlify.com/drop**
2. Drag this entire `landing-page` folder onto the page
3. You get a random URL like `wonderful-tank-abc123.netlify.app` — site is live immediately
4. Sign up (free) to keep it permanent
5. Connect your custom domain `gardengrovetankleak.com`:
   - Netlify dashboard → Domain settings → Add custom domain → enter `gardengrovetankleak.com`
   - Netlify shows you DNS records to set
6. In GoDaddy DNS settings, set:
   - `A` record → `75.2.60.5` (Netlify load balancer)
   - `CNAME` record (www) → `your-site.netlify.app`
7. Wait 10-60 min for DNS propagation. Done.

**Pros:** Free, fast CDN, automatic HTTPS, zero config
**Cons:** None for this use case

#### Option B: Cloudflare Pages (best long-term, free, ~5 min)

1. Go to **https://pages.cloudflare.com** → Sign up (free)
2. Click **Create a project** → Direct Upload
3. Project name: `gardengrovetankleak`
4. Upload the `landing-page` folder
5. Deploy
6. Add custom domain in Cloudflare Pages settings
7. Cloudflare gives you DNS records to add at GoDaddy (or you can transfer DNS management to Cloudflare for $0)

**Pros:** Same as Netlify + better caching, unlimited bandwidth, free SSL
**Cons:** Slightly more setup

#### Option C: GoDaddy Web Hosting (~$5-10/month, the "everything in one place" option)

1. In GoDaddy, upgrade to **Web Hosting Economy plan** (~$5/month)
2. Use cPanel File Manager to upload `index.html`, `hero.jpg`, `logo.png` to `public_html/`
3. Domain auto-connects since both are on GoDaddy

**Pros:** All-in-one billing with GoDaddy
**Cons:** Slower than Netlify/Cloudflare, costs money, GoDaddy hosting performance is notoriously meh

## Recommended path

Do **Option A (Netlify Drop)** today. Takes 2 minutes. Free forever for this traffic level. You can migrate later if you outgrow it (which is unlikely).

## After deployment

Verify the page works end-to-end:

1. Open `gardengrovetankleak.com` in a browser → page loads
2. Fill out the form with a test entry → submit
3. Check `occlaim@kitsinianlaw.com` → email arrives within seconds
4. Check on mobile (iPhone Safari, Android Chrome) → looks right
5. Add the URL to your Meta lead form's `follow_up_action_url` so people who tap "Visit our website" on the thank-you screen land here too:
   - Open Meta Forms Library → GG Chem Leak — Intake v5 → wait, can't edit published forms
   - Workaround: create form v6 with the new URL when you next iterate

## Optional: add tracking

If you want to track landing-page conversion rates separate from Meta lead form conversions:

1. **Add Meta Pixel** to the page (so the website also feeds Meta's algo):
   - Paste your Pixel base code in the `<head>` of `index.html`
   - The page already has `fbq('track', 'Lead')` firing on form submit (see the script at the bottom)
2. **Add Google Analytics or Plausible** if you want bounce rate / source attribution

I can wire either of these up — just give the word.

## File structure when deployed

```
gardengrovetankleak.com/
├── index.html        ← the page
├── hero.jpg          ← background image
└── logo.png          ← firm logo
```

That's it. Three files. No build step, no framework, loads in <1 second.

## Future iterations to consider

- Add a video embed (autoplay your motion ad as a section)
- Add a Spanish-language version at `/es`
- Add a "Frequently Asked Questions" section
- Add testimonials once you have client results
- A/B test headline + photo

Just say the word for any of these.
