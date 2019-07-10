import Vue from 'vue'
import App from '../components/App.vue'
import router from './router/index.js'
import UIkit from 'uikit'
import Icons from 'uikit/dist/js/uikit-icons';
import store from './store'
import 'leaflet/dist/leaflet.css'
import L from 'leaflet'

delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({  
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),  
  iconUrl: require('leaflet/dist/images/marker-icon.png'),  
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')  
})

UIkit.use(Icons)

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
