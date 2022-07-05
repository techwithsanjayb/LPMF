console.log("main hits")


function disableReadMore(className){
  console.log(document.querySelector(`.${className}`).attributes['aria-expanded'].nodeValue)
  if(document.querySelector(`.${className}`).ariaExpanded=="true"){
    if(className !== "read-more-btn1" && document.querySelector('.read-more-btn1').ariaExpanded=="false"){
      console.log("button1")
      document.querySelector('.read-more-btn1').style.display = "block";
    }
    if(className !== "read-more-btn2" && document.querySelector('.read-more-btn2').ariaExpanded=="false"){
      document.querySelector('.read-more-btn2').style.display = "block";
    }
    if(className !== "read-more-btn3" && document.querySelector('.read-more-btn3').ariaExpanded=="false"){
      document.querySelector('.read-more-btn3').style.display = "block";
    }
    if(className !== "read-more-btn4" && document.querySelector('.read-more-btn4').ariaExpanded=="false"){
      document.querySelector('.read-more-btn4').style.display = "block";
    }
    if(className !== "read-more-btn5" && document.querySelector('.read-more-btn5').ariaExpanded=="false"){
      document.querySelector('.read-more-btn5').style.display = "block";
    }
    document.querySelector(`.${className}`).style.display = "none";
    
  }
  else if(document.querySelector(`.${className}`).ariaExpanded=="false"){
    console.log("1")
    document.querySelector(`.${className}`).style.display = "block";
  }
}
// function disableLink(className){
//   console.log("recieved classname ",className)
//     console.log("disabled link ",document.querySelector(`.${className}`))
//       document.querySelector(`.${className}`).style.display = "none";
//   }

// function enableLink(className){
//   console.log("recieved classname ",className)
//   document.querySelector(`.${className}`).style.display = "block";
// }
// let readMoreBtn = document.querySelector('.read-more-btn');

// console.log(readMoreBtn)
// readMoreBtn.addEventListener('click',(e)=>{
//     console.log(text)
//    text.classList.toggle('show-more');
//    console.log(document.querySelector('.show-more')!==null)
//    if(document.querySelector('.show-more')!==null){
//     console.log(document.querySelector('.moreText').style.display)
//    if(document.querySelector('.moreText').style.display==="" || document.querySelector('.moreText').style.display==="none"){
//     console.log("i")
//     document.querySelector('.read-more-btn').innerHTML ="Read Less";
//     document.querySelector('.moreText').style.display = "inline";
//    }
// }else{
//     console.log("j")
//     document.querySelector('.read-more-btn').innerHTML ="Read More ...";
//     document.querySelector('.moreText').style.display = "none";
// }
// })
