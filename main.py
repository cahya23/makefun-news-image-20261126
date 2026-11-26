# The World Today -- Thursday, 26 November 2026.
#
# A one-page newspaper front page, painted pixel by pixel with
# Python's standard library only. It reads no files, uses no
# network and no randomness, so two runs write byte-identical
# PNGs. The page is a masthead, a lead story on the US tariff
# plan with a bar chart of the proposed ceilings, six short
# stories in two rows, an also-today strip and a footer, all
# drawn with a small 5x7 bitmap font written out below.
#
# The day's stories, each date-checked against reporting
# dated 26 November 2026 (most were first reported late on
# Wednesday 25 November and carried as Thursday's news):
#   LEAD -- TARIFFS: the US proposed new tariffs on 14
#     trading partners, including Indonesia, China, the EU,
#     Japan and India, to fight excess factory capacity.
#     Proposed ceilings: Vietnam 35%, India 25%, China 20%,
#     Indonesia 18%, EU and Japan 15%. Japan called the
#     plan regrettable; Indonesia is reviewing it.
#   CAIRO: a fuel tanker crashed and caught fire on the
#     Ring Road in Warraq, killing at least 31 people and
#     injuring 21; 27 vehicles were destroyed.
#   GULF: Yemen's Houthis said they hit Saudi Arabia's
#     Ras Tanura refinery and Riyadh's financial district;
#     a projectile fell at Jazan port and a drone was
#     downed near Jeddah port. Brent rose 3.5% on Wednesday.
#   MARKETS: the Nasdaq 100 briefly fell 20% from its
#     October peak, touching bear-market ground, before
#     recovering; it closed down 0.64%. Nvidia fell 3.9%.
#   SAVASLEYKA: Ukraine said it damaged five Russian
#     jets at the Savasleyka air base, three MiG-31s and
#     two Su-34s, in strikes on 24-25 November.
#   IRAN: the US told its citizens to leave Iran at once,
#     warning hostilities could escalate fast, after Iran
#     hit US assets in Bahrain and Kuwait.
#   EU: leaders met in Brussels on Thursday to argue over
#     a 45 billion euro loan for Ukraine and a 1.6 trillion
#     euro seven-year budget; four states object to the loan.
#   ALSO: Bogor mine, 13 dead found and 13 still trapped;
#     Kim Jong Un urges wider tactical nuclear deployment;
#     the FCC cleared SpaceX to deploy 1 million Starmind
#     data-centre satellites; judges urged prosecutors to
#     drop Netanyahu's Case 4000 bribery charge; Liverpool
#     beat Club Brugge 3-0 in the Champions League.
#
# Two items from the day's wire that were NOT used: the
# Cartagena supermarket rescue (76 hostages freed) was
# already Wednesday 25 November's news, and an unverified
# Poland no-fly-zone report was left out.

import os
import struct
import zlib

W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (178, 34, 34)
NAVY = (32, 52, 96)
GREY = (110, 106, 98)
PALE = (232, 226, 212)
GOLD = (176, 132, 32)

# ---------------------------------------------------------------- font
# Glyphs are seven rows of five cells. '#' is ink, ' ' is empty.
# Only capitals are needed: every string is upper-cased first.

GLYPHS = {
    'A': (" ### ", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    'B': ("#### ", "#   #", "#   #", "#### ", "#   #", "#   #", "#### "),
    'C': (" ### ", "#   #", "#    ", "#    ", "#    ", "#   #", " ### "),
    'D': ("#### ", "#   #", "#   #", "#   #", "#   #", "#   #", "#### "),
    'E': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#####"),
    'F': ("#####", "#    ", "#    ", "#### ", "#    ", "#    ", "#    "),
    'G': (" ### ", "#   #", "#    ", "# ###", "#   #", "#   #", " ####"),
    'H': ("#   #", "#   #", "#   #", "#####", "#   #", "#   #", "#   #"),
    'I': (" ### ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    'J': ("  ###", "   # ", "   # ", "   # ", "   # ", "#  # ", " ##  "),
    'K': ("#   #", "#  # ", "# #  ", "##   ", "# #  ", "#  # ", "#   #"),
    'L': ("#    ", "#    ", "#    ", "#    ", "#    ", "#    ", "#####"),
    'M': ("#   #", "## ##", "# # #", "# # #", "#   #", "#   #", "#   #"),
    'N': ("#   #", "##  #", "# # #", "#  ##", "#   #", "#   #", "#   #"),
    'O': (" ### ", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    'P': ("#### ", "#   #", "#   #", "#### ", "#    ", "#    ", "#    "),
    'Q': (" ### ", "#   #", "#   #", "#   #", "# # #", "#  # ", " ## #"),
    'R': ("#### ", "#   #", "#   #", "#### ", "# #  ", "#  # ", "#   #"),
    'S': (" ####", "#    ", "#    ", " ### ", "    #", "    #", "#### "),
    'T': ("#####", "  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "  #  "),
    'U': ("#   #", "#   #", "#   #", "#   #", "#   #", "#   #", " ### "),
    'V': ("#   #", "#   #", "#   #", "#   #", "#   #", " # # ", "  #  "),
    'W': ("#   #", "#   #", "#   #", "# # #", "# # #", "## ##", "#   #"),
    'X': ("#   #", "#   #", " # # ", "  #  ", " # # ", "#   #", "#   #"),
    'Y': ("#   #", "#   #", " # # ", "  #  ", "  #  ", "  #  ", "  #  "),
    'Z': ("#####", "    #", "   # ", "  #  ", " #   ", "#    ", "#####"),
    '0': (" ### ", "#   #", "#  ##", "# # #", "##  #", "#   #", " ### "),
    '1': ("  #  ", " ##  ", "  #  ", "  #  ", "  #  ", "  #  ", " ### "),
    '2': (" ### ", "#   #", "    #", "   # ", "  #  ", " #   ", "#####"),
    '3': ("#####", "   # ", "  #  ", "   # ", "    #", "#   #", " ### "),
    '4': ("   # ", "  ## ", " # # ", "#  # ", "#####", "   # ", "   # "),
    '5': ("#####", "#    ", "#### ", "    #", "    #", "#   #", " ### "),
    '6': ("  ## ", " #   ", "#    ", "#### ", "#   #", "#   #", " ### "),
    '7': ("#####", "    #", "   # ", "  #  ", " #   ", " #   ", " #   "),
    '8': (" ### ", "#   #", "#   #", " ### ", "#   #", "#   #", " ### "),
    '9': (" ### ", "#   #", "#   #", " ####", "    #", "   # ", " ##  "),
    '.': ("     ", "     ", "     ", "     ", "     ", " ##  ", " ##  "),
    ',': ("     ", "     ", "     ", "     ", " ##  ", "  #  ", " #   "),
    '-': ("     ", "     ", "     ", " ### ", "     ", "     ", "     "),
    "'": ("  #  ", "  #  ", " #   ", "     ", "     ", "     ", "     "),
    '%': ("##  #", "## # ", "   # ", "  #  ", " #   ", " # ##", "#  ##"),
    '/': ("    #", "   # ", "   # ", "  #  ", " #   ", " #   ", "#    "),
    '(': ("   # ", "  #  ", " #   ", " #   ", " #   ", "  #  ", "   # "),
    ')': (" #   ", "  #  ", "   # ", "   # ", "   # ", "  #  ", " #   "),
    '+': ("     ", "  #  ", "  #  ", "#####", "  #  ", "  #  ", "     "),
    '&': (" ##  ", "#  # ", "# #  ", " #   ", "# # #", "#  # ", " ## #"),
    '!': ("  #  ", "  #  ", "  #  ", "  #  ", "  #  ", "     ", "  #  "),
    '?': (" ### ", "#   #", "    #", "   # ", "  #  ", "     ", "  #  "),
    ':': ("     ", " ##  ", " ##  ", "     ", " ##  ", " ##  ", "     "),
    ';': ("     ", " ##  ", " ##  ", "     ", " ##  ", "  #  ", " #   "),
    '$': ("  #  ", " ####", "# #  ", " ### ", "  # #", "#### ", "  #  "),
    '=': ("     ", "     ", "#####", "     ", "#####", "     ", "     "),
    ' ': ("     ", "     ", "     ", "     ", "     ", "     ", "     "),
}


# ---------------------------------------------------------------- canvas

class Page:
    def __init__(self):
        self.px = bytearray(PAPER * W * H)

    def dot(self, x, y, colour):
        if 0 <= x < W and 0 <= y < H:
            i = (y * W + x) * 3
            self.px[i:i + 3] = bytes(colour)

    def rect(self, x, y, w, h, colour):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.dot(xx, yy, colour)

    def box(self, x, y, w, h, colour):
        self.rect(x, y, w, 1, colour)
        self.rect(x, y + h - 1, w, 1, colour)
        self.rect(x, y, 1, h, colour)
        self.rect(x + w - 1, y, 1, h, colour)

    def text(self, s, x, y, scale, colour):
        s = s.upper()
        cx = x
        for ch in s:
            glyph = GLYPHS.get(ch, GLYPHS[' '])
            for r, row in enumerate(glyph):
                for c, cell in enumerate(row):
                    if cell == '#':
                        self.rect(cx + c * scale, y + r * scale,
                                  scale, scale, colour)
            cx += 6 * scale
        return cx

    def text_w(self, s, scale):
        return len(s) * 6 * scale

    def centred(self, s, y, scale, colour, x0=0, x1=W):
        w = self.text_w(s, scale)
        self.text(s, x0 + (x1 - x0 - w) // 2, y, scale, colour)

    def wrap(self, s, x, y, max_w, scale, colour, gap=10):
        words = s.upper().split()
        line = ''
        cy = y
        for word in words:
            trial = (line + ' ' + word).strip()
            if self.text_w(trial, scale) <= max_w or not line:
                line = trial
            else:
                self.text(line, x, cy, scale, colour)
                cy += 7 * scale + gap - 7 * scale
                cy += 2
                line = word
        if line:
            self.text(line, x, cy, scale, colour)
        return cy + 7 * scale


def chunk(kind, data):
    out = struct.pack('>I', len(data)) + kind + data
    out += struct.pack('>I', zlib.crc32(kind + data) & 0xFFFFFFFF)
    return out


def write_png(page, path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += page.px[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack('>IIBBBBB', W, H, 8, 2, 0, 0, 0)
    png = b'\x89PNG\r\n\x1a\n'
    png += chunk(b'IHDR', ihdr)
    png += chunk(b'IDAT', zlib.compress(bytes(raw), 9))
    png += chunk(b'IEND', b'')
    with open(path, 'wb') as f:
        f.write(png)


# ---------------------------------------------------------------- layout

def story(page, x, y, w, h, kicker, head, body):
    page.box(x, y, w, h, INK)
    page.rect(x, y, w, 3, RED)
    page.text(kicker, x + 12, y + 12, 1, RED)
    hy = y + 30
    for line in head:
        page.text(line, x + 12, hy, 2, INK)
        hy += 18
    page.wrap(body, x + 12, hy + 6, w - 24, 1, INK)


def bar_chart(page, x, y, w, title, rows):
    page.text(title, x, y, 1, NAVY)
    cy = y + 14
    for name, val in rows:
        page.text(name, x, cy, 1, INK)
        bx = x + 92
        bw = int((w - 92 - 44) * val / 35)
        page.rect(bx, cy, bw, 9, RED)
        page.text(str(val) + '%', bx + bw + 6, cy, 1, INK)
        cy += 17
    return cy


def build():
    p = Page()
    # Masthead.
    p.centred('THE WORLD TODAY', 22, 7, INK)
    p.centred('THURSDAY 26 NOVEMBER 2026  -  ONE DAY IN ONE PAGE',
              84, 2, RED)
    p.rect(28, 112, 968, 3, INK)
    p.rect(28, 118, 968, 1, INK)

    # Lead story: tariffs, with a bar chart of the ceilings.
    p.box(28, 132, 968, 296, INK)
    p.rect(28, 132, 968, 3, RED)
    p.text('LEAD  -  TRADE WAR', 44, 148, 1, RED)
    p.text('US HITS 14 PARTNERS', 44, 168, 4, INK)
    p.text('WITH NEW TARIFFS', 44, 198, 4, INK)
    p.wrap('WASHINGTON PROPOSED NEW TARIFFS ON 14 TRADING '
           'PARTNERS, INCLUDING INDONESIA, CHINA, THE EU, '
           'JAPAN AND INDIA, TO FIGHT WHAT IT CALLS EXCESS '
           'FACTORY CAPACITY. THE DUTIES WOULD FOLLOW A '
           'PUBLIC COMMENT PERIOD AND A HEARING IN JANUARY.',
           44, 238, 560, 1, INK)
    p.wrap('JAPAN CALLED THE PLAN REGRETTABLE. INDONESIA, '
           'FACING 18%, IS REVIEWING THE IMPACT WITH ITS '
           'INDUSTRIES BEFORE IT RESPONDS.',
           44, 306, 560, 1, RED)
    p.wrap('THE 14: CHINA, EU, INDIA, INDONESIA, JAPAN, '
           'SOUTH KOREA, TAIWAN, VIETNAM, THAILAND, '
           'MALAYSIA, SINGAPORE, CAMBODIA, BANGLADESH, '
           'SWITZERLAND. MEXICO AND NORWAY ARE EXCLUDED '
           'FOR NOW.',
           44, 348, 560, 1, INK)
    p.rect(628, 148, 1, 262, GREY)
    bar_chart(p, 648, 148, 332, 'PROPOSED CEILINGS, %',
              [('VIETNAM', 35), ('INDIA', 25), ('CHINA', 20),
               ('INDONESIA', 18), ('EU', 15), ('JAPAN', 15)])
    p.wrap('CHINA FACES THE HIGHEST RATE OF THE BIG '
           'ECONOMIES. VIETNAM AND INDIA PAY LESS IF '
           'THEY REACH A TRADE DEAL.',
           648, 268, 332, 1, INK)

    # Row one.
    story(p, 28, 444, 312, 196, 'EGYPT  -  DISASTER',
          ['CAIRO TANKER', 'FIRE KILLS 31'],
          'A FUEL TANKER CRASHED AND CAUGHT FIRE ON THE '
          'RING ROAD IN WARRAQ, NEAR CAIRO, KILLING AT '
          'LEAST 31 PEOPLE AND INJURING 21. THE BLAZE '
          'DESTROYED 27 VEHICLES.')
    story(p, 356, 444, 312, 196, 'GULF  -  OIL',
          ['HOUTHIS HIT', 'SAUDI REFINERY'],
          "YEMEN'S HOUTHIS SAID THEY HIT THE RAS TANURA "
          'REFINERY AND RIYADH FINANCIAL DISTRICT. A '
          'PROJECTILE FELL AT JAZAN PORT. BRENT ROSE '
          '3.5% ON WEDNESDAY.')
    story(p, 684, 444, 312, 196, 'MARKETS  -  AI SLUMP',
          ['NASDAQ BRIEFLY', 'IN BEAR MARKET'],
          'THE NASDAQ 100 FELL 20% FROM ITS OCTOBER PEAK '
          'IN EARLY TRADE, TOUCHING BEAR-MARKET GROUND, '
          'BEFORE RECOVERING TO CLOSE DOWN 0.64%. '
          'NVIDIA FELL 3.9%.')

    # Row two.
    story(p, 28, 656, 312, 196, 'WAR  -  UKRAINE',
          ['KYIV HITS FIVE', 'RUSSIAN JETS'],
          'UKRAINE SAID IT DAMAGED FIVE RUSSIAN JETS AT '
          'THE SAVASLEYKA AIR BASE, THREE MIG-31S AND '
          'TWO SU-34S, IN STRIKES ON 24-25 NOVEMBER. '
          'MOSCOW DID NOT COMMENT.')
    story(p, 356, 656, 312, 196, 'MIDDLE EAST  -  WARNING',
          ['US: LEAVE IRAN', 'AT ONCE'],
          'WASHINGTON TOLD ITS CITIZENS TO LEAVE IRAN '
          'IMMEDIATELY, WARNING HOSTILITIES COULD '
          'ESCALATE FAST, AFTER IRAN HIT US ASSETS IN '
          'BAHRAIN AND KUWAIT.')
    story(p, 684, 656, 312, 196, 'EUROPE  -  SUMMIT',
          ['EU SPLIT OVER', '45BN UKRAINE LOAN'],
          'LEADERS MET IN BRUSSELS ON THURSDAY TO ARGUE '
          'OVER A 45 BILLION EURO LOAN FOR UKRAINE AND '
          'A 1.6 TRILLION EURO BUDGET. FOUR STATES '
          'OBJECT TO THE LOAN.')

    # Also today strip.
    p.box(28, 868, 968, 116, INK)
    p.rect(28, 868, 968, 3, NAVY)
    p.text('ALSO TODAY', 44, 882, 1, NAVY)
    items = [
        ('BOGOR MINE', '13 DEAD FOUND, 13 STILL TRAPPED IN A FLOODED ILLEGAL GOLD MINE.'),
        ('KIM JONG UN', 'URGES WIDER TACTICAL NUCLEAR DEPLOYMENT, KCNA REPORTS.'),
        ('SPACEX', 'FCC CLEARS 1 MILLION STARMIND DATA-CENTRE SATELLITES.'),
        ('NETANYAHU', 'JUDGES URGE PROSECUTORS TO DROP THE CASE 4000 BRIBERY CHARGE.'),
        ('LIVERPOOL', 'BEAT CLUB BRUGGE 3-0. ISAK SCORED TWICE, WIRTZ ONCE.'),
    ]
    cx = 44
    for head, body in items:
        w = 184 if head != 'NETANYAHU' else 200
        p.text(head, cx, 902, 1, RED)
        p.wrap(body, cx, 918, w - 8, 1, INK)
        cx += w + 6
        if head != 'LIVERPOOL':
            p.rect(cx - 6, 902, 1, 66, GREY)

    # Footer.
    p.centred('SOURCES: REUTERS, AP, KCNA, FCC  -  DRAWN FROM SCRATCH, NO PHOTOS',
              996, 1, GREY)
    return p


def main():
    out = os.environ.get('MAKEFUN_OUTPUT_DIR', '/output')
    os.makedirs(out, exist_ok=True)
    write_png(build(), os.path.join(out, 'entry.png'))


if __name__ == '__main__':
    main()
