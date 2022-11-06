if False:from mypygui.page.scripts.script_globals import *


sidebar = document.get_element_by_id('sidebar')
# document.get_element_by_id('sidebar-menu').event_emitter.subscribe(Event.Types.click, lambda e:sidebar.state.toggle('active'))
sidebar.event_emitter.subscribe(Event.Types.click, lambda e:sidebar.state.toggle('active'))
sidebar.event_emitter.never_propogate = True

def handle_sidebar_item(si):
    if si.attrs.destination is None:return
    if si.attrs.current is not None:
        si.state.add('current')
        return
    def handle_click(e):
        redirect(document.root_directory._uri.make(si.attrs.destination + '.html'))
    si.event_emitter.subscribe(Event.Types.click, handle_click)

for si in sidebar.children:handle_sidebar_item(si)
def unfocus_sidebar(e):
    global sidebar
    if not sidebar.state.contains('active'):return
    sidebar.state.remove('active')

document.root.event_emitter.subscribe(Event.Types.click, unfocus_sidebar)
def unload(e):
    global sidebar
    sidebar = None
page_closed.then(unload)
