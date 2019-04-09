new Vue({
    el: "#search",
    data : {
        test: 'jordan',
        laptops: []
    },
    delimiters: ['[[',']]'],
    created: function(){
        self = this
        console.log("jordan")
        fetch('/get_items')
        .then(function(response) {

           return response.json();
        })
        .then(function(data) {
            self.laptops = data
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