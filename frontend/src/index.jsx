import React from 'react'
import ReactDOM from 'react-dom/client'
import Login from './Login.jsx'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import Time from "./routes/Time.jsx";
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
    path: "/Time",
    element: <Time />,
  },


]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  
  </React.StrictMode>,
)
