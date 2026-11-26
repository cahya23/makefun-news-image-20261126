#!/usr/bin/env python3
"""THE WORLD TODAY - Thursday 26 November 2026.

Draws a one-page newspaper front page in pure Python stdlib.
No network, no randomness, no file reads. The image is drawn
from scratch with a hand-typed 5x7 bitmap font and a hand-written
PNG encoder (zlib + struct). Two runs give identical bytes.
"""
import os
import struct
import zlib

W = 1024
H = 1024

WHITE = (255, 255, 255)
BLACK = (10, 10, 10)
INK = (20, 20, 20)
GREY = (90, 90, 90)
LIGHT = (238, 238, 238)
NAVY = (18, 42, 86)
RED = (168, 28, 28)
BLUE = (28, 78, 150)

# 5x7 bitmap font, typed by hand. Each glyph is 7 rows of 5 bits.
FONT = {
    'A': ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    'B': ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    'C': ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    'D': ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    'E': ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    'F': ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    'G': ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    'H': ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    'I': ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    'J': ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    'K': ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    'L': ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    'M': ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    'N': ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    'O': ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    'P': ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    'Q': ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    'R': ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    'S': ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    'T': ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    'U': ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    'V': ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    'W': ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    'X': ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    'Y': ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    'Z': ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    '0': ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    '1': ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    '2': ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    '3': ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    '4': ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    '5': ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    '6': ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    '7': ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    '8': ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    '9': ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    ' ': ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    '.': ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ',': ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ':': ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ';': ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    '-': ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    '%': ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    '(': ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ')': ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    '/': ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '&': ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    '+': ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    '?': ("01110", "10001", "00001", "00110", "00100", "00000", "00100"),
    '!': ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    '=': ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
}

pix = bytearray(W * H * 3)
for _i in range(W * H):
    pix[_i * 3] = 255
    pix[_i * 3 + 1] = 255
    pix[_i * 3 + 2] = 255


def set_px(x, y, col):
    if 0 <= x < W and 0 <= y < H:
        o = (y * W + x) * 3
        pix[o] = col[0]
        pix[o + 1] = col[1]
        pix[o + 2] = col[2]


def fill_rect(x, y, w, h, col):
    for yy in range(y, y + h):
        for xx in range(x, x + w):
            set_px(xx, yy, col)


def box(x, y, w, h, col, thick=2):
    fill_rect(x, y, w, thick, col)
    fill_rect(x, y + h - thick, w, thick, col)
    fill_rect(x, y, thick, h, col)
    fill_rect(x + w - thick, y, thick, h, col)


def hline(x, y, w, col, thick=2):
    fill_rect(x, y, w, thick, col)


def text_w(s, scale):
    return len(s) * 6 * scale - scale


def draw_text(x, y, s, scale, col):
    s = s.upper()
    cx = x
    for ch in s:
        g = FONT.get(ch, FONT[' '])
        for r in range(7):
            row = g[r]
            for c in range(5):
                if row[c] == '1':
                    fill_rect(cx + c * scale, y + r * scale, scale, scale, col)
        cx += 6 * scale
    return cx


def draw_centered(y, s, scale, col):
    draw_text((W - text_w(s, scale)) // 2, y, s, scale, col)


def wrap(s, scale, max_w):
    words = s.upper().split(' ')
    lines = []
    cur = ''
    for wd in words:
        trial = wd if not cur else cur + ' ' + wd
        if text_w(trial, scale) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_para(x, y, s, scale, col, max_w, lh=None):
    if lh is None:
        lh = 7 * scale + 4
    for ln in wrap(s, scale, max_w):
        draw_text(x, y, ln, scale, col)
        y += lh
    return y


def chunk(tag, data):
    c = struct.pack('>I', len(data)) + tag + data
    return c + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)


def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw.extend(pix[y * W * 3:(y + 1) * W * 3])
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    data = b'\x89PNG\r\n\x1a\n'
    data += chunk(b'IHDR', ihdr)
    data += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    data += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(data)


def story_box(x, y, w, h, title, body):
    fill_rect(x, y, w, h, LIGHT)
    box(x, y, w, h, BLACK, 2)
    ty = draw_para(x + 12, y + 10, title, 2, NAVY, w - 24, 18)
    hline(x + 12, ty + 2, w - 24, RED, 3)
    draw_para(x + 12, ty + 10, body, 2, INK, w - 24, 18)


def main():
    # Masthead
    fill_rect(24, 14, 976, 4, NAVY)
    draw_centered(26, "THE WORLD TODAY", 8, NAVY)
    draw_centered(88, "THURSDAY 26 NOVEMBER 2026", 3, BLACK)
    hline(24, 110, 976, BLACK, 3)

    # Lead story
    fill_rect(24, 120, 976, 320, WHITE)
    box(24, 120, 976, 320, BLACK, 3)
    draw_text(40, 132, "LEAD STORY - TRADE", 2, RED)
    draw_text(40, 156, "US PROPOSES NEW TARIFFS", 4, BLACK)
    draw_text(40, 190, "ON 14 TRADING PARTNERS", 4, BLACK)
    hline(40, 228, 944, GREY, 2)
    ly = draw_para(40, 240, "WASHINGTON PROPOSES NEW TARIFFS ON 14 TRADING "
        "PARTNERS TO FIGHT EXCESS FACTORY CAPACITY. DUTIES FOLLOW A PUBLIC "
        "COMMENT PERIOD AND A HEARING IN JANUARY. JAPAN CALLED THE PLAN "
        "REGRETTABLE. INDONESIA, AT 18 PERCENT, IS REVIEWING THE IMPACT.",
        2, INK, 540, 18)
    draw_para(40, ly + 8, "THE 14: CHINA, EU, INDIA, INDONESIA, JAPAN, SOUTH "
        "KOREA, TAIWAN, VIETNAM, THAILAND, MALAYSIA, SINGAPORE, CAMBODIA, "
        "BANGLADESH, SWITZERLAND. MEXICO, NORWAY OUT FOR NOW.",
        2, INK, 540, 18)
    # Chart on the right of the lead
    draw_text(612, 240, "PROPOSED CEILINGS", 2, NAVY)
    hline(612, 260, 360, RED, 3)
    bars = [("VIETNAM", 35), ("INDIA", 25), ("CHINA", 20),
            ("INDONESIA", 18), ("EU", 15), ("JAPAN", 15)]
    by = 272
    for name, val in bars:
        draw_text(612, by, name, 2, INK)
        bw = int(val * 180 / 35)
        fill_rect(736, by + 2, bw, 10, BLUE)
        draw_text(736 + bw + 8, by, str(val) + "%", 2, BLACK)
        by += 28

    # Six story boxes, two rows of three
    bw3 = 317
    stories = [
        ("CAIRO TANKER FIRE KILLS 31",
         "FUEL TANKER CRASHED AND CAUGHT FIRE ON THE RING ROAD IN WARRAQ, "
         "NEAR CAIRO. AT LEAST 31 DEAD, 21 INJURED. 27 VEHICLES DESTROYED."),
        ("HOUTHIS HIT SAUDI REFINERY",
         "HOUTHIS SAID THEY HIT THE RAS TANURA REFINERY AND RIYADH FINANCIAL "
         "DISTRICT. A PROJECTILE FELL AT JAZAN PORT. BRENT ROSE 3.5 PERCENT "
         "ON WEDNESDAY."),
        ("NASDAQ BRIEFLY IN BEAR MARKET",
         "NASDAQ 100 FELL 20 PERCENT FROM ITS OCTOBER PEAK IN EARLY TRADE, "
         "BEFORE RECOVERING TO CLOSE DOWN 0.64 PERCENT. NVIDIA FELL 3.9 PERCENT."),
        ("KYIV HITS FIVE RUSSIAN JETS",
         "UKRAINE SAID IT DAMAGED FIVE RUSSIAN JETS AT SAVASLEYKA AIR BASE, "
         "THREE MIG-31S AND TWO SU-34S, IN STRIKES ON 24-25 NOVEMBER. "
         "MOSCOW DID NOT COMMENT."),
        ("US: LEAVE IRAN AT ONCE",
         "WASHINGTON TOLD ITS CITIZENS TO LEAVE IRAN IMMEDIATELY, WARNING "
         "HOSTILITIES COULD ESCALATE FAST, AFTER IRAN HIT US ASSETS IN "
         "BAHRAIN AND KUWAIT."),
        ("EU SPLIT OVER 45BN UKRAINE LOAN",
         "LEADERS MET IN BRUSSELS ON THURSDAY OVER A 45 BILLION EURO LOAN "
         "FOR UKRAINE AND A 1.6 TRILLION EURO BUDGET. FOUR STATES OBJECT."),
    ]
    for i, (t, b) in enumerate(stories):
        col = i % 3
        row = i // 3
        x = 24 + col * (bw3 + 12)
        y = 452 + row * (190 + 12)
        story_box(x, y, bw3, 190, t, b)

    # Also-today strip
    fill_rect(24, 856, 976, 116, LIGHT)
    box(24, 856, 976, 116, BLACK, 2)
    draw_text(40, 866, "ALSO TODAY", 2, RED)
    also = [
        "BOGOR MINE: 13 DEAD FOUND, 13 STILL TRAPPED IN A FLOODED ILLEGAL GOLD MINE.",
        "KIM JONG UN: URGES WIDER TACTICAL NUCLEAR DEPLOYMENT, KCNA REPORTS.",
        "SPACEX: FCC CLEARS 1 MILLION STARMIND DATA-CENTRE SATELLITES.",
        "NETANYAHU: JUDGES URGE PROSECUTORS TO DROP THE CASE 4000 BRIBERY CHARGE.",
        "LIVERPOOL: BEAT CLUB BRUGGE 3-0. ISAK SCORED TWICE, WIRTZ ONCE.",
    ]
    ay = 888
    for line in also:
        draw_text(40, ay, line, 2, INK)
        ay += 17

    # Footer
    draw_centered(986, "SOURCES: REUTERS, AP, KCNA, FCC - DRAWN FROM SCRATCH, NO PHOTOS.", 2, GREY)

    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out, exist_ok=True)
    write_png(os.path.join(out, "entry.png"))


if __name__ == "__main__":
    main()
