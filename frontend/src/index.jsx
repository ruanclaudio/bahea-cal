import React from 'react'
import ReactDOM from 'react-dom/client'


import './index.css';
// import NotificationForm from './NotificationForm';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";

import Login from './components/Login.jsx'
import FormSettings from './components/FormSettings.jsx';
import Club from "./components/Club.jsx";
import UserSettings from './components/UserSettings.jsx';
import  { GoogleOAuthProvider }  from  '@react-oauth/google' ;
import './index.css'

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
    element: <Club/>,
  },

  {
      path: "/settings",
      element: <UserSettings/>

  },

  {
      path: "/settings/edit",
      element: <FormSettings/>,
  },

]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID}>
      <RouterProvider router={router} />
    </GoogleOAuthProvider>
  </React.StrictMode>
)
