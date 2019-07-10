import Landing from '../../components/Landing.vue'
import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

let router = new Router({
  mode: 'history',
  routes: [  
    {
        path: '/',
        name: 'landing',
        component: Landing       
    }    
  ]  
})
export default router