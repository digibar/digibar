import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Routes from './routes'
import VuePeerJS from 'vue-peerjs';
import Peer from 'peerjs';
import './style/style.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'

library.add(fas);


Vue.component('font-awesome-icon', FontAwesomeIcon);
Vue.use(BootstrapVue);
Vue.use (VueRouter);
Vue.use(IconsPlugin);
Vue.use(VuePeerJS, new Peer({}));

//Router
const router = new VueRouter({
  routes: Routes,
  mode: 'history'
});

const appConfig = {
  backend_uri: "http://localhost:5000/",
  video_bandwith: 50,
  audio_bandwith: 64
};

export const bus = new Vue();

Vue.config.productionTip = false;
Vue.prototype.$appConfig = appConfig;


new Vue({
  el:'#app',
  render: h => h(App),
  router: router
});
