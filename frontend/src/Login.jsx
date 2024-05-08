import ApiCalendar from "react-google-calendar-api";
import React from 'react';
import {} from 'react-router-dom'

const config = {
  clientId: process.env.REACT_APP_GOOGLE_CLIENT_ID,
  apiKey: process.env.REACT_APP_GOOGLE_API_KEY,
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

 handleItemClick = async (event, name) => {
    

    if (name === 'sign-in') {
        try {
            await apiCalendar.handleAuthClick();
           
            // Ou qualquer outra ação após o login bem-sucedido
        } catch(error){
            //console.error('erro ocorrido' , error);
            
        }

       } else if (name === 'sign-out') {
        apiCalendar.handleSignoutClick();
    } 
};

  
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
  
