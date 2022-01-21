
chrome.browserAction.onClicked.addListener(function buttonClicked(tab) {
    let msg = {
        txt: "hello"
    }
    chrome.tabs.sendMessage(tab.id, msg);

}

function buttonClicked(tab) {
    //console.log(tab);
    
}
