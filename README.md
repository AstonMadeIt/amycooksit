# Amy Cooks It

Austin landing page for [amycooksit.com](https://amycooksit.com/). GitHub Pages serves the files on `main`. The registrar already points the domain at GitHub Pages. Do not change DNS to publish a copy edit.

`content/site.json` is the menu. `python3 scripts/build.py` writes `index.html`.

```sh
python3 scripts/build.py
git add -A
git commit -m "Update the table"
git push
```

## Replace a photograph

Keep the filename, replace the file, and rebuild. The build adds a short hash to the image URL, so a same-name swap does not stick in a browser cache.

- Hero: `assets/images/jerk.jpg`
- Mark: `assets/images/logo.jpg`
- Event: `assets/images/events/<name>.jpg`, then an entry in `events`

The hero is a generated serving illustration. The caption says so. Replace it with a photograph from a real plate before treating the picture as service.

## Add an event

Append to `events` in `content/site.json`:

```json
{
  "date": "2026-12-06",
  "title": "Crestview dinner",
  "blurb": "Forty people. Mojo pernil. The room stayed.",
  "image": "assets/images/events/crestview.jpg",
  "alt": "Chafing dishes of pernil and rice on a dining table"
}
```

`image` may be omitted for a text-only note. Newest date renders first. An empty list keeps the quiet Austin book. Do not invent a photograph for a night that has not happened.

## Instagram and TikTok

Instagram is [instagram.com/amycooksit](https://www.instagram.com/amycooksit/). TikTok is `social.tiktok`. Leave it `null` until the real URL exists. A null value hides the link.

## What this page will not invent

Prices, the phone number, and the dish list come from `site.json`. The public phone is the number already printed on the 2025 holiday menu. Supper delivery is Brentwood, Crestview, and Allandale. Events and catering are quoted, with Austin delivery confirmed in that quote. The New York holiday menu stays archived. It is not the Austin offer.

## Check

```sh
python3 scripts/build.py --check
```
