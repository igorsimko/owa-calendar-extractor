// uncomment if you want to save log file into your G Drive folder
// var dir = DriveApp.getFolderById("<< YOUR GOOGLE DRIVE FOLDER ID>>");

// GOOGLE CALENDAR IDENTIFICATOR in form - aaaa1123@group.calendar.google.com
var calendar = CalendarApp.getCalendarById("<<YOUR GOOGLE CALENDAR IDENTIFICATOR>>");

function doGet(e) {
  return insertData(e, null);
}

function insertData(req, calendar){
  // for test purpose uncomment line down below
  // var data = req.parameter.data;
  var data = JSON.parse(quoteKeys(decodeURIComponent(req.parameter.data)));
  // var file = dir.createFile("log-" + new Date().getTime() + ".txt", JSON.stringify(data));
  var calendarEvents = createEvents(data);
  insertToCalendar(calendarEvents);
  
  return ContentService.createTextOutput(req.parameter.callback + '('+ JSON.stringify('[{"message":"insert successfull."},{"data": ' + JSON.stringify(req) + '}]')+')').setMimeType(ContentService.MimeType.JAVASCRIPT);
}

function createEvents(data){
  for(var i = 0; i < data.length; i++){
    for(var k = 0; k < data[i].events.length; k++){
      var dateStr = "";
      var wholeDay = false;
      
      if(data[i].events[k][0].toString().indexOf(':') !== -1){
        dateStr = data[i].date + " " + data[i].events[k][0];
      } else {
        dateStr = data[i].date + " " + "00:00";
        wholeDay = true;
      }
      var eStartTime = new Date(dateStr);
      var eEndTime = new Date(dateStr);
      
      var eDuration = data[i].events[k][2];
      if(eDuration && eDuration.length > 0){
        eEndTime.setMinutes(parseInt(eEndTime.getMinutes()) + parseInt(eDuration.split(':')[1]));
        eEndTime.setHours(parseInt(eEndTime.getHours()) + parseInt(eDuration.split(':')[0]));
        
        if(wholeDay){
          eEndTime.setMinutes(59);
          eEndTime.setHours(23);
        }
      }

      var e = {title: data[i].events[k][1], startTime: eStartTime, endTime: eEndTime, location: data[i].events[k][3]}
      if(typeof e !== "undefined"){
        insertToCalendar(e);
      }
    }
  }
}

function insertToCalendar(e){
  if(!e){
    Logger.log("Undefined event.");
    return;
  }
  var eventExists = false;
  calendar.getEventsForDay(e.startTime).forEach(function(calEvent){
    if(e && e.title == calEvent.getTitle()){
      Logger.log(calEvent.getTitle());
      eventExists = true;
      return;
    }
  });
  
  if(!eventExists){
    calendar.createEvent(e.title, e.startTime, e.endTime, {location: e.location});
    Logger.log("Added - " + e.title);
  }
}

function quoteKeys(data){
  return data.replace(/([{,])(\s*)([A-Za-z0-9_\-]+?)\s*:/g, '$1"$3":');
}

// test request
function test(){
  doGet({'parameter':{'data':[{"date": "8/31/2018", "events": [["Dovolenka", "1 de\u0148", "", ""]]}, {"date": "8/27/2018", "events": [["12:00", "Design a architekt\u00fara EMANS - Workshop", "4:0", "ANA-multifunkcna zasadacka"]]}, {"date": "8/28/2018", "events": [["9:30", "Lunys intro", "1:30", "ANA-multifunkcna zasadacka"], ["13:00", "Architekt\u00fara a design Lunysu", "2:0", "ANA-multifunkcna zasadacka"]]}, {"date": "9/4/2018", "events": [["14:00", "Lunys PP - aktualne info + najblizsi plan", "1:30", "ANA-velka stredna zasadacka"]]}]
,'callback':'callbackkk'}});
}