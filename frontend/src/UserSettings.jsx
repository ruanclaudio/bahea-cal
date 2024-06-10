// import React from "react";
const UserSettings = () => {


    return (
      <div className="container">
        <div className="user-info">
          <img src="https://via.placeholder.com/100" alt="Foto do Usuário" className="profile-photo" />
          <h2>Nome do Usuário</h2>
          <p>Time escolhido: <strong>Time Exemplo FC</strong></p>
        </div>
        <div className="notification-settings">
          <h3>Configurações de Notificação:</h3>
          <ul>
            <li>Receber notificações sobre os jogos: <strong>30 minutos antes</strong></li>
          </ul>
        </div>
      </div>
    );
  };
  
  export default UserSettings;