function fa(icon, tooltip, direction) {
  direction = direction || 'top';
  return `<i class="fas fa-${icon}" aria-hidden="true" data-toggle="tooltip" data-placement="${direction}" title="${tooltip}"/>`;
}

/** Override default Quill icons */
var icons = Quill.import('ui/icons');
icons['bold'] = fa('bold', 'Bold');
icons['italic'] = fa('italic', 'Italicize');
icons['underline'] = fa('underline', 'Underline');
icons['strike'] = fa('strikethrough', 'Strikethrough');
icons['list'] = { 'ordered': fa('list-ol', 'Insert number list'), 'bullet': fa('list-ul', 'Insert bullet list') };
icons['link'] = fa('link', 'Insert link');
icons['indent'] = { '+1': fa('indent', 'Increase indent'), '-1': fa('outdent', 'Decrease indent') };
icons['align'] = { '': fa('align-left', 'Align left', 'right'), 'right': fa('align-right', 'Align right', 'right'),
                    'justify': fa('align-justify', 'Justify', 'right'), 'center': fa('align-center', 'Align center', 'right') };
icons['embed'] = fa('plus-circle', 'Embed content');

// TODO: add tooltips and fontawesome icons for color styling
// TODO: customize fonts and sizes

//class ContentBlot extends BlockEmbed {
//  static create(id) {
//    let node = super.create();
//    node.setAttribute("src", id);
//    return node;
//  }
//
//  static value(domNode) {
//    return domNode.getAttribute("src");
//  }
//}
//ContentBlot.blotName = 'content';
//ContentBlot.tagName = 'div';
//ContentBlot.className = 'content';

/** Create a new Quill editor for an element. */
function quill(id, short, embed) {
  var toolbar = { container: [
      ['bold', 'italic', 'underline', 'strike']
  ], handlers: { } };

  if (!short) {
    toolbar.container.push(...[
      [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
      ['link'],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'indent': '-1'}, { 'indent': '+1' }],
      [{ 'color': [] }, { 'background': [] }],
      [{ 'align': [] }],
      ['clean']
    ]);
  }

  if (embed) {
    toolbar.container.push(['embed']);
    toolbar.handlers.embed = function() {
      this.quill.insertEmbed(this.quill.getSelection().index, 'image', 'https://quilljs.com/images/cloud.png');
    };
  }

  return new Quill(id, {
    theme: "snow",
    modules: {
      toolbar: toolbar
    }
  });
}