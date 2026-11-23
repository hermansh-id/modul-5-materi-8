import sys

from app import Bot
from guards import make_guards

bot = Bot(make_guards() if "--guarded" in sys.argv else None)
while True:
    print(bot.ask(input("you> ")))
    for c in bot.calls[-3:]:
        print("   tool:", c["tool"], c["args"], "(ran)" if c["ran"] else "(not run)")
