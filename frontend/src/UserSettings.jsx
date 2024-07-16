import axios from "axios";
import React, { useEffect, useState } from "react";


console.log(React)

const MOCKBIN = "http://localhost:8000/api/v1/user/info";


const UserSettings = () => {
  const [userData, setUserData] = useState(null);
  useEffect(() => {
    async function fetchData() {

      try {

        const loginData = localStorage.getItem('loginData');


        const response = await axios.get(
          MOCKBIN,
          {
            headers: {
              "Authorization": "Token " + loginData.token,
            },
          }
        );
        console.log('response: ', response);
        setUserData(response.data);
      } catch (error) {
        console.error('Erro ao buscar dados!', error);
      }
    }
    fetchData();
  }, []);

  if (!userData) {
    return <p>Carregando...</p>;
  }


  return (
    <div className="container">
      <div className="user-info">

        <img src={userData.picture || 'https://via.placeholder.com/100'} alt="Foto do Usuário" className="profile-photo" />
        <h2>{userData.middleName || 'Nome do Usuário'}</h2>
        <p>Email: <strong>{userData.lastName || 'example@example.com'}</strong></p>
        <p>Time escolhido: <strong>{userData.firstName || 'Time Exemplo FC'}</strong></p>
      </div>
      <div className="notification-settings">
        <h3>Configurações de Notificação:</h3>
        <ul>
          <li>Receber notificações sobre os jogos: <strong>{userData.notificationTime || '30 minutos antes'}</strong></li>
        </ul>
      </div>
    </div>
  );
};

export default UserSettings;
