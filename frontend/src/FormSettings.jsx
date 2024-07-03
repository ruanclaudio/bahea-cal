import { useState } from 'react';

const NotificationForm = () => {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [calendar, setCalendar] = useState('gregorian');
    const [notification, setNotification] = useState('30min');
    const [club, setClub] = useState('clubA');
    const [anotherClub, setAnotherClub] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
    };

    return (
        <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="firstName">First Name:</label><br />
                <input 
                    type="text" 
                    id="firstName" 
                    value={firstName} 
                    onChange={(e) => setFirstName(e.target.value)} 
                    required 
                />
            </div>
            <div>
                <label htmlFor="lastName">Last Name:</label><br />
                <input 
                    type="text" 
                    id="lastName" 
                    value={lastName} 
                    onChange={(e) => setLastName(e.target.value)} 
                    required 
                />
            </div>
            <div>
                <label htmlFor="calendar">Calendar:</label><br />
                <select 
                    id="calendar" 
                    value={calendar} 
                    onChange={(e) => setCalendar(e.target.value)}
                >
                    <option value="Google">Google</option>
                    <option value="iPhone">iPhone</option>
                    <option value="Outros">Outros</option>
                </select>
            </div>
            <div>
                <label>Notify in:</label><br />
                <input 
                    type="radio" 
                    id="30min" 
                    name="notification" 
                    value="30min" 
                    checked={notification === '30min'}
                    onChange={(e) => setNotification(e.target.value)} 
                />
                <label htmlFor="30min">30 minutes before</label><br />
                <input 
                    type="radio" 
                    id="2hours" 
                    name="notification" 
                    value="2hours" 
                    checked={notification === '2hours'}
                    onChange={(e) => setNotification(e.target.value)} 
                />
                <label htmlFor="2hours">2 hours before</label><br />
                <input 
                    type="radio" 
                    id="1day" 
                    name="notification" 
                    value="1day" 
                    checked={notification === '1day'}
                    onChange={(e) => setNotification(e.target.value)} 
                />
                <label htmlFor="1day">1 day before</label>
            </div>
            <div>
                <label htmlFor="club">Selected Club:</label><br />
                <select 
                    id="club" 
                    value={club} 
                    onChange={(e) => setClub(e.target.value)}
                >
                    <option value="clubA">Club A</option>
                    <option value="clubB">Club B</option>
                    <option value="clubC">Club C</option>
                </select>
            </div>
            <div>
                <label htmlFor="anotherClub">Would you like to choose another club?</label><br />
                <input 
                    type="checkbox" 
                    id="anotherClub" 
                    checked={anotherClub} 
                    onChange={(e) => setAnotherClub(e.target.checked)} 
                />
                <label htmlFor="anotherClub">Yes</label>
            </div>
            <button type="submit">Submit</button>
        </form>
    );
};

export default NotificationForm;
