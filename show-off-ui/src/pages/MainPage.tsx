import React from 'react';

import {makeStyles} from '@mui/styles';

import RecordButton from '../components/RecordButton';

const useStyles = makeStyles({
    container: {
        display: 'flex',
        justifyContent: 'center',
    },
    recordButton: {
        position: 'fixed',
        bottom: 100,
    }
});

export default function MainPage() {

    const classes = useStyles();

    const onClick = () => {};

    return (
        <div className={classes.container}>
            <RecordButton onClick={onClick} className={classes.recordButton}/>
        </div>
    );
}