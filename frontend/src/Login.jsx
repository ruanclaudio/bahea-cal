
import axios from 'axios';

export default function Login() {
  
  <GoogleOAuthProvider clientId="470653035644-rkr19rof1eclp7f7gmd4044jt110hf9g.apps.googleusercontent.com"></GoogleOAuthProvider>;

  const scope = ["https://www.googleapis.com/auth/calendar https://www.googleapis.com/auth/calendar.app.created",
                  "https://www.googleapis.com/auth/userinfo.email",
                  "https://www.googleapis.com/auth/userinfo.profile",
                  "openid"]
  console.log('scope configurado = ', scope)
  const login = GoogleLogin({
    onSuccess: tokenResponse => console.log(tokenResponse),
  });

  const hasAccess = hasGrantedAllScopesGoogle(
    login.tokenResponse,
    scope
  );  
  console.log(hasAccess);

  // return (<div>
  //         <button onClick={ () => login()}>Login com Google</button>
  //         <button>(nao funciona) Log out</button>
  //   </div>);

  const handleLogin = async (credentialResponse) => {
    console.log('credential Response', credentialResponse);

    try {
      const response = await axios.post('http://localhost:8000/api/v1/calendar/token/', credentialResponse, {
        headers: {
          // 'Access-Control-Allow-Headers': '*',
          'Content-Type': 'application/json',
          // 'Allow-Control-Allow-Origin': '*',
          // 'Access-Control-Allow-Methods': '*'
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

  // return (<button onClick={() => teste()}> oiasodiaosio</button>)
  return (<button onClick={() => login()}> Fazer login</button>)

  // return(<GoogleLogin onSuccess={credentialResponse => {
  //     console.log(credentialResponse);
  //   }}
  //   onError={() => {
  //     console.log('Login Failed');
  //   }}
  // />) 

}


 