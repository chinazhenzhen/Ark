// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from './App'
import router from './router'
import AtComponents from 'at-ui'
import 'at-ui-style'

Vue.config.productionTip = false
Vue.use(AtComponents)

/* eslint-disable no-new */
/* 将App.vue 放到#app中 */
/* 相当于一个总的入口，在index.html中<app></app>使用这个vue app(开发过程中不用改) */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
