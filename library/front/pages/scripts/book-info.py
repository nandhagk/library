if False:from mypygui.page.scripts.script_globals import *

print(tmp_store)

def unload(e):
    del tmp_store.requested_book

page_closed.then(unload)
