// import React from 'react';
import BahiaLogo from '../assets/bahia.png'; // Corrigindo o caminho para os arquivos de imagem
import flamengologo from '../assets/flamengo1.png';
import palmeiraslogo from '../assets/palmeiras.png';
import atleticologo from   '../assets/atletico.png';
import fluminenselogo from '../assets/fluminense.png';
import corinthiaslogo from '../assets/corinthias.png';
import { useGoogleLogin } from '@react-oauth/google';
import {} from 'react-router-dom';
import axios from 'axios';

export default function Club(){

  const scope = [
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.app.created",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "openid"
  ];

  console.log('escopo configurado:');
  console.log(scope);

  // Função para mostrar o escudo quando o botão é clicado
  // const showLogo = (teamName) => {
  //   alert(`Você selecionou o ${teamName}`);
  //   // Aqui você pode adicionar lógica para exibir o escudo
  // }

  const handleLogin = async (credentialResponse) => {
    console.log('credential Response', credentialResponse);
    try {
        const response = await axios.post('http://localhost:8000/api/v1/calendar/token/', credentialResponse, {
          headers: {
            'Content-Type': 'application/json',
          }
        });

        console.log('response-data: ', response.data);
      } catch (error) {
        console.error('error: ', error);
    }
  }

  const login = useGoogleLogin({
    scope: "https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.app.created https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid",
    flow: 'auth-code',
    access_type: 'offline',
    prompt: 'consent',
    onSuccess: handleLogin,
  });


  return (
      <div className='container'>

        <h1>Adicione Jogos do Seu Time</h1>

        <h3>no calendário do seu celular</h3>
        <div className='button-container'>

        <button onClick={login}  className="bahia-button" >
          <img src={BahiaLogo} alt="Bahia" style={{ width: '50px', height: '50px' }} /> Bahia
        </button>

          <h5>Em breve...</h5>

        <div className="horizontal-buttons">
        <button> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={flamengologo} alt="Flamengo" style={{ width: '50px', height: '50px' }} /> Flamengo
        </button>
        <button> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={palmeiraslogo} alt="Palmeiras" style={{ width: '50px', height: '50px' }} /> Palmeiras
        </button>
        <button> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={corinthiaslogo} alt="corinthinas" style={{ width: '50px', height: '50px' }} /> Corinthians
        </button>
        <button> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={fluminenselogo} alt="fluminense" style={{ width: '50px', height: '50px' }} /> Fluminense
        </button>
        <button> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={atleticologo} alt="atletico" style={{ width: '50px', height: '50px' }} /> Atlético
        </button>
        </div>
      </div>
    </div>
    );
}


