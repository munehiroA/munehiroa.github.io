# v2 verification — 2026-09-27

- 16 content pages rendered in Chromium at 1440, 390 and 320 px: no horizontal overflow, exactly one h1, all images decoded.
- All local HTML links, fragment targets, scripts, styles, posters and media references resolved, including redirects and root-relative 404 links.
- EN/JA language switching retains the corresponding page and section; no automatic locale redirect.
- Legacy #work route tested. Other legacy routes use the same mapping implementation.
- Reduced-motion setting prevents automatic video playback; explicit playback, 0.5× speed and retained manual pause verified.
- Home, people and publications desktop views and English/Japanese mobile home views visually inspected.
- Bibliographic metadata checked for 33 listed published/conference works plus 1 separately labelled preprint.

Scope: local Chromium rendering. Hosting configuration, live 301 responses, other browser engines, search indexing and all external profile links were not comprehensively tested. Existing public site has not been deployed or changed.
