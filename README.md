# Valve Partners

Website for valvepartners.com.  VALVE is the family: Vicki, Ayden, Lauren, Vincent and Eric.

## Pages

- `index.html`: home page, the five partners, and the contact form
- `tutoring.html`: Ayden's tutoring page (Humboldt County)
- `values.html`: core values page
- `logos.html`: logo options page (not linked from the menu)
- `lauren.html`: Lauren's page, bread and soccer training (bread photos go in `assets/lauren/`)

## Logo

Chosen logo: "Under One Roof" in Gold on Navy (option H4).  Colors: navy #1B1F3B, soft blues #E9EEF6 #C8D4E6 #A6B9D6 #86A0C6, white, gold #C9A227.

- `assets/logo/valve-partners.svg`: main logo, gold on navy
- `assets/logo/valve-partners-light.svg`: version for white backgrounds
- `assets/logo/valve-partners-wide.svg`: wide version for headers and letterhead
- `assets/logo/valve-partners-icon.svg`: icon (site icon and profile pictures)
- `assets/logo/options/`: every option from all rounds

## Custom domain

The site runs at valvepartners.com (CNAME file).  DNS is in Cloudflare, set up the same way as caliit.com: three A records for valvepartners.com (185.199.109.153, 185.199.110.153, 185.199.111.153) and a www CNAME to hbliving33.github.io, all proxied, with SSL/TLS mode Full.

## Settings to change

- Contact email: the first line of `script.js` (`CONTACT_EMAIL`)
- Vincent's business link (TopFlight Services): his name and the link with `id="vincent-link"` in `index.html`
