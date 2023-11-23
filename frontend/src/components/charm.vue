<template>
<div class="home">
<el-row display="margin-top:10px">
<el-input v-model="input" placeholder="请输入订单号" style="display:inline-table; width: 30%; float:left"></el-input>
<el-button type="primary" @click="addbook()" style="float:left; margin: 2px;">新增</el-button>
</el-row>
  <el-table
    :data="booklist.filter(data => !search || data.fields.loan_request_no.toLowerCase().includes(search.toLowerCase()))"
    style="width: 100%">
    <el-table-column
      label="编号"
      prop="id"
      min-width="100">
      <template slot-scope="scope"> {{ scope.$index+1 }} </template>
    </el-table-column>
    <el-table-column
      label="订单号"
      prop="loan_request_no"
      min-width="100">
      <template slot-scope="scope"> {{ scope.row.fields.loan_request_no }} </template>
    </el-table-column>
    <el-table-column
      label="状态"
      prop="payment_status"
      min-width="100">
      <template slot-scope="scope"> {{ scope.row.fields.payment_status }} </template>
    </el-table-column>
    <el-table-column
      align="right">
      <template slot="header" slot-scope="scope">
        <el-input
          v-model="search"
          size="mini"
          placeholder="输入关键字搜索"/>
      </template>
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="handleEdit(scope.$index, scope.row.pk)">编辑</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row.pk)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>


</div>
</template>

<script>
import axios from "axios";

export default {
  name: 'home',
  data () {
    return {
      input: '',
      search: '',
      booklist: []
    }
  },
  mounted: function () {
    this.showbooks()
  },
  change () {
    this.$forceUpdate();
  },
  methods: {
    addbook () {
      this.$axios.get('/api/add_book?loan_request_no=' + this.input)
        .then((res) => {
          //var res = JSON.parse(response.bodyText)
          if (res.data.respcode === '000000') {
            this.showbooks()
          } else if (res.data.respcode === '666666'){
            this.$message.error(res.data['respmsg'])
          }else {
            this.$message.error('新增书籍失败，请重试')
            console.log(res['respmsg'])
          }
        })
    },
    showbooks () {
      axios({
        methods:'get',
        url:'/api/show_books',
      })

      // this.$http.get('http://127.0.0.1:8000/api/show_books/')
        .then((res) => {
          // console.log('response====', response)
          // var res = JSON.parse(response.bodyText)
            console.log('res===', res)
          if (res.data.respcode === '000000') {
            this.booklist = res.data['list']
          } else {
            this.$message.error('查询书籍失败')
            console.log(res.data['respmsg'])
          }
        })
    },
    handleDelete(index, row) {
      console.log('删除数据的id = '+ index,row)
      this.$confirm("确定删除?", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
      // 确认删除
        .then(() => {
        //删除接口只需要传个id就行了 id是当前点击事件传过来的的id
          this.$axios.post('/api/del_books', {pk:row})
            .then((res) => {
              // var res = JSON.parse(response.bodyText)
            if (res.data.respcode == '000000') {
              this.showbooks()
              this.$message.success("删除成功");
            } else {
              this.$message.error('删除书籍失败，请重试');
            }
          });
        })
        //取消删除
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消删除",
          });
        });
    },
    handleEdit(index, row) {
      this.$prompt('重新输入书名', '编辑', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
        //确认修改
        }).then(({ value }) => {
        //修改接口需要传个id和bookname
          console.log('获取输入的值='+value)
          this.$axios.post('/api/edit_books', {pk:row,loan_request_no:value})
            .then((res) => {
              // var res = JSON.parse(response.bodyText)
            if (res.data.respcode == '000000') {
              this.showbooks()
              this.$message.success("修改成功");
            } else {
              this.$message.error('修改书名失败，请重试');
            }
          });
        })
        //取消修改
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消修改",
          });
        });
    },

  }
}
</script>

<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}
</style>
