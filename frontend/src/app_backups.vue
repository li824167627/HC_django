<template>
    <el-container>
      <el-header>
      <div id="app">
        <img src="./assets/logo.png">
      </div>
      </el-header>
      <el-main>
        <div id="app">
          <router-view/>
        </div>
      </el-main>
      <el-aside>
    
      </el-aside>
      <el-footer>
        
      </el-footer>
    </el-container>
    </template>
    <script>
    export default {
      name: 'App'
    }
    </script>
    
    <style>
    #app {
      font-family: 'Avenir', Helvetica, Arial, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
      text-align: center;
      color: #2c3e50;
      margin-top: 60px;
    }
    </style>
    