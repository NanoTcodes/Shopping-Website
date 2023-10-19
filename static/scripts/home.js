let text=document.getElementsById('text1');

window.addEventListener('scroll',()=>{
    let value=window.scrollY;
    text.style.marginTop=value*2.5+'px';
})



