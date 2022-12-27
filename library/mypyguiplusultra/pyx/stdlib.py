from .component import Component
from .pyx_factory import createElement
from mypyguiplusultra.objects.cssom import StyleSheet
from pathlib import Path

class Body(Component):
    def body(self):
        from ..tools.renderWorkers import RootRenderWorker
        if self.props.renderWorker is None:
            self.props.renderWorker = RootRenderWorker()
        return createElement('body', self.props, *self.slots)

defaultStyles = StyleSheet.fromPath(Path(__file__).parent.parent.joinpath("objects/cssom/default-styles.css"))
