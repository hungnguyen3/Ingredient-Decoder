const port1 = process.env.PORT || 3000; 

const {app} = require("./backend");

var server_get_data = app.listen(port1, function(){ // listen to the port
    var port = server_get_data.address().port;
    console.log("Listening at %s", port); 
});

// file to run backend