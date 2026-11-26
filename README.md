# The World Today — Thursday 26 November 2026

A one-page newspaper front page summing up the world's news of
Thursday 26 November 2026, drawn from scratch in pure Python
(stdlib only, no photos, no network, no randomness).

## The image

- Lead story: the US proposes new tariffs on 14 trading partners
  to fight excess factory capacity, with a bar chart of the
  proposed ceilings — Vietnam 35%, India 25%, China 20%,
  Indonesia 18%, EU 15%, Japan 15% (Reuters, 26 Nov 2026).
- Cairo tanker fire kills 31 on the Ring Road in Warraq
  (Reuters, 26 Nov 2026).
- Houthis hit the Saudi Ras Tanura refinery; Brent rose 3.5%
  (Reuters, 26 Nov 2026).
- Nasdaq 100 briefly touched bear-market ground, down 20% from
  its October peak, before recovering (Reuters, 26 Nov 2026).
- Ukraine damaged five Russian jets at Savasleyka air base
  (Reuters, 26 Nov 2026).
- Washington told its citizens to leave Iran at once
  (Reuters, 26 Nov 2026).
- EU leaders split over a 45 billion euro loan for Ukraine
  (Reuters, 26 Nov 2026).
- Also today: the flooded illegal gold mine in Bogor, Kim Jong Un
  on tactical nuclear weapons, SpaceX's FCC clearance, the
  Netanyahu Case 4000 recommendation, and Liverpool 3-0 Club Brugge.

## Build

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` draws the 1024x1024 PNG with a hand-typed 5x7 bitmap
font and a hand-written PNG encoder. Two runs produce identical bytes.
