document
function console_control(evt,tabname){
    let tab_content, tab_links, i;

    // remove all elements from the cosole
    tab_content = document.getElementsByClassName("tab-content")
    for(i=0; i<tab_content.length; i++){
        tab_content[i].style.display = "none";
    }

    // Highlight the the current tab with a different color with the classname and styling 'active'
    tab_links = document.getElementsByClassName("tablinks");
    for (i = 0; i < tab_links.length; i++) {
    tab_links[i].className = tab_links[i].className.replace(" active", "");
    }
    
    // Select the content of the desired tab and display its content only
    document.getElementById(tabname).style.display = "block";
    evt.currentTarget.className += " active";
    console.log(evt.currentTarget.className)
}

