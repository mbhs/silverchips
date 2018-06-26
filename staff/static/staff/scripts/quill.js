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
let BlockEmbed = Quill.import('blots/block/embed');

class ContentBlot extends BlockEmbed {
  static create(contentId) {
    let node = super.create();
    node.setAttribute("class", "content-embed");
    node.setAttribute("data-content-id", contentId);
    return node;
  }

  static value(node) {
    return node.getAttribute("data-content-id");
  }
}
ContentBlot.blotName = 'content-embed';
ContentBlot.tagName = 'div';

Quill.register(ContentBlot);

/** Create a new Quill editor for an element. */
function quill(name, short, embed) {
  let toolbar = { container: [
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

  let quill;

  if (embed) {
    toolbar.container.push(['embed']);
    toolbar.handlers.embed = function() {
      let selection = quill.getSelection(true);

      $("#embed-modal").modal('show');
      $("#embed-button").on('click', function() {
        let content = $("#embed-form").find("select[name=content]").val();

        if (content) {
          quill.insertText(selection.index, '\n', Quill.sources.USER);
          quill.insertEmbed(selection.index + 1, 'content-embed', content, Quill.sources.USER);
          quill.insertText(selection.index + 2, '\n', Quill.sources.SILENT);
          preview_embeds();
        }

        $("#embed-modal").modal('hide');
        quill.setSelection(selection);
      });
    };
  }

  quill = new Quill(`#${name}-editor`, {
    theme: "snow",
    modules: {
      toolbar: toolbar
    }
  });

  if (embed) {
    quill.on('text-change', preview_embeds);
  }

  return quill;
}

function preview_embeds() {
  $("div.content-embed[data-previewing!='true']").each(function () {
    $(this).data("previewing", "true");
    let contentId = $(this).data("content-id");
    let that = $(this);
    $.get(`/content/embed/${contentId}`, function (result) {
      console.log(result.replace(/\n+/g, ''));
      that.html("<div class=\"card\"><div class=\"card-body\">" + result.replace(/\n+/g, '') + "</div></div>");
    });
  });
}

function unpreview_embeds() {
  $("div.content-embed").each(function (index, element) {
    $(this).removeData("previewing");
    $(this).empty();
  });
}