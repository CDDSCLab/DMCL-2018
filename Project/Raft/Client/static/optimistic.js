var index = 0
$('.watch').each(function(){
  index++
new Vue({
  el: this,
  data: {
    name: '',
    value: '',
    res :'',
    trans_id : index
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
      axios.get('http://127.0.0.1:5000/read?name='+this.name+'&id='+this.trans_id)
            .then(function(response){
              vm.value = _.capitalize(response.data)
              vm.res = 'the value is'+response.data
              console.log(response.data)
            })
            .catch(function (error){
              vm.res = 'No data '+vm.name
              vm.value = ''
            })
    },
      writeValue:function(){
      this.res = 'Waiting for server'
      var vm = this
      axios.get('http://127.0.0.1:5000/update?name='+this.name+'&value='+this.value+'&id='+this.trans_id)
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
      axios.get('http://127.0.0.1:5000/add?name='+this.name+'&value='+this.value+'&id='+this.trans_id)
            .then(function(response){
              vm.res = _.capitalize(response.data)
              console.log(response.data)
            })
            .catch(function (error){
              vm.res = 'Error'
            })
    },

    register:function(){
      this.res = 'Waiting for server'
      var vm = this
      axios.get('http://127.0.0.1:5000/register?id='+this.trans_id)
            .then(function(response){
              vm.res = _.capitalize(response.data)
              console.log(response.data)
            })
            .catch(function (error){
              vm.res = 'Error'
            })

    },

      submitTrans:function(){
      this.res = 'Waiting for server'
      var vm = this
      axios.get('http://127.0.0.1:5000/commit?id='+this.trans_id)
            .then(function(response){
              vm.res = _.capitalize(response.data)
              console.log(response.data)
            })
            .catch(function (error){
              vm.res = 'Error'
            })
    }
  }
})
})

