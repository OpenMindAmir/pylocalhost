// In the name of Allah

var langs = ['','html','css','javascript','markdown','python','php']

var editor = CodeMirror.fromTextArea(document.getElementById('content'),{
    lineNumbers: true,
    theme: 'monokai',
    mode: langs[document.getElementById('type').options.selectedIndex]
});

document.getElementById('type').addEventListener('change',function () {
    editor.setOption('mode',langs[document.getElementById('type').options.selectedIndex])
});

switch (document.getElementById('name').value.split('.').pop()) {
    case 'js':
        editor.setOption('mode','javascript');
        document.querySelector('option[value=javascript]').setAttribute('selected',null);
        break;
    case 'html':
        editor.setOption('mode','htmlembedded');
        document.querySelector('option[value=htmlembedded]').setAttribute('selected',null);
        break;
    case 'htm':
        editor.setOption('mode','htmlembedded');
        document.querySelector('option[value=htmlembedded]').setAttribute('selected',null);
        break;
    case 'css':
        editor.setOption('mode','css');
        document.querySelector('option[value=css]').setAttribute('selected',null);
        break;
    case 'sass':
        editor.setOption('mode','css');
        document.querySelector('option[value=css]').setAttribute('selected',null);
        break;
    case 'scss':
        editor.setOption('mode','css');
        document.querySelector('option[value=css]').setAttribute('selected',null);
        break;
    case 'less':
        editor.setOption('mode','css');
        document.querySelector('option[value=css]').setAttribute('selected',null);
        break;
    case 'md':
        editor.setOption('mode','markdown');
        document.querySelector('option[value=markdown]').setAttribute('selected',null);
        break;
    case 'py':
        editor.setOption('mode','python');
        document.querySelector('option[value=python]').setAttribute('selected',null);
        break;
    case 'php':
        editor.setOption('mode','php');
        document.querySelector('option[value=php]').setAttribute('selected',null);
        break;
    default:
        editor.setOption('mode','');
}