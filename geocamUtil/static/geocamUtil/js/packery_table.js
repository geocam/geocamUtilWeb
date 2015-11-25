function updateTableScrollY(divID, tableID) {
    var divItem = $('#' + divID);
    var parentHeight = divItem.height();
    divItem.find('.dataTables_scrollBody').height(parentHeight-110);
    theDataTable.fnAdjustColumnSizing();
}

/* 
 * Table View
 */
function setupTable(divID, tableID, initialData, aoColumns){
	// initialize the table with json of existing data.
	defaultOptions["aaData"] = initialData;
	defaultOptions["aoColumns"] = aoColumns;
	defaultOptions["scrollY"] = 200;

	if ( ! $.fn.DataTable.isDataTable( '#' + tableID ) ) {
		  theDataTable = $('#' + tableID ).dataTable(defaultOptions);
	}
	
	// handle resizing
	var tableResizeTimeout;
	$('#' + divID).resize(function() {
	    // debounce
	    if ( tableResizeTimeout ) {
		clearTimeout( tableResizeTimeout );
	    }

	    tableResizeTimeout = setTimeout( function() {
		updateTableScrollY(divID, tableID);
	    }, 30 );
	});
	
}