/** Helper function to produce tooltipped FontAwesome icons. */
function fa(icon, tooltip, direction) {
  direction = direction || 'top';
  return `<i class="fas fa-${icon}" aria-hidden="true" data-toggle="tooltip" data-placement="${direction}" title="${tooltip}"/>`;
}

// Override default Quill icons
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

/** Quill blot model for content placeholders. */
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

/** Create a new Quill editor for a form field. */
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
      // Save old selection (text box is unfocused when modal shows)
      let selection = quill.getSelection(true);

      $("#embed-modal").modal('show');
      $("#embed-button").on('click', function () {
        // Find the dropdown for content in the modal
        let content = $("#embed-form").find("select[name=content]").val();

        if (content) {
          // Add the data to the Quill model
          quill.insertEmbed(selection.index, 'content-embed', content, Quill.sources.USER);

          // Preview the embedded data
          preview_embeds();
        }

        $("#embed-modal").modal('hide');

        // Restore old selection
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
    // Reload previewed content after Quill operations like undo, redo, etc.
    quill.on('text-change', preview_embeds);
  }

  return quill;
}

/** Load content placeholders in text with content previews using AJAX.
 *  This is the equivalent of expand_embeds() on the server-side, but works *as* you're editing content.
 */
function preview_embeds() {
  $("div.content-embed").each(function () {
    if (!$(this).data("previewing")) {
      $(this).data("previewing", "true");
      let contentId = $(this).data("content-id");
      let that = $(this);

      // Load a preview from the site using AJAX
      $.get(`/content/preview/${contentId}`, function (result) {
        // Strip whitespace in appropriate places so Quill doesn't insert extra newlines
        result = result.trim().replace(/>\s+/g, ">").replace(/\s+</g, "<");
        that.html(`<div class=\"card my-2\"><div class=\"card-body p-2\">${result}</div></div>`);
      });
    }
  });
}

/** Empty all content placeholders of previews. */
function unpreview_embeds() {
  $("div.content-embed").each(function () {
    $(this).removeData("previewing");
    $(this).empty();
  });
}