var filterBtn = document.getElementById("filterBtn")
// var printResult = "{{printresult}}"
var filter = document.querySelector("#filterWord")
var filterVal = document.getElementById("filter_val")

if(filter.value != ''){
    var filterWord = filter.value
    filterVal.setAttribute('value', filterWord)
    var cards = document.getElementsByClassName('col')
    var filteredlist = []
    Array.from(cards).forEach((card)=>{
        var brand = (card.children[0].getElementsByClassName('card-header')[0].innerText)
        var product = (card.children[0].getElementsByClassName('card-title')[0].innerText)
        if (brand.includes(filterWord) || product.includes(filterWord)){
            card.style.display='inline-block'

        }
        else{
            card.style.display='None'
        }

    })
}

filter.addEventListener('keyup',()=>{
    // var filterVal = document.getElementById("filter_val")
    var filterWord = filter.value
    filterVal.setAttribute('value', filterWord)
    var cards = document.getElementsByClassName('col')
    var filteredlist = []
    Array.from(cards).forEach((card)=>{
        var brand = (card.children[0].getElementsByClassName('card-header')[0].innerText)
        var product = (card.children[0].getElementsByClassName('card-title')[0].innerText)
        if (brand.includes(filterWord) || product.includes(filterWord)){
            card.style.display='inline-block'

        }
        else{
            card.style.display='None'
        }

    })
})

// filterBtn.addEventListener("click",()=>{
//     var filterWord = document.querySelector("#filterWord").value
    
// })

// var form1 = document.querySelector('#seemodal')
// form1.on('submit',)