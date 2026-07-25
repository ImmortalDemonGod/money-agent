# Google Search Console verification + sitemap submission (mechanical steps)

Both hosts are static Vercel deploys the agent fully controls, so it can host any verification file.

1. Open https://search.google.com/search-console and add two URL-prefix properties:
   - `https://chat-export-seven.vercel.app/`
   - `https://life-in-weeks-iota-two.vercel.app/`
2. For each property, use the **HTML file** verification method. Google provides a file named
   `google<hash>.html` with a one-line content.
3. Return, via the encrypted return channel, the exact filename and contents for BOTH properties.
   The agent will host each file at its domain root and redeploy, then the operator clicks Verify.
4. After both verify, under **Sitemaps**, submit `sitemap.xml` for each property:
   - `https://chat-export-seven.vercel.app/sitemap.xml`
   - `https://life-in-weeks-iota-two.vercel.app/sitemap.xml`
   (Both already return HTTP 200.)
5. Under **URL Inspection**, request indexing for each homepage.

Return value: the two `google<hash>.html` filenames and their contents. No credentials needed.
