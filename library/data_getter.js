if (document.location.href.startsWith("https://www.goodreads.com/book/show")){
data = JSON.parse(localStorage.getItem("mydata") || "[]")
document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookPageMetadataSection__genres > ul > div > button").click()
document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookPageMetadataSection__description > div > div.TruncatedContent__gradientOverlay > div > button").click()
document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > div > button").click()
console.log("Adding shit")
data.push({
"imgSource" : document.querySelector(".BookCover__image").querySelector("img").src,
"description" : document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookPageMetadataSection__description > div > div.TruncatedContent__text.TruncatedContent__text--large.TruncatedContent__text--expanded > div > div > span").innerText,
"pages" : document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > div.BookDetails__list > span > div > dl > div:nth-child(1) > dd > div > div.TruncatedContent__text.TruncatedContent__text--small").innerText.split(" ")[0] - 0,
"publisher" : document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > div.BookDetails__list > span > div > dl > div:nth-child(2) > dd > div > div.TruncatedContent__text.TruncatedContent__text--small").innerText.split("by")[1].trim(),
"publishedDate" : document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.BookDetails > div > span:nth-child(2) > div.BookDetails__list > span > div > dl > div:nth-child(2) > dd > div > div.TruncatedContent__text.TruncatedContent__text--small").innerText.split("by")[0].trim(),
"author" : document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageMetadataSection > div.PageSection > div.AuthorPreview > div > div.FeaturedPerson__profile > div.FeaturedPerson__container > div.FeaturedPerson__info > div.FeaturedPerson__infoPrimary > h4 > a > span.ContributorLink__name").innerText,
"title" : document.querySelector("#__next > div > main > div.BookPage__gridContainer > div.BookPage__rightColumn > div.BookPage__mainContent > div.BookPageTitleSection > div > h1").innerText,
"tags" : Array.from(document.querySelectorAll(".Button.Button--tag-inline.Button--small")).filter(i => {return i.href.includes("genres")}).map(i=> {return i.children[0].innerText})
})
localStorage.setItem("mydata", JSON.stringify(data))
}