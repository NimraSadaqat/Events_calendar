console.log("hello world");

window.onload = function() {
  var today = new Date();
  var mm = String(today.getMonth() + 1) //January is 0!
  var yyyy = today.getFullYear();
  var month = document.getElementById('month');
  month.value = mm;
  var year = document.getElementById('year');
  year.value = yyyy;
};

function selectdate() {
  console.log("hello function2");
  var month = document.getElementById('month').value
  console.log(month);
  var year = document.getElementById('year').value
  console.log(year);
  var a = document.getElementById('submit')
  a.href += year +"-"+ month;
  console.log(a.href);
}
