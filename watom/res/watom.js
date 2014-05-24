(function() {
    var oldSavedVersion = null,
        timerId;

    function hasClass(ele,cls) {
        return ele.className.match(new RegExp('(\\s|^)'+cls+'(\\s|$)'));
    }

    function addClass(ele,cls) {
        if (!hasClass(ele,cls)) ele.className += " "+cls;
    }

    function removeClass(ele,cls) {
        if (hasClass(ele,cls)) {
            var reg = new RegExp('(\\s|^)'+cls+'(\\s|$)');
            ele.className=ele.className.replace(reg,' ');
        }
    }

    function quickSave()
    {
        if(document.forms['page_edit']['new_content'].value == document.forms['page_edit']['old_content'].value)
           return;

        var httpRequest;
        httpRequest = new XMLHttpRequest();
        httpRequest.onreadystatechange = function(){handleResponse(httpRequest)};
        httpRequest.open('PUT', '', true);

        // change the color of 'save' button
        addClass(document.getElementById("btn_save"), 'saving');

        httpRequest.setRequestHeader("Content-Type", "text/plain; charset=UTF-8");
        httpRequest.send(JSON.stringify({
            new_content: document.forms['page_edit']['new_content'].value,
            old_content: document.forms['page_edit']['old_content'].value
        }));
    }


    function handleResponse(response)
    {
        var previewFrame = document.querySelectorAll('.j-preview-frame')[0],
            data;
        previewFrame.contentWindow.location.reload();

        if(response.readyState == 4) {
            if(response.status == 200) {
                data = JSON.parse(response.response);
                document.forms['page_edit']['old_content'].value = data['updated_content'];
                if(data['result'] == 'CONFLICTED')
                    document.forms['page_edit']['new_content'].value = data['updated_content'];
                // small trick to actually see the saving: wait for more 500ms
                setTimeout(resetSaveStatus, 500);
            }
        }
    }

    function resetSaveStatus()
    {
        removeClass(document.getElementById("btn_save"), 'saving');
    }

    this.automatic_save = function()
    {
        if (timerId !== null)
           clearTimeout(timerId);

        timerId = setTimeout(function(){
                timerId = null;
                quickSave();
        }, 2000);
    }

    this.save = function()
    {
        document.forms['page_edit'].submit();
    }

    this.disable_links = function()
    {
        var links = document.querySelectorAll('.j-preview-frame')[0].contentDocument.querySelectorAll('a'),
            i;
        for(i = 0; i < links.length; ++i)
            links[i].addEventListener('click', function(event){
             event.preventDefault();
              });
    }

    window.onload = function() {
        if(document.forms['page_edit']) {
            document.forms['page_edit']['new_content'].addEventListener('input', automatic_save);
            document.getElementById("btn_save").addEventListener('click', save);
            document.querySelectorAll('.j-preview-frame')[0].onload = function(){ disable_links(); };
            disable_links();
        }
    };
}).call(this);