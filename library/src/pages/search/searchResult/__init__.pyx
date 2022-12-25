import styles from './searchResult.css'
from mypyguiplusultra.core import createRef

from .paginator import Paginator
SET_SIZE = 10

def getResultsSize(query):
    # TODO: SQL
    print("TODO: Get Results Size")
    return 31

def getResults(query, start):
    # TODO: SQL
    print("TODO: Getting results")
    return [
        {'locator' : {123:1}, 'primaryText' : "Hello", 'secondaryText' : 'world', 'chips' : ['yo', 'mama', 'gae']},
        {'locator' : {123:1}, 'primaryText' : "Hello", 'secondaryText' : 'world', 'chips' : ['yo', 'mama', 'gae']},
    ]

@styles
class SearchResult(pyx.Component):


    def init(self):
        self.resultContainer = createRef()
        self.paginator = createRef()
        self.currentQuery = None # The query stored (since new queries must be created on paginate :))

    def onClick(self, e):
        # TODO: Redirect to information page
        print("TODO: Redirect to info page")

    def clearResults(self):
        rc = self.resultContainer()

        for child in rc.children:
            child.remove(_relayout=False, _removeFromParentList=False)
        rc.children.clear()

    def updateQuery(self, query):
        self.clearResults()
        self.currentQuery = query

        # Get the count of results of query
        total = getResultsSize(self.currentQuery)

        # Update paginator
        self.paginator().setTotalPages(total)


    def showSubResults(self, start): # Shows the currentQuery from result number <start>
        # Clear the results if any
        self.clearResults()

        # Query
        results = getResults(self.currentQuery, start)

        rc = self.resultContainer()
        # When query completes show the results (using getResultNode)
        for result in results:
            rc.appendChild(self.getResultNode(result), _relayout=False)

        xs = rc.renderNode.reflow()
        for child in rc.children:
            child.renderNode.renderWorker.paint()
        xs.renderWorker.update()


    def getResultNode(self, result):
        xs = <div class="result" locator={result['locator']} clickable={True}>
            <div class="textContainer">
                <span class="primaryText">{result['primaryText']}</span>
                <span class="secondaryText">{result['secondaryText']}</span>
            </div>
            <div class="chipContainer">
                {*( <span class="chip">{i}</span> for i in result['chips'] )}
            </div>
        </div>
        xs.on.click.subscribe(self.onClick)
        return xs

    def body(self):
        return <div class="container">
            <text class="heading">Results:</text>
            <div class="resultContainer" ref={self.resultContainer} />
            <Paginator ref={self.paginator} setSize={SET_SIZE} searchCommand={self.showSubResults}/>
        </div>
