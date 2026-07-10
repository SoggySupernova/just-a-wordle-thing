import colorsys, subprocess, sys, time
from colorama import init
subprocess.run('cls',shell=True)
init()
def rgb(h_deg, s_pct, l_pct):
    h = h_deg / 360.0
    s = s_pct / 100.0
    l = l_pct / 100.0
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return int(round(r * 255)), int(round(g * 255)), int(round(b * 255))

def ansi(r, g, b):
    return '\033[48;2;'+str(r)+';'+str(g)+';'+str(b)+'m'

def fore(r, g, b):
    return '\033[38;2;'+str(r)+';'+str(g)+';'+str(b)+'m'
reset = '\033[0m'

def hsl(h, s, l):
    r, g, b = rgb(h, s, l)
    return ansi(r, g, b)


def fade(r,g,b,w):
    return int(r*w), int(g*w), int(b*w)


import random

with open("possibleanswers.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    random_line = random.choice(lines)
    possibleanswers = lines
    
with open("allowedguesses.txt", "r", encoding="utf-8") as file:
    allowedguesses = file.readlines()

for i in range(len(allowedguesses)):
    allowedguesses[i] = allowedguesses[i].strip().upper()
for i in range(len(possibleanswers)):
    possibleanswers[i] = possibleanswers[i].strip().upper()


word = random_line.strip().upper()

# guess = "chili"
guess = ""

while guess != word:
    # Newline and show cursor
    sys.stdout.write("\n> \033[?25h")
    guess = input("").upper()
    # clear the input line
    sys.stdout.write('\033[?25l\x1b[1A\x1b[2K')
    sys.stdout.flush()
    if guess in allowedguesses or guess in possibleanswers:
        0
    else:

        # Clear not allowed text
        for i in range(10):
            nr, ng, nb = fade(212, 45, 36, 1-0.09*i)
            sys.stdout.write('\r\033[2K'+"> "+fore(nr, ng, nb)+'Not allowed'+reset)
            sys.stdout.flush()
            time.sleep(.03)

        sys.stdout.write('\033[2K\x1b[1A')
        sys.stdout.flush()
        continue
    letters = list(word)
    colors = list(guess)
    # get green letters
    for i in range(len(guess)):
        if guess[i] in word and word[i] == guess[i]:
            # use up this letter
            letters[i] = ""
            colors[i] = "green"
    # Check remaining letters
    for i in range(len(guess)):
        if guess[i] in letters:
            # do not overwrite greens
            if colors[i] != "green":
                # use up this letter
                # Find where the actual letter is and delete it so future things will be gray instead of a duplicate yellow
                letters[letters.index(guess[i])] = ""
                colors[i] = "yellow"
        else:
            # Do not overwrite greens
            if colors[i] != "green":
                colors[i] = "gray"
    print("  ",end="")
    for i in range(len(guess)):
        r = 0
        g = 0
        b = 0
        colstring = ""
        if colors[i] == "green":
            r, g, b = (0, 185, 0)
        if colors[i] == "yellow":
            r,g,b = (170, 170, 0)
        if colors[i] == "gray":
            r,g,b = (128, 128, 128)
        # Animation
        for w in range(10):
            if w > 0:
                sys.stdout.write('\033[K\033[3D')
                sys.stdout.flush()
            newr, newg, newb = fade(r,g,b,w/10)
            print("\033[?25l"+ansi(newr, newg, newb),guess[i],end=" "+reset)
            sys.stdout.flush()
            time.sleep(0.015)
        time.sleep(0.04)
    print(reset,end="")
    
