<template>
<div class="examine">
<el-input v-model="input" placeholder="请输入订单号" style="display:inline-table; width: 30%; float:left"></el-input>
<el-button type="primary" @click="cattime()" style="float:left; margin: 2px;">审批</el-button>
</div> 
</template>
    
<script> 
    export default {
      name: 'examine',
      data () {
        return {
            input: '',
        }
    },
      methods: {
        cattime () {
          this.$http.get('http://127.0.0.1:8000/api/examine?order_no=' + this.input)
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.respcode === '000000') {
                console.log(res)
                this.$message({
                    type: 'success',
                    message: `渤海合同上传完成`
                  });
              } else {
                this.$message.error('上传失败，请重试')
                console.log(res['respmsg'])
              }
            })
        }  
      }
    }
</script>
    