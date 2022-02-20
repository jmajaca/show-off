import React from 'react';

import {BrowserRouter} from 'react-router-dom';

import './App.css';
import AppRoutes from './AppRoutes';

function App() {
  return (
      <BrowserRouter basename="/show-off">
        <AppRoutes/>
      </BrowserRouter>
  );
}

export default App;
