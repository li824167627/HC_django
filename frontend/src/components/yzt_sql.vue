<template>
    <div class="yzt">

    <el-input v-model="input" placeholder="请输入手机号" style="display:inline-table; width: 30%; float:left"></el-input>
    <el-button type="primary" @click="query_sql_yzt()" style="float:left; margin: 2px;">查询</el-button>
    </div>
    </template>

    <script>
        export default {
          name: 'yzt',
          data () {
            return {
                input: '',
            }
        },
          methods: {
            query_sql_yzt () {
              this.$axios.get('/api/query_sql?phone=' + this.input)
                .then((res) => {
                  // var res = JSON.parse(response.bodyText)
                  if (res.data.respcode === '000000') {
                    // console.log(res)
                    this.$alert(`预客户号为：${res.data[0][1]}<br/>客户号为：${res.data[0][2]}`, '一账通查询结果', {
                        confirmButtonText: '确定',
                        dangerouslyUseHTMLString: true,
                        callback: action => {
                            this.$message({
                                type: 'success',
                                message: `查询成功`
                            });
                        }
                    });
                  } else {
                    this.$message.error('查询失败失败，请重试')
                    // console.log(res['respmsg'])
                  }
                })
            }
          }
        }
    </script>
