import React from 'react'
import ReactDOM from 'react-dom/client'
import Login from './Login.jsx'



import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Time from "./routes/Time.jsx";
import  { GoogleOAuthProvider }  from  '@react-oauth/google' ;
import './index.css'
import UserSettings from './UserSettings.jsx';

const router = createBrowserRouter([

  {
      path:"/",
      element: <Login/>,

  },
  {
    path: "/hello",
    element: <div> hello</div>,
  },
  {
    path: "/time",
    element: <Time />,
  },

  {
    path: "/settings",
    element: <UserSettings/>,
  },

]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <RouterProvider router={router} />
    </GoogleOAuthProvider>
  </React.StrictMode>
)
