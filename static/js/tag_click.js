$('#tags a[data-toggle="tag"]').on('click', function (e) {
    console.log(e);
    e.target.addClass("primary");
    // $('#'+e.relatedTarget.id).removeClass('active') // previous active tag
  })
  