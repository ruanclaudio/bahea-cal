import React from 'react';
import BahiaLogo from '../assets/bahia.png'; // Corrigindo o caminho para os arquivos de imagem
import flamengologo from '../assets/flamengo1.png';
import palmeiraslogo from '../assets/palmeiras.png';

class Time extends React.Component {
  // Função para mostrar o escudo quando o botão é clicado
  showLogo = (teamName) => {
    alert(`Você selecionou o ${teamName}`);
    // Aqui você pode adicionar lógica para exibir o escudo
  }

  render() {
    return (
      <div className='container'>
        
        <h1>Escolha seu time favorito para Acompanhar:</h1>
        
        <button onClick={() => this.showLogo('Bahia')}> {/* Alterando para this.showLogo */}
          <img src={BahiaLogo} alt="Bahia" style={{ width: '50px', height: '50px' }} /> Bahia
        </button>
        <button onClick={() => this.showLogo('Flamengo')}> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={flamengologo} alt="Flamengo" style={{ width: '50px', height: '50px' }} /> Flamengo 
        </button>
        <button onClick={() => this.showLogo('Palmeiras')}> {/* Alterando para this.showLogo e corrigindo o nome do time */}
          <img src={palmeiraslogo} alt="Palmeiras" style={{ width: '50px', height: '50px' }} /> Palmeiras 
        </button>
        {/* Adicione mais botões conforme necessário */}
      </div>
    );
  }
}

export default Time;
