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

function connectSelectionCallback(table, callback, singleSelection){
    try {
	table.find('tbody').on( 'click', 'tr', function () {
	    if (singleSelection){
		clearTableSelection(table);
	    }
	    $(this).toggleClass('selected');
	    	if (callback !== undefined){
        		callback(this);
        	    }
        	} 
	);
    } catch (err) {
	console.log("could not connect selection callback");
    }

}