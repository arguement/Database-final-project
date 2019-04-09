new Vue({
    el: "#search",
    data : {
        test: 'jordan'
    },
    delimiters: ['[[',']]'],
    created: function(){
        console.log("jordan")
        fetch('/get_items')
        .then(function(response) {

           return response.json();
        })
        .then(function(data) {

           console.log(data);
           
        });
    },
    methods: {
        search: function(){
            console.log("jordan")
        fetch('/get_items')
        .then(function(response) {

           return response.json();
        })
        .then(function(data) {

           console.log(data);
           
        });
        }
    }
});