<script>
var list=document.getElementsByTagName("tbody")[1];
var length = list.getElementsByTagName("tr").length - 3;
var startLine = 2;
var i = 0;

var buildId = ${ENV:BUILD_ID};
var buildIdInt = parseInt(buildId);
function callServer() {	
	var xmlHttp;
	if(window.ActiveXObject)
        xmlHttp =new ActiveXObject("Microsoft.XMLHTTP");
    else if(window.XMLHttpRequest)   
        xmlHttp=new XMLHttpRequest();   
	var baseUrl = document.URL
    var url = baseUrl.substring(0, baseUrl.lastIndexOf("/") + 1) + buildIdInt + "/api/xml?pretty=true&tree=actions[parameters[*],causes[*]]";
	
	xmlHttp.open("GET",url,true);   
	xmlHttp.onreadystatechange = function(){
		if(xmlHttp.readyState==4 && xmlHttp.status==200 && i < length) {
			var branch_name = xmlHttp.responseXML.getElementsByTagName("parameter")[1].getElementsByTagName("value")[0].firstChild.nodeValue;
			var user_name = xmlHttp.responseXML.getElementsByTagName("cause")[0].getElementsByTagName("userName")[0].firstChild.nodeValue;
			var lineContent1, lineContent2;
			if(branch_name=="trunk") {
				lineContent1 = "　　trunk发布";
				lineContent2 = ""
			}
			else {
				lineContent1 = "　　branch_name=" + branch_name
				lineContent2 = "　　btag=b_" + buildIdInt + "_" + user_name;
			}
			buildIdInt--;
			var textnode1 =document.createTextNode(lineContent1);
			var textnode2 =document.createTextNode(lineContent2);
			var textnode3 =document.createTextNode("　");
			var newDiv1=document.createElement("DIV");
			var newDiv2=document.createElement("DIV");
			var newDiv3=document.createElement("DIV");
			newDiv1.appendChild(textnode1);
			newDiv2.appendChild(textnode2);
			newDiv3.appendChild(textnode3);
			var newTd=document.createElement("TD");
			newTd.appendChild(newDiv1);
			newTd.appendChild(newDiv2);
			newTd.appendChild(newDiv3);
			
			var newTr=document.createElement("TR");
			newTr.appendChild(newTd);
			list.insertBefore(newTr,list.children[i*2 + startLine]);
			i++;
			callServer();
		}
	};
	xmlHttp.send(null);   
}
callServer();

</script>