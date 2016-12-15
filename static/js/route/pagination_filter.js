$(function() {

// Search through Date
// filter all data logs
// paginate by 10

var $parentDiv = $(".main");
var $parentHeader = $(".page-header");
var $studentSearch = $("<div class='student-search'></div>");

var dataItems = $(".tr_parent tr");
var studentDetails = $(".student-details");
var perPage = 30;


//$('.page-header').append("<input placeholder='Search by date' id='inputSearch' type='text'>");

// pagination Btns
var $parentPagination = $("<div class='pagination'></div>");
var pageChild = $("<ul></ul>");

 $parentDiv.append($parentPagination);

// initilize the function
paginate(dataItems);

$(document).on("click", ".pagination li > a", function (event) {
   // Prevent to on top while clicking
   event.preventDefault();
   var currentActive = $(this).text();
   goToPage(currentActive, dataItems);

});

// bind search function to typing in search bar
$("#inputSearch").on("keyup", function() {

  //alert('hello');
  //search();
  $(".pagination").remove();
  $(".no-results").remove();

  var searchTerm = $("#inputSearch").val().toLowerCase();
  //console.log('hello', searchTerm);
     
  dataItems.hide();

  $("table td").each(function() {

    if ($(this).text().toLowerCase().match(searchTerm)) {
        $(this).parent().show();
    }
  });

  dataItems = $(".tr_parent tr:visible");
  console.log('test', dataItems.length);

  if (dataItems.length >= 0) {

    paginate(dataItems);

  }else {

      var noRecord = $('#inputSearch').val();
      $('.page-header').append("<div class='no-results'><h3>Sorry, there is no \"" + noRecord + "\" in the table. <button class='reset'>Reset </button></h3></div>");
      $('.reset').click(function() {location.reload();});

  }

});


// add page number links for each page and start off going to page 1
function paginate(dataItems) {

  var dataCounts = dataItems.length;
  var numLink = Math.ceil(dataCounts / perPage);

  if (numLink > 1) {

   
    $(".pagination").append("<ul></ul>");

    for (var i = 1; i <= numLink; i++) {

      $(".pagination").append("<li><a href='#'>" + i + "</a></li>");

    }
    goToPage(1, dataItems);
  }
}

// show just students on that page
function goToPage(pageNumber, studentListItems) {
  var startIndex = perPage * (pageNumber - 1);
  var endIndex = perPage * pageNumber;

  var studentsToShow = studentListItems.slice(startIndex, endIndex);

  studentListItems.hide();
  studentsToShow.fadeIn();

  //highlightSelectedPage(pageNumber);
  $(".pagination a").removeClass("active");
  $(".pagination a").eq(pageNumber - 1).addClass("active");
}

}); // end of wrapper
