import React from 'react';

import {Routes, Route} from 'react-router-dom';

import MainPage from './pages/MainPage';

export default function AppRoutes(): JSX.Element {

    return (
        <Routes>
            <Route path="/" element={<MainPage/>}/>
            <Route path="/health" element={<h3>Health UP</h3>}/>
        </Routes>
    );

}