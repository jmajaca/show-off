import React from 'react';

import {makeStyles} from '@mui/styles';

import RecordButton from '../components/RecordButton';
import RecordBackground from '../components/RecordBackground';

const useStyles = makeStyles({
    container: {
        display: 'flex',
        justifyContent: 'center',
        width: '100%',
        height: '100%',
    },
    recordButton: {
        position: 'fixed',
        bottom: 100,
    },
    recordBackground: {
        width: '100%',
        height: '100%',
    }
});

export default function MainPage() {

    const classes = useStyles();

    const onClick = () => {};

    return (
        <div className={classes.container}>
            <RecordBackground className={classes.recordBackground}/>
            <RecordButton onClick={onClick} className={classes.recordButton}/>
        </div>
    );
}