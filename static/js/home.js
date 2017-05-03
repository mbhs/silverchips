var datetime; (datetime = function() {
    var now = new Date();
    var day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"][now.getDay()];
    var month = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"][now.getMonth()];
    var string = day + ", " + month + " " + now.getDate() + ", " + (now.getYear() + 1900);
    $("#datetime").html(string);
})();

setInterval(function() { datetime(); }, 1000);