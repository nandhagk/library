if False:from mypygui.page.scripts.script_globals import *

search_results = document.get_element_by_id('search-results')

def add_search_results(results : list):
    def add_result(result):
        xs = DOMNode(
            class_list=ClassList('search-result'),
            children=[
                DOMNode(
                    class_list=ClassList('person-info__name-container'),
                    children=[DOMNode(tag='span', class_list=ClassList('person-info__name-text'), content=result['name'])]
                )
            ]
        )
        search_results.append_child(xs, _reflow=False)
        def handle_click(e):
            tmp_store.requested_person = result
            redirect(document.root_directory._uri.make('person-info.html'))
        xs.event_emitter.subscribe(Event.Types.click, handle_click)
    for result in results:
        add_result(result)

    document.root.render_node.request_reflow()

def clear_search_results():
    for child in search_results.children:
        child.remove(_reflow=False, _remove_from_parent=False)
    search_results.children.clear()
    search_results.render_node.request_reflow()


add_search_results([
    {
        'name': 'Ramji2'
    },
    {
        'name': 'Boss'
    }
])

def unload(e):
    global search_results
    search_results = None

page_closed.then(unload)
