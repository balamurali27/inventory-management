function showAllTimesInLocal() {
  times = document.getElementsByTagName("time");
  console.log(times);
  for (const time of times) {
    datetime = time.getAttribute("datetime");
    time.innerHTML = moment.utc(datetime).local().format("LLLL");
  }
}
showAllTimesInLocal();
