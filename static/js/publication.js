//
// require jquery
//
if (typeof jQuery === 'undefined') {
  alert('JPrints::Publication JavaScript requires jQuery')
  throw new Error('JPrints::Publication JavaScript requires jQuery')
}



//
// utility functions for contributor entry
//
function formContributorEntry(personid, pos, title, given, family, orcid ) {
	var entry = title+" "+given+" "+family+" ("+orcid+")";
	var p_hidden = '<input type="hidden" name="contrib_entry_p_'+pos+'" id="contrib_entry_p_'+pos+'" value='+pos+' />'
	var i_hidden = '<input type="hidden" name="contrib_entry_i_'+pos+'" id="contrib_entry_i_'+pos+'" value='+personid+' />'
	var t_hidden = '<input type="hidden" name="contrib_entry_t_'+pos+'" id="contrib_entry_t_'+pos+'" value='+title+' />'
	var g_hidden = '<input type="hidden" name="contrib_entry_g_'+pos+'" id="contrib_entry_g_'+pos+'" value='+given+' />'
	var f_hidden = '<input type="hidden" name="contrib_entry_f_'+pos+'" id="contrib_entry_f_'+pos+'" value='+family+' />'
	var o_hidden = '<input type="hidden" name="contrib_entry_o_'+pos+'" id="contrib_entry_o_'+pos+'" value='+orcid+' />'
	var newEntry = '<li id="contrib_entry_'+ pos +'" class="contributor">'+entry;
        newEntry += ' <button type="button" id="removeContrib_' + pos + '" class="btn-link remove-contributor" >';
        newEntry += '<span class="glyphicon glyphicon-remove-sign"></span></button>';
	newEntry += p_hidden;
	newEntry += i_hidden;
	newEntry += t_hidden;
	newEntry += g_hidden;
	newEntry += f_hidden;
	newEntry += o_hidden;
        newEntry += '</li>';

	var contribList = "#contribs_to_add";
	$(contribList).append(newEntry);
}

function updateContributorFields(pos) {

	$("#contrib_t").val("");
	$("#contrib_g").val("");
	$("#contrib_f").val("");
	$("#contrib_o").val("");
	$("#contribs_found").remove();

        $("#contrib_count").val(pos);  

        $('.remove-contributor').click(function(e){
            	e.preventDefault();
		var idParts = this.id.split("_");
		if ( idParts.length == 2 && null != idParts[1] ) {
                	var contribNum = idParts[1];
                	var fieldID = "#contrib_entry_" + contribNum;
                	$(this).remove();
                	$(fieldID).remove();
		}
	});
}

//
// add contributors manually
//
$(document).ready(function(){
    $(".add-contributor").click(function(e){
        e.preventDefault();
    	var count = $("#contrib_count").val();
	var tVal = $("#contrib_t").val();
	var gVal = $("#contrib_g").val();
	var fVal = $("#contrib_f").val();
	var oVal = $("#contrib_o").val();

	var entry = tVal+" "+gVal+" "+fVal+" ("+oVal+")";
	entry = entry.trim();
	if (  entry.length < 5 ) {
		return;
	}

	var next = Number(count) + 1;
	var pVal = next.toString();

	formContributorEntry(-1, pVal, tVal, gVal, fVal, oVal);
	updateContributorFields(pVal);

   });
    
});

//
// select contributor from ajax lookup list
//
$(document).on('click', ".sel-contributor", function(e){
        e.preventDefault();
    	var count = $("#contrib_count").val();
	var idParts = this.id.split("_");
	if ( idParts.length != 2 || null == idParts[1] ) {
		return;
	}
	var contribNum = idParts[1];
        var iFieldID = "#selectontrib_i_" + contribNum;
        var tFieldID = "#selectontrib_t_" + contribNum;
        var gFieldID = "#selectontrib_g_" + contribNum;
        var fFieldID = "#selectontrib_f_" + contribNum;
        var oFieldID = "#selectontrib_o_" + contribNum;

	var iVal = $(iFieldID).val();
	var tVal = $(tFieldID).val();
	var gVal = $(gFieldID).val();
	var fVal = $(fFieldID).val();
	var oVal = $(oFieldID).val();

	var entry = tVal+" "+gVal+" "+fVal+" ("+oVal+")";
	entry = entry.trim();
	if (  entry.length < 5 ) {
		return;
	}

	var next = Number(count) + 1;
	var pVal = next.toString();

	formContributorEntry(iVal, pVal, tVal, gVal, fVal, oVal);
	updateContributorFields(pVal);

    });
    

//
// contributor ajax lookup
//
$('.contrib_input').keyup(function(){

	$("#contribs_found").remove();
	var tVal = $("#contrib_t").val();
	var gVal = $("#contrib_g").val();
	var fVal = $("#contrib_f").val();
	var oVal = $("#contrib_o").val();
	
	var query_len =  gVal.length + fVal.length + oVal.length;
	if (  query_len < 3 ) {
		return;
	} 
	var query = {
		't': tVal,
		'g': gVal,
		'f': fVal,
		'o': oVal
	};
    	$.ajax({
		url: '/api/lookup/contrib/',
		data: query, 
		type: "GET",
		dataType: "json",
   	})
   	.done(function( json ) {
		$("#found_contribs_div").append('<ol id="contribs_found"></ol>');
		for (var i=0; i<json.people.length; i++) {
			var entry = json.people[i].title;
			entry = entry + " "+json.people[i].given;
			entry = entry + " "+json.people[i].family;
			entry = entry + " ("+json.people[i].orcid+")";
			var newEntry = '<li id="selectcontrib_'+ i +'" class="sel-contributor">'+entry;
        		//newEntry += ' <button id="selectcontrib_'+i+'" class="btn sel-contributor" type="button">+</button>';
        		newEntry += '</li>';
			var i_hidden = '<input type="hidden" id="selectontrib_i_'+i+'" value='+json.people[i].id+' />'
			var t_hidden = '<input type="hidden" id="selectontrib_t_'+i+'" value='+json.people[i].title+' />'
			var g_hidden = '<input type="hidden" id="selectontrib_g_'+i+'" value='+json.people[i].given+' />'
			var f_hidden = '<input type="hidden" id="selectontrib_f_'+i+'" value='+json.people[i].family+' />'
			var o_hidden = '<input type="hidden" id="selectontrib_o_'+i+'" value='+json.people[i].orcid+' />'
			$("#contribs_found").append(newEntry);
			$("#contribs_found").append(i_hidden);
			$("#contribs_found").append(t_hidden);
			$("#contribs_found").append(g_hidden);
			$("#contribs_found").append(f_hidden);
			$("#contribs_found").append(o_hidden);
		}
   	})
   	.fail(function( xhr, status, errorThrown ) {
		alert("contriblookup ERROR" + errorThrown);
   	});
});

//
// sort contributors toggle
//
$(document).ready(function(){
    $(".sort-contributors").click(function(e){
        e.preventDefault();
	var contribList = "#contribs_to_add";
	$(contribList).sortable({
		stop: function( event, ui ) {
			var sorted = $(contribList).sortable( "toArray" );
			var pos = 1;
			for (id in sorted) {
				if (sorted[id].match(/contrib_entry_\d+/)) {
					var idParts = sorted[id].split("_");
					var thePosId = "#contrib_entry_p_"+idParts[2];
					$(thePosId).val(pos);
					pos++;
				}
			}
		}
	});
	$(contribList).sortable( "option", "disabled", false );
	$(".sort-contributors").prop('disabled', true);
	$(".fix-contributors").prop('disabled', false);

    });
    
});

$(document).ready(function(){
    $(".fix-contributors").click(function(e){
        e.preventDefault();
	var contribList = "#contribs_to_add";
	$(contribList).sortable( "option", "disabled", true );
	$(".sort-contributors").prop('disabled', false);
	$(".fix-contributors").prop('disabled', true);

    });
    
});

//
// remove function (for existing contributors, new ones will see the dynamic one)
//
$(document).ready(function(){
	$('.remove-contributor').click(function(e){
        e.preventDefault();
	var idParts = this.id.split("_");
	if ( idParts.length == 2 && null != idParts[1] ) {
               	var contribNum = idParts[1];
               	var fieldID = "#contrib_entry_" + contribNum;
               	$(this).remove();
               	$(fieldID).remove();
	}
        });
}); 



//
// workflow accordian
//
$( function() {
    $( "#toggle" ).button().on( "click", function() {
      if ( $( "#accordion" ).accordion( "option", "icons" ) ) {
        $( "#accordion" ).accordion( "option", "icons", null );
      } else {
        $( "#accordion" ).accordion( "option", "icons", icons );
      }
    });
} );

$( function() {
    $( "#accordion" ).accordion( {
       heightStyle: "content"
    });
  } );
  


//
// example autocomplete with a fixed list of options
// 
$( function() {

    var availableTags = [
    "ActionScript",
    "AppleScript",
    "Asp",
    "Java",
    "JavaScript",
    "Python",
    "Ruby",
    "Scheme"
    ];
    $( "#autocomplete" ).autocomplete({
    source: availableTags
    });
} );

//
// Date Pickers for the publication dates
//
$(document).ready(function() {
    $( "#id_publication_date" ).datepicker({ dateFormat: 'yy-mm-dd'} );
});
$(document).ready(function() {
    $( "#id_online_date" ).datepicker({ dateFormat: 'yy-mm-dd'} );
});
$(document).ready(function() {
    $( "#id_accept_date" ).datepicker({ dateFormat: 'yy-mm-dd'} );
});
$(document).ready(function() {
    $( "#id_submit_date" ).datepicker({ dateFormat: 'yy-mm-dd'} );
});
$(document).ready(function() {
    $( "#id_complete_date" ).datepicker({ dateFormat: 'yy-mm-dd'} );
});


//
// ajax lookup for journal title - uses DOAJ 
//
$(document).ready(function() {
    $( "#id_journal" ).keyup(function(){

	$("#journals_found").remove();
	var jVal = $("#id_journal").val();
	if ( jVal.length < 3 ) {
		return;
	}
	var query = 'https://doaj.org/api/v1/search/journals/title%3A%22'+jVal+'%22';
	$.ajax({
		url: query,
		//data: jVal, 
		type: "GET",
		dataType: "json",
	})
	.done(function( json ) {
		if (json.results.length > 0 ) {
			$("#found_journals_div").append('<ol id="journals_found"></ol>');
			for (var i=0; i<json.results.length; i++) {
				var jentry = json.results[i];
				var entry = '<li id="journalentry_'+ i +'" class="sel-journal">'
				entry += jentry.bibjson.title+" "+jentry.bibjson.publisher;
				entry += "<br/>";
				var identifiers = jentry.bibjson.identifier;
				for (var j=0; j<identifiers.length; j++) {
					var ident = identifiers[j];
					var idType = ident.type;
					var idVal = ident.id;
					entry += idType+": "+idVal+"  ";
					var inputId = "selectjour_"+idType+"_"+i;
					var i_hidden = '<input type="hidden" id="'+inputId+'" value='+idVal+' />'
					$("#journals_found").append(i_hidden);
				}
				entry += '</li>';
				var j_hidden = '<input type="hidden" id="selectjour_j_'+i+'" value="'+encodeURIComponent(jentry.bibjson.title)+'" />'
				var p_hidden = '<input type="hidden" id="selectjour_p_'+i+'" value="'+encodeURIComponent(jentry.bibjson.publisher)+'" />'
				var c_hidden = '<input type="hidden" id="selectjour_c_'+i+'" value="'+jentry.bibjson.country+'" />'
				$("#journals_found").append(j_hidden);
				$("#journals_found").append(p_hidden);
				$("#journals_found").append(c_hidden);
				$("#journals_found").append(entry);
			}
		} else {
			//$("#found_journals_div").append('<span id="journals_found">no results found yet ...</span>');
		}
   	})
   	.fail(function( xhr, status, errorThrown ) {
		alert("DOAJ ERROR" + errorThrown);
   	});
    });
});

//
// select journal from ajax lookup list
//
$(document).on('click', ".sel-journal", function(e){
        e.preventDefault();
	var idParts = this.id.split("_");
	if ( idParts.length != 2 || null == idParts[1] ) {
		return;
	}
	var journalNum = idParts[1];
        var jFieldID = "#selectjour_j_" + journalNum;
        var pFieldID = "#selectjour_p_" + journalNum;
        var cFieldID = "#selectjour_c_" + journalNum;
        var ieFieldID = "#selectjour_eissn_" + journalNum;
        var ipFieldID = "#selectjour_pissn_" + journalNum;

	var jVal = $(jFieldID).val();
	var pVal = $(pFieldID).val();
	var cVal = $(cFieldID).val();
	var ieVal = $(ieFieldID).val();
	var ipVal = $(ipFieldID).val();

	$("#id_journal").val(decodeURIComponent(jVal));
	$("#id_publisher").val(decodeURIComponent(pVal));
	$("#id_place_of_pub").val(cVal);
	$("#id_issn_e").val(ieVal);
	$("#id_issn_p").val(ieVal);
	$("#journals_found").remove();

    });
    







