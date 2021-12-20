var review_list = "{{review_list}}"
// var reviewBtns = document.querySelectorAll('#reviewBtn')
var reviewBrand = document.querySelector('#review_brand')
reviewBrand.innerText = "{{brand}}"
var reviewProduct = document.querySelector('#review_product')
reviewProduct.innerText = "{{product}}"
var reviews = document.getElementById('reviewsTable')


Array.from(review_list).forEach((review)=>{
    var tr = document.createElement('tr')
    var sub = documnet.createElement('td')
    sub.innerText = review[2]
    var rev = documnet.createElement('td')
    rev.innerText = review[3]
    var dt = documnet.createElement('td')
    dt.innerText = review[4]
    tr.appendChild(sub)
    tr.appendChild(rev)
    tr.appendChild(dt)
    reviews.appendChild(tr)
})
// Array.from(reviewBtns).forEach((reviewBtn)=>{
//     reviewBtn.addEventListener('click', ()=>{
//         var product = reviewBtn.previousElementSibling.innerText
//         console.log(product)
        
//     })
// })