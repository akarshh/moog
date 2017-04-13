var ss = SpreadsheetApp.openById('1nuA-k3Z62Nb4ZT-ZxtO8ypFgOtITxHYI5JaGdPkx96I');
var sheet = ss.getSheetByName('Sheet1');

function doGet(e) {
  var temp = e.parameter.value;
  var read = e.parameter.value;
  var depth = e.parameter.depth;
  var d = new Date();
  var c;
  var tempCell;
  var depthCell;
  var time;
  var cell2;


   if (temp != undefined && depth != undefined) {
    c = sheet.getRange('D2').getValue();
    tempCell = 'A'+ c;
    time = 'B' + c;
    depthCell = 'C' + c;
    var currentTime = d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds(); // "12:35 PM", for instance
    if (temp > 250 || depth > 10) {
       sendEmails(value, currentTime);
    }
    sheet.getRange(tempCell).setValue(temp);
    sheet.getRange(time).setValue(currentTime);
    sheet.getRange(depthCell).setValue(depth);
    c++;
    sheet.getRange('D2').setValue(c);
    if (c > 3600 && d.getHours > 17 && d.getHours < 9) {
      //Assuming machine works for 10 hours till 6pm
      //We get 1 value every 10 sec so 3600 every 10 hr
      c = 2;
   }
  }
}
function sendEmails(value, time) {
  var sheet = SpreadsheetApp.getActiveSheet();
  var maxt = sheet.getRange('E2').getValue();
  var mint = sheet.getRange('F2').getValue();
  var avgt = sheet.getRange('G2').getValue();
  var stddevt = sheet.getRange('H2').getValue();
  var maxf = sheet.getRange('E4').getValue();
  var minf = sheet.getRange('F4').getValue();
  var avgf = sheet.getRange('G4').getValue();
  var stddevf = sheet.getRange('H4').getValue();
  var emailAddress = "machinehealthgtmoog@gmail.com";  // First column
  var message = "The parameter has exceeded the trigger value. Current status: "
      + value + " at " + time + " Temperature - Maximum value: " + maxt + " Minimum value: "
      + mint + " Average: " + avgt + " Standard Deviation: " + stddevt;
      + " Fluid Level - Maximum value: " + maxf + " Minimum value: "
      + minf + " Average: " + avgf + " Standard Deviation: " + stddevf;
  var subject = "Critical Threshold Crossed";
  MailApp.sendEmail(emailAddress, subject, message);
  SpreadsheetApp.flush();
}
function doPost(e) {
  var avg = e.parameter.average;
  var maxVal = e.parameter.maxVal;
  var stdDev = e.parameter.stdDev;
  var timeElapsed = e.parameter.timeElapsed;
  var d = new Date();

  var c, avgCell, maxCell, stdDevCell, timeElapsedCell, timeCell;

  if (avg != undefined) {
    var currentTime = d.getHours() + ":" + d.getMinutes() + ":" + d.getSeconds(); // "12:35 PM", for instance
    c = sheet.getRange('P2').getValue();
    avgCell = 'J' + c;
    maxCell = 'K' + c;
    stdDevCell = 'L' + c;
    timeElapsedCell = 'M' + c;
    timeCell = 'N' + c;
    sheet.getRange(avgCell).setValue(avg);
    sheet.getRange(maxCell).setValue(maxVal);
    sheet.getRange(stdDevCell).setValue(stdDev);
    sheet.getRange(timeElapsedCell).setValue(timeElapsed);
    sheet.getRange(timeCell).setValue(currentTime)
    c++;
    sheet.getRange('P2').setValue(c);
  }

}
