if False:from mypygui.page.scripts.script_globals import *

currently_focused_input : DOMNode = None

def handle_search_input(i):
    def handle_click(e):
        e.propogate = False
        global currently_focused_input
        if currently_focused_input is not None:
            currently_focused_input.state.remove('active')
        i.state.add('active')
        currently_focused_input = i

    i.event_emitter.subscribe(Event.Types.click, handle_click)
    i.event_emitter.subscribe(Event.Types.key_press, lambda e:validate_text_input(e, i.children[0].children[0], clipboard, lambda j:i.state.contains('active') and e.info._e.char not in ('\r', '\n')))

for i in document.get_elements_by_class_name('search-param__input-container'):
    handle_search_input(i)
def unfocus_input(e):
    global currently_focused_input
    if currently_focused_input is not None:
        currently_focused_input.state.remove('active')
        currently_focused_input = None
document.root.event_emitter.subscribe(Event.Types.click, unfocus_input)



def unload(e):
    global currently_focused_inputs
    currently_focused_input = None

page_closed.then(unload)
