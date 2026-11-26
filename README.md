# The World Today — 26 November 2026

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/cahya23/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/cahya23/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

A one-page newspaper front page summing up world news on Thursday, 26 November 2026.

## What the image shows

Masthead **THE WORLD TODAY**, dated Thursday, 26 November 2026, above a lead
story on the US tariff plan with a bar chart of the proposed ceilings, and
smaller stories on Cairo, the Gulf, the markets, Ukraine, Iran and the EU.
Everything is drawn from scratch with Python's standard library only — a
hand-made 5x7 bitmap font and a hand-written PNG encoder — no photographs
or copied images.

## The stories

1. **US HITS 14 PARTNERS WITH NEW TARIFFS** — Washington proposed new
   tariffs on 14 trading partners, including Indonesia, China, the EU,
   Japan and India, to fight excess factory capacity. Proposed ceilings:
   Vietnam 35%, India 25%, China 20%, Indonesia 18%, EU and Japan 15%.
   Japan called the plan regrettable; Indonesia is reviewing it.
   (Reuters, 25–26 Nov 2026.)
2. **CAIRO TANKER FIRE KILLS 31** — A fuel tanker crashed and caught fire
   on the Ring Road in Warraq, near Cairo, killing at least 31 people and
   injuring 21. The blaze destroyed 27 vehicles. (Reuters, 26 Nov 2026.)
3. **HOUTHIS HIT SAUDI REFINERY** — Yemen's Houthis said they hit the Ras
   Tanura refinery and Riyadh's financial district. A projectile fell at
   Jazan port. Brent rose 3.5% on Wednesday. (Reuters, 26 Nov 2026.)
4. **NASDAQ BRIEFLY IN BEAR MARKET** — The Nasdaq 100 fell 20% from its
   October peak in early trade, touching bear-market ground, before
   recovering to close down 0.64%. Nvidia fell 3.9%. (Reuters, 26 Nov 2026.)
5. **KYIV HITS FIVE RUSSIAN JETS** — Ukraine said it damaged five Russian
   jets at the Savasleyka air base, three MiG-31s and two Su-34s, in
   strikes on 24–25 November. Moscow did not comment. (Reuters, 26 Nov 2026.)
6. **US: LEAVE IRAN AT ONCE** — Washington told its citizens to leave Iran
   immediately, warning hostilities could escalate fast, after Iran hit
   US assets in Bahrain and Kuwait. (Reuters, 25 Nov 2026.)
7. **EU SPLIT OVER 45BN UKRAINE LOAN** — Leaders met in Brussels on
   Thursday to argue over a 45 billion euro loan for Ukraine and a 1.6
   trillion euro budget. Four states object to the loan.
   (Reuters, 26 Nov 2026.)
8. **ALSO TODAY** — Bogor mine: 13 dead found, 13 still trapped; Kim Jong
   Un urges wider tactical nuclear deployment; the FCC cleared SpaceX to
   deploy 1 million Starmind data-centre satellites; judges urged
   prosecutors to drop Netanyahu's Case 4000 bribery charge; Liverpool
   beat Club Brugge 3-0. (Reuters, 26 Nov 2026.)

Two items were deliberately left out: the Cartagena supermarket rescue
(76 hostages freed) was already Wednesday 25 November's news, and an
unverified Poland no-fly-zone report was not used.

## Build

```bash
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` paints the page pixel by pixel and encodes the PNG by hand with
`zlib` and `struct`. It reads no files, uses no network and no randomness,
so two runs write identical bytes.
