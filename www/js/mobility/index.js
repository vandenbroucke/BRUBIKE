/*
 * Mobility enables you to capture historical data from Mobility Brussels API
 */
import axios from 'axios'

Date.prototype.yyyymmdd = function() {
    var mm = this.getMonth() + 1; // getMonth() is zero-based
    var dd = this.getDate();
  
    return [this.getFullYear(),
            (mm>9 ? '' : '0') + mm,
            (dd>9 ? '' : '0') + dd
           ].join('');
  };

 
export default{

        load_history(device_name){

            let startDate = new Date();
            startDate.setDate(startDate.getDate() -3 );
            startDate =  startDate.yyyymmdd();
            let requestURL = "https://data-mobility.brussels/bike/api/counts/?request=history&featureID="+device_name+"&startDate="+startDate+"&endDate=22001210&outputFormat=json";
            return axios.get(requestURL);
        },
        fillDates(history,timegaps){
            for(var i = 0;i<history.length;i++){
                history[i].count_date +=" "+ timegaps[history[i].time_gap-1][1];
            }
            return history;
        }

    
}