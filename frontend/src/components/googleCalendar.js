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



