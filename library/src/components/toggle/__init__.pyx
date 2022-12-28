from mypyguiplusultra.core import createRef
@pyx.useStylesheet(
    """
    .container{
        height:10%;
        max-height:3rem;
        margin:1rem;
        background-color:#26262a;
    }

    .option{
        display:inline-block;
        height:100%;
        opacity:0.5;
        text-align:center;
    }
    .option:active{
        background-color:#9e97dd;
        color:#111111;
        opacity:1;
    }
    """
)
class Toggle(pyx.Component):
    def init(self):
        self.activeItem = createRef()

        self.scopedStyleSheet.merge(pyx.useStylesheet(
            f"""
            .option{'{'}
                width:{(100 / len(self.props['items']) - 0.1)}%;
            {'}'}
            """
        ))

    def onMount(self):
        self.activeItem().state.add('active',updateStyles=False)
        for item in self.bodyNode().children:
            item.on.click.subscribe(self.onClick)

    def onClick(self, e):
        if e[1] is self.activeItem():return
        self.activeItem().state.remove('active')
        self.activeItem().renderNode.renderWorker.setClickable(True)
        self.activeItem.set(e[1])
        e[1].renderNode.renderWorker.setClickable(False)
        e[1].state.add('active')
        self.props['searchFilter'].set(e[1].content.lower())

    def body(self):
        return <div class="container">
            <text class="option" ref={self.activeItem}>{self.props.items[0]}</text>
            {*( <text class="option" clickable={True}>{i}</text> for i in self.props.items[1:])}
        </div>
