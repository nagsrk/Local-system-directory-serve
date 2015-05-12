function execute(url){
  jQuery.ajax ({
    url: url,
    method: 'get',
    success: function(data){
      var log = data.log;
      log = log.replace(/\n/g, "<br>");
      $("#log-result").append(log);
      $("#log-result").html(log);
    },
  });
}
