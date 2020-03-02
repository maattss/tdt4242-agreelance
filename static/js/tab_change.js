$('#project-toggle a[data-toggle="list"]').on('shown.bs.tab', function (e) {
  $('#'+e.relatedTarget.id).removeClass('active') // previous active tab
})
