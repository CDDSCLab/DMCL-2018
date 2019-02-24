
$('.watch').each(function(){
new Vue({
  el: this,
  data: {
    name: '',
    value: '',
    res :'',
    tableID:'',
    item: {
                timestamp: '0',
                client: '',
                term: '',
                data: ''
            },
     logs: [{"timestamp": "2019-01-22 14:17:17.748997", "term": 0, "client": "8002", "data": "Start"},
      {"timestamp": "2019-01-22 14:17:21.457354", "term": 1, "client": 0, "data": "000"}]
  },
  // watch: {
  //   // 如果 `question` 发生改变，这个函数就会运行
  //   name: function (newQuestion, oldQuestion) {
  //     this.value = 'Waiting for you to stop typing...'
  //     this.debouncedGetAnswer()
  //   }
  // },
  created: function () {
    // `_.debounce` 是一个通过 Lodash 限制操作频率的函数。
    // 在这个例子中，我们希望限制访问 yesno.wtf/api 的频率
    // AJAX 请求直到用户输入完毕才会发出。想要了解更多关于
    // `_.debounce` 函数 (及其近亲 `_.throttle`) 的知识，
    // 请参考：https://lodash.com/docs#debounce
    this.debouncedGetAnswer = _.debounce(this.getAnswer, 500)
  },
  methods: {
    getAnswer: function () {
      if (this.name.indexOf('?') === -1) {
        this.value = 'Questions usually contain a question mark. ;-)'
        return
      }
      this.value = 'Thinking...'
      var vm = this
      axios.get('https://yesno.wtf/api')
        .then(function (response) {
          vm.value = _.capitalize(response.data.value)
        })
        .catch(function (error) {
          vm.res = 'Error! Could not reach the API. ' + error
        })
    },
    getValue:function(){
      this.res = 'Waiting for server'
      var vm = this
      axios.get('http://127.0.0.1:5000/getNodeData/'+this.tableID)
            .then(function(response){
                = _.capitalize(response.data)
              vm.res = 'the value is'+response.data
              vm.logs = response.data
              console.log(response.data)
            })
            .catch(function (error){
              vm.res = 'No data '+vm.name
              vm.value = ''
              vm.logs = []
            })
    },
    writeValue:function(){
      this.res = 'Waiting for server'
      var vm = this
      axios.get('http://127.0.0.1:5000/addValue/'+this.value)
            .then(function(response){
              vm.res = _.capitalize(response.data)
            })
            .catch(function (error){
              vm.res = 'Error'
            })
    },
      addValue:function(){
      this.res = 'Waiting for server'
      var vm = this
      axios.get('http://127.0.0.1:5000/addbylock?name='+this.name+'&value='+this.value)
            .then(function(response){
              vm.res = _.capitalize(response.data)
              console.log(response.data)
            })
            .catch(function (error){
              vm.res = 'Error'
            })
    },
  }
})
})

