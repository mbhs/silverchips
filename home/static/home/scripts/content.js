function lightboxShow(contentId) {
  $("#lightboxModalTitle").html($("#lightboxTitle-" + contentId).html());
  $("#lightboxModalBody").html($("#lightboxContent-" + contentId).html());
  $("#lightboxModalFooter").html($("#lightboxCaption-" + contentId).html());
  $("#lightboxModalDialog").css("max-width", $("#lightboxContent-" + contentId).width());
  $("#lightboxModalDialog").css("max-height", $("#lightboxContent-" + contentId).height());
  $("#lightboxModal").modal("show");
}

function galleryShow(galleryId, index) {
  let gallery = $("#gallery-" + galleryId);
  gallery.data("current-index", index);

  gallery.find(".gallery-entry").css("display", "none");
  gallery.find(`[data-gallery-entry-index='${index}']`).css("display", "block");
  gallery.find(".gallery-item-counter").html(index);

  gallery.find(".gallery-left-button").toggleClass("disabled", index === 1);
  gallery.find(".gallery-right-button").toggleClass("disabled", index === gallery.data("total-entries"));
}

function galleryMove(galleryId, delta) {
  const gallery = $("#gallery-" + galleryId);
  galleryShow(galleryId, gallery.data("current-index") + delta);
}