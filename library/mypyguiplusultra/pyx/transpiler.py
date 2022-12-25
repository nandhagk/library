# from pyx_transpiler import transpilePyx as tp
from ._transpiler import transform, setGlobals

def tp(raw : str,
    createMethod="createElement", 
    autoImports = """# Automatic Imports
from pathlib import Path
# End of automatic imports :(

""", 
    cssImportMethod="importCSS"):
    setGlobals(createMethod=createMethod,autoImports=autoImports, cssImportMethod=cssImportMethod)
    return transform(raw)
def transpilePyx(raw : str):
    return tp(
        raw,
        createMethod="pyx.pyx_factory.createElement" ,
        autoImports="""# Automatic Imports from mypyguiplusultra :)
import mypyguiplusultra.pyx.pyx_factory
import mypyguiplusultra.pyx as pyx
from pathlib import Path
# End of automatic imports :(

""", cssImportMethod="mypyguiplusultra.objects.StyleSheet.fromPath"
)
