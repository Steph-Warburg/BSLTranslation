document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('button').addEventListener('click',
    onclicked, false)

    function onclicked() {
        chrome.tabs.query({ currentWindow: true, active: true }, function (tabs) {
            chrome.tabs.sendMessage(tabs[0].id, 'on')
            }
        )
    }
}, false)