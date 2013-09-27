window.onload=pageonload;
url='ajaxserver'

function pageonload(event){
    Event.observe($('btFetchWeather'),'click',fetchweather);
    $('spinner').style.visibility="hidden";

}

function fetchweather(event){
    $('spinner').style.visibility="visible";
    param=$H({ // All these values are dependent on the backend server...
 	a: 'tempdata'
	,pos: $('inpLocation').value
	,time: $('inpTime').value
	,date: $('inpDate').value
	,sender: event.element().id
    });
    ajax=new Ajax.Request(url,
			  {method:'get',
			   parameters: param.toQueryString(),
			   onComplete: hHR_receiveddata}
			 );
}


function hHR_receiveddata(response,json){ // The response function to the ajax call
    if(Object.inspect(json)){
	jsondata=response.responseText.evalJSON();
	if(jsondata.error>''){
	    $('error').innerHTML=jsondata.error;
	}
    }
    $('result').innerHTML=jsondata.temp+"&deg;C "+jsondata.cloudiness+"% cloud";
     $('spinner').style.visibility="hidden";
    
}
