// __BEGIN_LICENSE__
//Copyright © 2015, United States Government, as represented by the 
//Administrator of the National Aeronautics and Space Administration. 
//All rights reserved.
//
//The xGDS platform is licensed under the Apache License, Version 2.0 
//(the "License"); you may not use this file except in compliance with the License. 
//You may obtain a copy of the License at 
//http://www.apache.org/licenses/LICENSE-2.0.
//
//Unless required by applicable law or agreed to in writing, software distributed 
//under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR 
//CONDITIONS OF ANY KIND, either express or implied. See the License for the 
//specific language governing permissions and limitations under the License.
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
        sScrollY:  calcDataTableHeight(),
        "lengthMenu": [[10, 20, 40, -1], [10, 20, 40, "All"]],
        "oLanguage": {
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