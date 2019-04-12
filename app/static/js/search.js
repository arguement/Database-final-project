new Vue({
    el: "#search",
    data : {
        test: 'jordan',
        laptops: [],
        query: '',
        times: 0
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
          
           
        });
    },
    methods: {
        search: function(){
            console.log("jordan")
        fetch('/get_items')
        .then(function(response) {

           return response;
        })
        .then(function(data) {

           console.log(data);
           
        });
        },
        run: function(name){
            window.location.href = `/item_purchase/${name} `;
        },
        querys: function(){
            self = this;
            fetch(`/get_specific_item/${self.query}`)
        .then(function(response) {

           return response.json();
        })
        .then(function(data) {
            self.laptops = data
          
           
        });
        }
    }
});