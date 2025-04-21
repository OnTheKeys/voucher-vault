function popup() {
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
        let activeTab = tabs[0];
        chrome.tabs.sendMessage(activeTab.id, {"message": "start"}, (response) =>{
            let newURL = "http://localhost:5173/form?cart=" + response[0] + "&price=" + response[1];
            chrome.tabs.create({ url: newURL });
            
        });
    });


    

}

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("Checkout").addEventListener("click", popup);
});