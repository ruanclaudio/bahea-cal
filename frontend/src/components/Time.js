// components/Time.js
//import React from 'react';
//import PropTypes from 'prop-types';

const Time = ({ nome }) => {
  // Função para mostrar o escudo quando o botão é clicado
  const showLogo = () => {
    alert(`Você selecionou o escudo do ${nome}`);
    // Lógica para exibir o escudo
  }

  return (
    <button onClick={showLogo}>
      {nome}
    </button>
  );
}

Time.propTypes = {
  nome: PropTypes.string.isRequired,
  escudo: PropTypes.string.isRequired
}

export default Time;
