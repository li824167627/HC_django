<template>
<el-row :gutter="4">
  <el-col :span="4">
    <div class="home">
    <el-select v-model="value" filterable placeholder="请选择">
      <el-option
        v-for="item in options"
        :key="item.fields.hostname"
        :label="item.fields.hostname"
        :value="item.fields.hostname">
      </el-option>
    </el-select>
    </div>
    <div class="block">
    <span class="demonstration">选择需要修改的时间</span>
    <el-date-picker
      v-model="value1"
      type="datetime"
      placeholder="选择日期时间"
      default-time="12:00:00">
    </el-date-picker>
  </div>
    </el-col>
  <el-col :span="2"><div class="home">
    <el-button type="primary" @click="cattime()" style="float:left; margin: 2px;">查询</el-button>
    <el-button type="primary" @click="updatetime()" style="float:left; margin: 2px;">修改</el-button>
  </div></el-col>
  <el-col :span="6"><div class="grid-content bg-purple"></div></el-col>
  <el-col :span="6"><div class="grid-content bg-purple"></div></el-col>
</el-row>
</template>



<script>
import axios from "axios";
export default {
  name: 'home',
  data () {
    return {
        options: [],
        value: '',
        value1: ''
    }
},
mounted: function () {
this.showhost()
},
change () {
this.$forceUpdate();
},
methods: {
showhost () {
    axios({
        methods: 'get',
        url:'/api/host',
    })
        .then((res) => {
            console.log('res===', res)
         if (res.data.respcode === '000000') {
            this.options = res.data['options']
         } else {
            this.$message.error('查询失败')
            console.log(res.data['respmsg'])
         }
        })
},
cattime () {
    this.$axios.post('/api/time_date',{hn:this.value})
    .then((res) => {
        // var res = JSON.parse(response.bodyText)
        if (res.data.respcode === '000000') {
        // console.log(res)
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
        this.$message.error('查询失败失败:'+res['respmsg'])
        // console.log(res['respmsg'])
        }
    })
},
updatetime() {
    this.$axios.post('/api/set_server_time',{hn:this.value,new_time:this.value1})
    .then((res) => {
        // var res = JSON.parse(response.bodyText)
        if (res.data.respcode === '000000') {
        // console.log(res)
        this.$alert(res.data, '当前服务器时间', {
            confirmButtonText: '确定',
            callback: action => {
                this.$message({
                    type: 'success',
                    message: res.data['message']
                });
            }
        });
        } else {
        this.$message.error('查询失败失败:'+res['respmsg'])
        // console.log(res['respmsg'])
        }
    })
}
}
}
</script>

<style scoped>
.demo-datetime-picker {
  display: flex;
  width: 100%;
  padding: 0;
  flex-wrap: wrap;
}
.demo-datetime-picker .block {
  padding: 30px 0;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
}
.demo-datetime-picker .block:last-child {
  border-right: none;
}
.demo-datetime-picker .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>
