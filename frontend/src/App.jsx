//import React from 'react';
import bahia from './assets/bahia.png';
import flamengo1 from './assets/flamengo1.png';
import palmeiras from './assets/palmeiras.png';
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

 //* class DoubleButton extends React.Component {
  constructor(props) {
    super(props);
    this.handleItemClick = this.handleItemClick.bind(this);
  }
  
    handleItemClick(event, name) {
    if (name === 'sign-in') {
      apiCalendar.handleAuthClick()
    } else if (name === 'sign-out') {
      apiCalendar.handleSignoutClick();
    }
  }
} 




const App = () => {
  // Função para mostrar o escudo quando o botão é clicado
  const showLogo = (teamName) => {
    alert(`Você selecionou o escudo do ${teamName}`);
    // Aqui você pode adicionar lógica para exibir o escudo
  }

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




      <h1>Escolha seu time favorito para Acompanhar:
             </h1>
     
     <div className="logo-button"> 
      
      <button onClick={() => showLogo('bahia')}>
        <img src={bahia} ></img>
             Bahia
      </button>
      <button onClick={() => showLogo('Barcelona')}>
      <img src={flamengo1} ></img>
        Flamengo 
      </button>
      <button onClick={() => showLogo('Liverpool')}>
      <img src={palmeiras} ></img>
        Palmeiras 
      </button>

    </div>
      {/* Adicione mais botões conforme necessário */}
    </div>
  );
}

export default App;
