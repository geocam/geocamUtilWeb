// __BEGIN_LICENSE__
// Copyright (C) 2008-2010 United States Government as represented by
// the Administrator of the National Aeronautics and Space Administration.
// All Rights Reserved.
// __END_LICENSE__

var TOC = {
    load: function () {
        $('#toc_button').click(TOC.toggle);
    },
    
    toggle: function () {
        if ($('#sphinxsidebar').toggle().is(':hidden')) {
            $('div.document').css('left', "0px");
            $('toc_button').removeClass("open");
        } else {
            $('div.document').css('left', "230px");
            $('#toc_button').addClass("open");
        }
        return $('#sphinxsidebar');
    }
};

$(document).ready(function () {
    TOC.load();
});
