<template>
<div class="home">
<el-input v-model="input" placeholder="请输入地址" style="display:inline-table; width: 30%; float:left"></el-input>
<el-button type="primary" @click="cattime()" style="float:left; margin: 2px;">查询</el-button>
</div>
</template>

<script>
    export default {
      name: 'home',
      data () {
        return {
            input: '',
        }
    },
      methods: {
        cattime () {
          this.$axios.get('/api/show_time?show_time=' + this.input)
            .then((response) => {
              var res = JSON.parse(response.bodyText)
              if (res.respcode === '000000') {
                console.log(res)
                this.$alert(res.data, '当前服务器时间', {
                    confirmButtonText: '确定',
                    callback: action => {
                        this.$message({
                            type: 'success',
                            message: `查询成功`
                        });
                    }
                });
              } else {
                this.$message.error('查询失败失败，请重试')
                console.log(res['respmsg'])
              }
            })
        }
      }
    }
</script>
