<div class="header header_{{type}}">
    <div class="text">
         % if defined('meta') and meta:
            [<a href="{{meta}}">i</a>]:
         % end
         <a href="/">watom</a>:
         % if defined('breadcrumbs'):
            % for item in breadcrumbs[:-1]:
               <a href="{{item[1]}}">{{item[0]}}</a>:
            % end
            % if len(breadcrumbs) > 0:
                {{breadcrumbs[-1][0]}}
            % end
         % end
    </div>

    <div class="buttons">
        %if type == 'edit':
            <a href="#" id="btn_save">save</a>
        %else:
            %if not name.startswith('__'):
                <a href="{{name}}.__edit__" id="btn_edit">edit</a>
            %end
        %end
    </div>
</div>
