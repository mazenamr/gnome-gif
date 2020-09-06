#!/usr/bin/python

# author: Mazen Amr
# title: gnome-gif
# license: MIT License

import subprocess, sys, os

def main():
    if len(sys.argv) < 2:
        printhelp(1)
    if sys.argv[1] in ["-h", "--help"]:
        printhelp(0)
    if sys.argv[1].split(".")[-1] != "gif":
        printhelp(2)
    gifname = ".".join(sys.argv[1].split(".")[:-1])
    gifdir = os.path.expanduser(f"~/.local/share/backgrounds/{gifname}")
    makepngs(gifname, gifdir)
    makexml(gifname, gifdir)

def printhelp(exitcode):
    print("Usage: python gnome-gif.py filename.gif")
    print("This program outputs a .xml file to ~/.local/share/backgrounds")
    print("Select this file in gnome tweaks tool to use the animated wallpaper")
    print("This program requires ImageMagick to run")
    sys.exit(exitcode)

def makepngs(gifname, gifdir):
    os.makedirs(gifdir, exist_ok=True)
    try:
        subprocess.run(["convertt", "-coalesce", f"{gifname}.gif", f"{gifdir}/{gifname}.png"])
    except FileNotFoundError:
        printhelp(3)
    print(f"{gifdir}/{gifname}.png")

def makexml(gifname, gifdir):
    with open(f"{os.path.expanduser('~/.local/share/backgrounds/')}{gifname}.xml", "w") as f:
        # f.write("""<background>\n\t<starttime>\n\t\t<year>2011</year>\n\t\t<month>11</month>\n\t\t<day>24</day>\n\t\t<hour>7</hour>\n\t\t<minute>00</minute>\n\t\t<second>00</second>\n\t</starttime>\n""")
        f.write("<background>\n")
        durations = subprocess.run(["identify", "-format", "%T ", f"{gifname}.gif"], stdout=subprocess.PIPE)
        for i, d in enumerate(durations.stdout.decode("utf-8").split(" ")[:-1]):
            f.write(f"<static>\n<duration>{int(d)/100}</duration>\n<file>{gifdir}/{gifname}-{i}.png</file>\n</static>\n")
            # f.write(f"<static>\n<duration>{1}</duration>\n<file>{gifdir}/{gifname}-{i}.png</file>\n</static>\n")
        f.write("</background>")

if __name__ == "__main__":
    main()
