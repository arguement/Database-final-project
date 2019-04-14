new Vue({
    el:'#report',
    delimiters: ['[[',']]'],
    data: {
        start: '',
        end: '',
        top_sales_based_on_time: []
    },
    methods: {
        salesForSpecificFrame: function(){
            
        }
    },
    computed:{
        combine:function(){
            return this.start + this.end;
        }
    },
    watch:{
        combine: function (change) {
            self = this;
            if (this.end.length != 0 && this.start != 0){

            fetch(`/report/${this.start}/${this.end}`)
            .then(function(response) {

                return response.json();
             })
             .then(function(data) {
                 console.log(data)
                 self.top_sales_based_on_time = data;
                
             });
            }
        }
    }
});