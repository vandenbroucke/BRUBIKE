<template> 
    <div class="v_landing">
        <header>
             <h1 class="uk-position-center">
                 BRUBIKE 
             </h1>
            <a
          class="github-button uk-align-right"
          href="https://github.com/vandenbroucke/monefy-web"
          data-size="large"
          data-show-count="true"
          aria-label="Star vandenbroucke/monefy-web on GitHub"
        >Star</a>           
        </header>
        <div class="timeline uk-card-default uk-card uk-card-body uk-position-bottom-center">
            <span class="uk-margin-small-right" uk-icon="icon:play;ratio:1.2" v-on:click="start_timeline()"></span>                    
            <VueSlideBar 
                        :min="0" 
                        v-model="timeline.current_time"
                        :max="200" 
                        :tooltipStyles="{ backgroundColor:'rgba(0,0,0,0)',color:'white', borderColor: 'rgba(255,255,255,.4)' }"
                        :processStyle="{backgroundImage: 'linear-gradient(-20deg, #b721ff 0%, #21d4fd 100%)'}"
                        class="slide_bar"/>                    
        </div> 
  
    <div id="selected_station_info" uk-offcanvas="flip: true; overlay: true">
    <div class="uk-offcanvas-bar">

        <button class="uk-offcanvas-close" type="button" uk-close></button>

        <h3>{{selected_station.name}}</h3>
        <reactive-time-line :chart-data="selected_station.history"></reactive-time-line>
      
    </div>
</div>


        <l-map :zoom="map.zoom" :center="map.center"  :options="map.options" lazy>
                    <l-tile-layer :url="map.url" :attribution="map.attribution"></l-tile-layer>
                    <l-marker
                        v-for="marker in markers"
                        :key="marker.name"
                        :class-name="''"
                        :lat-lng="marker.geo"
                        :icon="dynamic_icon(marker.label)"
                        v-on:click="select_station(marker.name)"
                        >         
                    </l-marker>
        </l-map>

    </div>
    
</template>
<script>
import Vue from 'vue'
import reactiveTimeLine from './reactiveTimeLine.js'
import L from 'leaflet'
import UIkit from 'uikit'
import {LMap, LTileLayer, LMarker,LPopup} from 'vue2-leaflet'
import devices from '../../data/devices.json'
import VueSlideBar from 'vue-slide-bar'
import MobilityHelper from '../js/mobility/index.js'


function lerpColor(a, b, amount) { 

    var ah = parseInt(a.replace(/#/g, ''), 16),
        ar = ah >> 16, ag = ah >> 8 & 0xff, ab = ah & 0xff,
        bh = parseInt(b.replace(/#/g, ''), 16),
        br = bh >> 16, bg = bh >> 8 & 0xff, bb = bh & 0xff,
        rr = ar + amount * (br - ar),
        rg = ag + amount * (bg - ag),
        rb = ab + amount * (bb - ab);

    return '#' + ((1 << 24) + (rr << 16) + (rg << 8) + rb | 0).toString(16).slice(1);
}

export default{
    data(){
        return{
            devices: devices,
            map:{
                options:{
                    zoomControl:false
                },                
                zoom:14,
                center: L.latLng(50.8503, 4.3517),
                url:'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
                attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
               
            },
            timeline:{
                current_time:0,
                is_playing:false
            },
            selected_station:{
                name:"",
                history:{
                    datasets:[{
                        data:[{x:0,y:0},{x:1,y:2},{x:3,y:3}],
                        fill:'origin',
                        borderColor:"rgba(255,255,255,.5)"                       
                    }]
                    }
            }

        };
    },
    components:{
        reactiveTimeLine,
        VueSlideBar,
        LMap, LTileLayer, LMarker,LPopup
    },
    methods:{
        /**
         * If the timeline was already playing it will simply stop the animation, otherwise it will start the timeline_loop from the current point.
         */
        start_timeline(){
            this.timeline.is_playing = !this.timeline.is_playing;
            this.timeline_loop();
        },
        /**
         * Will update the current time depending on a set interval. This in turn triggers the map & graph visualizations to be updated without explicit notice.
         */
        timeline_loop(){
            if(this.timeline.current_time==200)this.timeline.is_playing = false;
            if(this.timeline.is_playing){
                this.timeline.current_time+=1;



                setTimeout(this.timeline_loop,400)
            }            
        },
        select_station(d_n){
            this.selected_station.name=d_n;
            let slider = document.getElementById('selected_station_info');
            UIkit.offcanvas(slider).show();

            let device_idx = this.devices.findIndex(function(el){return el.name==d_n})
            
            let history = [];

            for(var i = 0;i <this.devices[device_idx].history.length;i++){
                history.push({
                    x:this.devices[device_idx].history[i].count_date,
                    y:this.devices[device_idx].history[i].count
                });                
            }


            this.selected_station.history= {
                    datasets:[{
                        data:history,
                        fill:'origin',
                        borderColor:"rgba(255,255,255,.5)",
                        borderWidth: 1      
                                      
                    }]
            }
            
        },
        dynamic_icon(count){
            const max = 60;
            let color = lerpColor('#00ff00',"#ff0000",count/100)
            let size = 35+ count/6;
            return  L.divIcon({
                    className: "number-icon",
                    iconSize: [size, size],
                    iconAnchor: [size/2, size/2],
                    popupAnchor: [3, -40],
                    html: "<span class='marker' style='background:"+color+";width:"+size+"px;height:"+size+"px;color:white;opacity:.8;'>"+count+"</span>"       
                })
        }
    },    

    computed:{       
       markers(){
           let m = [];
           if(devices){
            for(var i = 0;i< this.devices.length;i++){
                if(this.devices[i].history.length>0 && this.devices[i].history[this.timeline.current_time]){
                        m.push({
                    label:(this.devices[i].history[this.timeline.current_time])? this.devices[i].history[this.timeline.current_time].count:0,
                    geo:this.devices[i].geo,
                    name:this.devices[i].name

                }); 
                }
                
            }
           }
           return m;
       }
    },
    created: function(){
        const vm = this;
        for(var i =0; i < this.devices.length;i++){
            const l = i;
            MobilityHelper.load_history(this.devices[i].name).then(function (r) {     
                    vm.devices[l].history =  MobilityHelper.fillDates(r.data.data,r.data.timeGaps);
                    vm.$forceUpdate();
                    vm.devices=vm.devices;
                })
                .catch(function (error) {
                    // handle error
                    console.log(error);
                });
        }
    }
}
</script>