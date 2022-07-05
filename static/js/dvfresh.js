
function loadHTML(){//要得div id

  fetch('myWeb.py')
  .then((response) => {
    // 操作 response 屬性、方法
    return response.json();
  })
  .then((data) => {
    // 實際存取到資料
    document.getElementById('now').innerHTML = data;
    console.log(data);
  })
  .catch((error) => {
    // 錯誤回應
    console.log(error);
  });
}

function getNews(path) {
  url='http://'+path
  fetch(url)
  .then(response => response.text())  
  .then(text => {
      console.log(text);
      document.getElementById("shownews").innerHTML = text
  })
}

//https://www.delftstack.com/zh-tw/howto/javascript/load-html-file-javascript/
//https://www.casper.tw/javascript/2017/12/28/javascript-fetch/S