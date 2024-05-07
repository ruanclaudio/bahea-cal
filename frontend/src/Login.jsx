import ApiCalendar from "react-google-calendar-api";
import React from 'react';
import {} from 'react-router-dom'

const config = {
  clientId: process.env.GOOGLE_CLIENT_ID,
  apiKey: process.env.GOOGLE_API_KEY,
  scope: "https://www.googleapis.com/auth/calendar",
  discoveryDocs: [
    "https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest",
  ],
};



const apiCalendar = new ApiCalendar(config);
export default class Login extends React.Component {
  constructor(props) {
    super(props);
    this.handleItemClick = this.handleItemClick.bind(this);
  }
  handleItemClick(event, name) {
    if (name === 'sign-in') {
    console.log( apiCalendar.handleAuthClick())

    } else if (name === 'sign-out') {
      apiCalendar.handleSignoutClick();     }
  }

  
  render() {
    return (
      <div>
          <button
              onClick={(e) => this.handleItemClick(e, 'sign-in')}
              
          >
            sign-in
          </button>
          <button
              onClick={(e) => this.handleItemClick(e, 'sign-out')}
          >
            sign-out
          </button>
       </div>
      );
  }
}

