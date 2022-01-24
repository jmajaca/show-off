import React from 'react';

import {makeStyles} from '@mui/styles';

const useStyles = makeStyles({
    button: {
        position: 'relative'
    },
    record: {
        position: 'absolute',
        width: '50px',
        height: '50px',
        backgroundColor: 'red',
        borderRadius: '100%',
        border: 'none',
    },
    innerMargins: {
        margin: '7px 7px 7px 7px',
    },
    ring: {
        position: 'absolute',
        width: '60px',
        height: '60px',
        borderRadius: '100%',
        borderStyle: 'solid',
        borderWidth: '2px',
        borderColor: 'black',
        backgroundColor: 'transparent'
    }
});

type RecordButtonProps = {
    onClick: () => void,
    className?: string
}

export default function RecordButton({onClick, className}: RecordButtonProps) {

    const classes = useStyles();

    return (
        <div className={`${classes.button} ${className}`}>
            <div className={classes.ring}/>
            <button onClick={onClick} className={`${classes.record} ${classes.innerMargins}`}/>
        </div>
    );
}