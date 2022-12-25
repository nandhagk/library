from .dom import DOMNode
from .render_tree import RenderNode, RootRenderNode
from .cssom import StyleSheet

def getDefaultRenderWorker(tag):
    from mypyguiplusultra.tools.renderWorkers import NormalRenderWorker, TextRenderWorker, SVGRenderWorker, ImageRenderWorker
    if tag in {'text', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}:
        return TextRenderWorker()
    elif tag in {'svg'}:
        return SVGRenderWorker()
    elif tag in {'img'}:
        return ImageRenderWorker()
    else:
        return NormalRenderWorker()
def traverseTree(node, callback, *args, **kwargs):
    for i in node.children:
        callback(i, node, *args, **kwargs)
        traverseTree(i, callback, *args, **kwargs)

def linkNode(node, parent, gss, wp):
    node.styles.globalStyleSheet = gss

    if node.styles.scopedStyleSheet is None:
        node.styles.scopedStyleSheet = parent.styles.scopedStyleSheet

    node.styles.computeStyles(notifyElement=False)
    # NOTE: We can add custom qelems here
    qh = node.attrs.get('renderWorker')
    if qh is None:
        qh = getDefaultRenderWorker(node.tag)

    node.renderNode = RenderNode(node, wp, renderWorker=qh)

    if node.tag == 'button':
        node.attrs['clickable'] = node.attrs.get('clickable', True)
    elif node.tag == 'img':
        node.renderNode.renderWorker.loadImageFromSource(node.attrs['source'])


def linkDom(root, gss, wp):
    root.renderNode = RootRenderNode(root, wp, renderWorker=root.attrs['renderWorker'])
    if root.styles.scopedStyleSheet is None:root.styles.scopedStyleSheet = StyleSheet()
    root.styles.globalStyleSheet = gss
    root.styles.computeStyles(notifyElement=False)


    traverseTree(root, linkNode, gss, wp)
