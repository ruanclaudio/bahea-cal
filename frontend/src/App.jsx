import ApiCalendar from "react-google-calendar-api";
import React from 'react';
const config = {
  clientId: process.env.GOOGLE_CLIENT_ID,
  apiKey: process.env.GOOGLE_API_KEY,
  scope: "https://www.googleapis.com/auth/calendar",
  discoveryDocs: [
    "https://www.googleapis.com/discovery/v1/apis/calendar/v3/rest",
  ],
};
const apiCalendar = new ApiCalendar(config);
export default class DoubleButton extends React.Component {
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
// import logo from './logo.svg';
// import './App.css';
// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }
// export default App;