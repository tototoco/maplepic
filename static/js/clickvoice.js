
var a= document.getElementsByTagName('a');
var lent=a.length;

const audio = document.createElement("audio");
audio.src = "/static/sound/click.wav";

const audio1 = document.createElement("audio");
audio1.src = "/static/sound/touch.wav";

for (var i=0;i<lent;++i){

 a[i].addEventListener('mouseenter', function(e){   
    audio1.play();
 }, false);

 a[i].addEventListener('click', function(e){   
    
   audio.play();
}, false);
}

