import ApiCalendar from "react-google-calendar-api";

const config = {
  clientId: process.env.GOOGLE_CLIENT_ID, 
  apiKey: process.env.GOOGLE_API_KEY, 
  scope: "https://www.googleapis.com/auth/calendar",
  discoveryDocs: [
    "https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest",
  ],
};

const apiCalendar = new ApiCalendar(config); 

const  eventFromNow : object  =  { 
    sumário : "Poc Dev From Now" , 
    hora : 480 , 
  } ;
  
  apiCalendar 
    . createEventFromNow ( eventoFromNow ) 
    . então ( ( resultado : objeto )  = >  { 
      console.log ( resultado ) ; } ) .​ catch ( ( erro : qualquer ) = > { console.log ( erro ) ; } ) ;​
    
      
      
    
  
  const  eventWithVideoConference : object  =  { 
    sumário : "Evento com conferência do Google Meet" , 
    início : { 
      dateTime : nova  data ( ) . toISOString ( ) , 
      timeZone : "Europa/Paris" , 
    } , 
    end : { 
      dateTime : new  Date ( new  Date ( ) . getTime ( )  +  3600000 ) . toISOString ( ) , 
      timeZone : "Europa/Paris" , 
    } , 
  } ;
  
  apiCalendar 
    . createEventWithVideoConference ( eventWithVideoConference ) 
    . então ( ( resultado : objeto )  = >  { 
      console.log ( resultado ) ; } ) .​ catch ( ( erro : qualquer ) = > { console.log ( erro ) ; } ) ;​
    

