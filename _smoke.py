import glob
import sys

from streamlit.testing.v1 import AppTest

failed = False
for f in [r"app.py", r"home.py"] + sorted(glob.glob("lessons/**/*.py", recursive=True)):
    at = AppTest.from_file(f, default_timeout=25)
    at.run()
    errs = [e.value for e in at.exception]
    if errs:
        failed = True
        print("FAIL", f)
        for e in errs:
            print("   ", str(e)[:300])
    else:
        print("OK  ", f)
sys.exit(1 if failed else 0)