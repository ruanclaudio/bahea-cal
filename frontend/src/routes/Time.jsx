import React from 'react';
import BahiaLogo from '../assets/bahia.png'; // Corrigindo o caminho para os arquivos de imagem
import flamengologo from '../assets/flamengo1.png';
import palmeiraslogo from '../assets/palmeiras.png';
import atleticologo from   '../assets/atletico.png';
import fluminenselogo from '../assets/fluminense.png';
import corinthiaslogo from '../assets/corinthias.png';

class Time extends React.Component {
  // Função para mostrar o escudo quando o botão é clicado
  showLogo = (teamName) => {
    alert(`Você selecionou o ${teamName}`);
    // Aqui você pode adicionar lógica para exibir o escudo
  }

  render() {
    return (
      <div className='container'>

        <h1>Adicione Jogos do Seu Time</h1>

        <h3>no calendário do seu celular</h3>
        <div className='button-container'>

        <button className="bahia-button" onClick={() => this.showLogo('Bahia')}> {/* Alterando para this.showLogo */}
          <img src={BahiaLogo} alt="Bahia" style={{ width: '50px', height: '50px' }} /> Bahia
        </button>

          <h5>Em breve...</h5>

        <div className="horizontal-buttons">
        <button onClick={() => this.showLogo('Flamengo')}> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={flamengologo} alt="Flamengo" style={{ width: '50px', height: '50px' }} /> Flamengo
        </button>
        <button onClick={() => this.showLogo('Palmeiras')}> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={palmeiraslogo} alt="Palmeiras" style={{ width: '50px', height: '50px' }} /> Palmeiras
        </button>
        <button onClick={() => this.showLogo('Flamengo')}> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={corinthiaslogo} alt="corinthinas" style={{ width: '50px', height: '50px' }} /> Corinthians
        </button>
        <button onClick={() => this.showLogo('Fluminense')}> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={fluminenselogo} alt="fluminense" style={{ width: '50px', height: '50px' }} /> Fluminense
        </button>
        <button onClick={() => this.showLogo('Atletico')}> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={atleticologo} alt="atletico" style={{ width: '50px', height: '50px' }} /> Atlético
        </button>
        </div>
      </div>
    </div>
    );
  }
}

export default Time;
