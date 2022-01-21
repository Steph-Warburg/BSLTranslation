//checks whether extension is working
console.log('BSL Translation Extension');

chrome.runtime.onMessage.addListener(function (request) {
    //change to if overlay is already open 
    if (request == 'on') {
       /* function createDiv() {
            console.log('Interpreter box added');
            
        }*/

        alert(request)
    }
    //else if (request == 'off') { alert(request) }
    else console.log('Error')
})
