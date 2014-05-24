%include header name=name
<body class="edit">
%include header_bar name=name, type=type
<div class='j-preview preview'>
     <iframe class='j-preview-frame' src="{{name}}.__preview__">
     </iframe>
</div>
<div class='j-editor editor'>
    <form name="page_edit" method="post" class="edit_form" accept-charset="UTF-8">
        <textarea id="new_content" name="new_content" cols="80" rows="40" class="textcontent">{{content}}</textarea>
        <textarea id="old_content" name="old_content" style="display: none">{{content}}</textarea>
    </form>
</div>
</body>
</html>
