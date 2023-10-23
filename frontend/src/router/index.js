import Vue from 'vue'
import Router from 'vue-router'
import home from "../components/home";
import charm from "../components/charm";
import time from "../components/time";
import hostinfo from "../components/hostinfo";
import yzt_sql from "../components/yzt_sql";
import examine from "../components/examine";

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: home
    },
    {
      path: '/charm',
      name: 'charm',
      component: charm
    },
    {
      path: '/time',
      name: 'time',
      component: time
    },
    {
      path: '/hostinfo',
      name: 'hostinfo',
      component: hostinfo
    },
    {
      path: '/query_sql_zyt',
      name: 'query_sql_zyt',
      component: yzt_sql
    },
    {
      path: '/examine',
      name: 'examine',
      component: examine
    }
  ]
})
