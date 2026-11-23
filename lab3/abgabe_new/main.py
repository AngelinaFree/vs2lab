import subprocess
import sys
import time
from pathlib import Path

import constPipe

BASE = Path(__file__).parent
FILE = sys.argv[1] if len(sys.argv) > 1 else "text.txt"
MAPPER_COUNT = 3


def start(script, *args):
    return subprocess.Popen([sys.executable, str(BASE / script), *args], cwd=BASE)


reducers, mappers = [], []
try:
    # 1. Reducer zuerst (Nummern ab 1, passend zu sys.argv[1] - 1 im Reducer)
    for i in range(1, len(constPipe.reducer_connections) + 1):
        reducers.append(start("reducer.py", str(i)))
    time.sleep(1)

    # 2. Mapper
    for _ in range(MAPPER_COUNT):
        mappers.append(start("mapper.py"))
    time.sleep(1)

    # 3. Splitter zuletzt
    splitter = start("splitter.py", FILE)
    splitter.wait()

    # 4. Warten, bis die Reducer per Timeout fertig sind und ihr Endergebnis ausgegeben haben
    for r in reducers:
        r.wait()
finally:
    # 5. Mapper laufen endlos, also beenden (auch bei Strg+C alles aufräumen)
    for p in mappers + reducers:
        if p.poll() is None:
            p.terminate()