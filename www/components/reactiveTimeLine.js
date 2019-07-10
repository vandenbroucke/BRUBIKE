
  import {Line, mixins} from 'vue-chartjs'
  import moment from 'moment'
  const { reactiveProp } = mixins
  
  export default{
    mixins: [reactiveProp,Line],
    data () {
      return {
        options: {
            responsive:true,
            animation: {
              easing:"easeOutExpo"
            },
          	maintainAspectRatio:!1, legend: {
              display: !1
            }
            ,scales: {
              yAxes:[ { ticks: {
                  display:1,
                  fontColor: "rgba(255,255,255,0.5)", fontStyle: "bold", beginAtZero: !0, maxTicksLimit: 10, padding: 0
                },                
                gridLines: {
                  drawTicks: 1, display: 1,
                }
              }
              ], xAxes:[ {
                  type: 'time',
                  time:{
                    parser: 'YYYY/MM/DD HH:mm:ss'
                  },
                  ticks: {
                  padding: -20, fontColor: "rgba(255,255,255,0.35)", fontStyle: "bold",
                  data:'source',
                  gridLines: {
                    color:"rgba(255,255,255,0.2)",
                    display:1,
                    drawTicks:1
                  }
                }
              }
              ]
            }
          }
      }
    },
    mounted () {
      this.renderChart(this.chartData, this.options);     
    }
  }