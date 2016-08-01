// __BEGIN_LICENSE__
//Copyright (c) 2015, United States Government, as represented by the 
//Administrator of the National Aeronautics and Space Administration. 
//All rights reserved.
// __END_LICENSE__

/*
 * Utilities to make using datatable easier
 * Import it of course
 * <script language="javascript" type="text/javascript" src="{{ STATIC_URL }}geocamUtil/js/datatable_helpers.js"></script>
 *
 */

/* put something like this in your document ready function: 
 * 
         defaultOptions['aoColumnDefs'] = [
                                              {
                                                  aTargets: ['name'],
                                                  sWidth: '285px',
                                              },
                                              {
                                                  aTargets: ['xls','kml', 'detail_doc', ''],
                                                  bSortable: false,
                                              },
                                          ];
            defaultOptions['order'] =  [[ 5, "desc" ]];


        var planTable = $('#planTable').dataTable(defaultOptions);
        $(window).resize(function(){ planTable.fnAdjustColumnSizing(); });
        initializeCheckbox();
     }));
 */
heightPercentage = 60;
/*
 * Change height percentage if you need a different size table
 */
calcDataTableHeight = function() {
    var h =  Math.floor($(window).height()*heightPercentage/100);
    return h + 'px';
};

/*
 * You will probably want to append things to the default options, for example:
 * defaultOptions['name'] = value;
 * defaultOptions['aoColumnDefs'] = [
            {
                aTargets: ['name'],
                sWidth: '285px',
            },
            {
                aTargets: ['xls','kml', 'detail_doc', ''],
                bSortable: false,
            },
        ]
 */
defaultOptions = {
        bAutoWidth: true,
        stateSave: true,
        bPaginate: true,
        iDisplayLength: -1, 
        bLengthChange: true,
        select: true,
        bSort: true,
        bJQueryUI: false,
        scrollY:  calcDataTableHeight(),
        lengthMenu: [[10, 20, 40, -1], [10, 20, 40, "All"]],
        oLanguage: {
            "sLengthMenu": "Display _MENU_"
        }
};

/*
 * Initialize the pick_master checkbox to check all checkboxes.
 */
initializeCheckbox = function() {
    if ($('#pick_master').length >= 0) {
        $('#pick_master').val($(this).is(':checked'));
    
        $('#pick_master').change(function() {
                var masterChecked = $(this).is(":checked");
                $('.check').each(function(i, obj) {
                 $(this).prop("checked", masterChecked);
                });
        });
    }
};

/* 
 * Disable changing the length of the table, disable searching
 */
disableLimitSearch = function() {
    defaultOptions['bLengthChange'] = false;
    defaultOptions['bFilter'] = false;
    defaultOptions['bInfo'] = false;
}

/* Get the rows which are currently selected */
function getSelectedRows( table ) {
    return table.find('tr.selected');
}		  

function clearTableSelection(table){
    getSelectedRows(table).removeClass('selected');
}

function selectRow(table, rowId){
    var identifier = 'tr#' + rowId;
    table.find(identifier).addClass('selected');
}

function ensureSelectedRow(table, rowId){
    var identifier = 'tr#' + rowId;
    var row = table.find(identifier);
    if (!row.hasClass('selected')){
	row.addClass('selected');
    }
}

function connectSelectionCallback(table, callback, singleSelection, context){
    try {
    	var dt = table.DataTable();
    	dt.on( 'select', function ( e, dt, type, indexes ) {
    	    if ( type === 'row' ) {
    	    	for (var i=0; i<indexes.length; i++){
    	    		callback(indexes[i], dt.row(indexes[i]).data(), context);
    	    	}
    	    }
    	} );
    	
    } catch (err) {
    	console.log("could not connect selection callback");
    }
}

/* 
 * Table View
 */
function setupTable(divID, tableID, initialData, aoColumns){
	// initialize the table with json of existing data.
	defaultOptions["aaData"] = initialData;
	defaultOptions["aoColumns"] = aoColumns;
	defaultOptions["scrollY"] = 200;
	defaultOptions["fnCreatedRow"] = function(nRow, aData, iDataIndex) { // add image id to row
		$(nRow).attr('id', aData['id'])
	}
	
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