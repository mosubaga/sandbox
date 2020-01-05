////////////////////////////////////////

const axios   = require('axios');

////////////////////////////////////////

const g_URL = 'http://www.google.com' 

axios({
    method:'get',
    url:g_URL
})
.then((response) => {
        
        response.data.projects.forEach((project) =>{
            console.log(project.project_name);
            console.log(project.project_id);
            console.log("\n");
        });
    })
    .catch(error => {
        console.log(error);
    })

