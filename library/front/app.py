import mypygui
from mypygui.tools.dev_console import run_dev_console
pages_dir = mypygui.fs.URI.from_local_path_string(__file__).parent.join('pages')

browser_window = mypygui.BrowserWindow()
browser_window.on_ready.await_result()

# TODO: Load resources that are persisted
# browser_window.load_page(pages_dir.join('add.html'), persist=True)
# browser_window.load_page(pages_dir.join('browse.html'), persist=True)
# browser_window.load_page(pages_dir.join('search.html'), persist=True)
# browser_window.resource_handler.request_resource()

xs = browser_window.load_page(pages_dir.join('browse.html'), persist=True).await_result()
browser_window.show_page(*xs)
browser_window.window_provider.root.minsize(400, 300) # kinda jank but it works ig
browser_window.on_close.await_result()

# TODO: Maybe we can like create a page solely for resource loading and once everthing has been persisted we can just like redirect
