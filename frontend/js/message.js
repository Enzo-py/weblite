const ctx = {

}

function read_message(event) {
    content = JSON.parse(event.data);
    switch (content.type) {
        case "popup":
            read_popup_message(content.data);
            break;
        case "toast":
            read_toast_message(content.data);
            break;
        default:
            return content
    }

    return content
}

function read_popup_message(data) {
    // data
}

function read_toast_message(data) {
    // data
}

