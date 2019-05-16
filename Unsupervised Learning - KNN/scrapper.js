var y = $("tr.even td").each(function(co){co.innerText});
var x = $("tr.odd td").each(function(co){co.innerText});

for(var i=0;i<y.length;i++){
	try {
		console.log(" , "+y[i*8+1].innerText+" , "+y[i*8+6].innerText);
	}
	catch(err) {
	} 
	}
	
for(i=0;i<x.length;i++){
	try {
		console.log(" , "+x[i*8+1].innerText+" , "+x[i*8+6].innerText);
	}
	catch(err) {
	} 
	
    }

