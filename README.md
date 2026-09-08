# Beyond Gradients

A fast, accessible static homepage for [beyondgradients.com](https://beyondgradients.com). Plain HTML, CSS, JavaScript and inline SVG. No npm packages, external fonts, analytics, cookies or server runtime.

## Preview locally

From this repository, run:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000. Stop the server with Ctrl+C. Open `/404.html` to preview the error page; Python's server does not automatically serve it for unknown paths, but GitHub Pages does.

## Edit content

- `index.html`: page structure, copy and SEO metadata.
- `styles.css`: design, responsive layouts, focus states and reduced-motion support.
- `script.js`: mobile navigation and the illustrative attention interaction. No animation loop or network requests.
- `content/site.json`: the single editing location for Instagram/YouTube profile URLs and the six explanation records.
- `scripts/build_content.py`: optional, dependency-free content generator. The generated HTML is committed, so hosting requires no build.
- `assets/beyond-grad-logo.png`: brand logo used throughout the site, including favicon, social metadata and Apple touch icons.
- `404.html`, `robots.txt`, `sitemap.xml`: error and search-engine support.

After changing `content/site.json`, run:

```sh
python3 scripts/build_content.py
```

The generator updates platform links, structured metadata and the marked explanation grid in `index.html`. Each record supports title, category, description, diagram (`visual`), platform, optional `format`, an optional direct `url`, and an optional local `thumbnail` image path. To publish a card, set its `url` to the real explanation and optionally set `format` (for example `6 min · Video`). Until then, cards say **Topic preview** and link to the chosen channel, without claiming an unpublished explanation exists. Edit diagrams in `illustration()`, or set `thumbnail` to a repository-relative image path to replace the diagram. Thumbnail space is reserved to prevent layout shift.

The attention illustration uses invented, normalized values for a single unmasked self-attention head. It is a teaching diagram, not live model data or a claim about the attention weights of ChatGPT.

## GitHub Pages

The existing `CNAME` is preserved as `beyondgradients.com`. Publish the repository root using the repository's existing Pages source branch. `.nojekyll` serves the files directly; no framework, package installation, workflow or server is needed. Commit and push the site files to the configured Pages branch to deploy. In GitHub → Settings → Pages, verify that **Deploy from a branch** points to that branch and **/(root)**, the custom domain is `beyondgradients.com`, and HTTPS is enabled. Repository settings and DNS are external to this checkout and are not modified by this implementation.

All navigation and cards are available without JavaScript. The mobile menu and attention selector progressively enhance the page. The 404 page uses root-relative assets so it works for nested missing URLs on the custom domain.
