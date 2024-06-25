import React, { useState } from 'react';

const FormularioNotificacao = () => {
    const [nome, setNome] = useState('');
    const [sobrenome, setSobrenome] = useState('');
    const [calendario, setCalendario] = useState('gregoriano');
    const [notificacao, setNotificacao] = useState('30min');
    const [clube, setClube] = useState('clubeA');
    const [outroClube, setOutroClube] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        /// Aqui você pode adicionar a lógica para lidar com o envio do formulário
        console.log({ nome, sobrenome, calendario, notificacao, clube, outroClube });
        console.log(React)
    };

    return (
           
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="nome">Nome:</label><br />
                <input 
                    type="text" 
                    id="nome" 
                    value={nome} 
                    onChange={(e) => setNome(e.target.value)} 
                    required 
                />
            </div>
            <div>
                <label htmlFor="sobrenome">Sobrenome:</label><br />
                <input 
                    type="text" 
                    id="sobrenome" 
                    value={sobrenome} 
                    onChange={(e) => setSobrenome(e.target.value)} 
                    required 
                />
            </div>
            <div>
                <label htmlFor="calendario">Calendário:</label><br />
                <select 
                    id="calendario" 
                    value={calendario} 
                    onChange={(e) => setCalendario(e.target.value)}
                >
                    <option value="gregoriano">Google</option>
                    <option value="juliano">Iphone</option>
                    <option value="islamico">Outros</option>
                    
                </select>
            </div>
            <div>
                <label>Notificar em:</label><br />
                <input 
                    type="radio" 
                    id="30min" 
                    name="notificacao" 
                    value="30min" 
                    checked={notificacao === '30min'}
                    onChange={(e) => setNotificacao(e.target.value)} 
                />
                <label htmlFor="30min">30 minutos antes</label><br />
                <input 
                    type="radio" 
                    id="2horas" 
                    name="notificacao" 
                    value="2horas" 
                    checked={notificacao === '2horas'}
                    onChange={(e) => setNotificacao(e.target.value)} 
                />
                <label htmlFor="2horas">2 horas antes</label><br />
                <input 
                    type="radio" 
                    id="1dia" 
                    name="notificacao" 
                    value="1dia" 
                    checked={notificacao === '1dia'}
                    onChange={(e) => setNotificacao(e.target.value)} 
                />
                <label htmlFor="1dia">1 dia antes</label>
            </div>
            <div>
                <label htmlFor="clube">Clube selecionado:</label><br />
                <select 
                    id="clube" 
                    value={clube} 
                    onChange={(e) => setClube(e.target.value)}
                >
                    <option value="clubeA">Clube A</option>
                    <option value="clubeB">Clube B</option>
                    <option value="clubeC">Clube C</option>
                </select>
            </div>
            <div>
                <label htmlFor="outro_clube">Deseja escolher outro clube?</label><br />
                <input 
                    type="checkbox" 
                    id="outro_clube" 
                    checked={outroClube} 
                    onChange={(e) => setOutroClube(e.target.checked)} 
                />
                <label htmlFor="outro_clube">Sim</label>
            </div>
            <button type="submit">Enviar</button>
        </form>
    );
};

export default FormularioNotificacao;
