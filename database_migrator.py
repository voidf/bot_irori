from GLOBAL import *
from database_utils import *

class Sniffer(Document, Base):
    player = ReferenceField(Player, primary_key=True)
    commands = DictField()

import os
for i in os.listdir('sniffer/'):
    print(i)
    with open(f"sniffer/{i}", 'r') as f:
        j = json.load(f)
        ist = i.strip()
        p = Player.objects(pid=ist).first()
        if not p:
            p = Player(pid=ist).save()
        if not Sniffer.objects(player=p):
            Sniffer(player=p, commands=j).save()
        print(j)