function read_message(event) {
    content = JSON.parse(event.data);
    switch (content.type) {
        case "pop-up":
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
    console.log("read_popup_message", data);
    pop_up_confirm(data.content, function() {
        if (data.callback) {
            window[data.callback]();
        }
    });
}

function read_toast_message(data) {
    // data
    console.log("read_toast_message", data);
    toast(data.type, data.content);
}

