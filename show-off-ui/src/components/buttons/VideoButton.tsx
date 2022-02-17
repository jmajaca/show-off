import React from 'react'

import {makeStyles} from '@mui/styles';
import {Button} from '@mui/material';

import {ProcessState} from '../../enums/ProcessState';

const useStyles = makeStyles({
    button: {
        width: '60vw',
    }
});

type VideoButtonProps = {
    processState: ProcessState,
    onClick: () => void,
    className?: string,
}

export default function VideoButton({processState, onClick, className}: VideoButtonProps) {

    const classes = useStyles();

    return (
        <div className={className}>
            <Button variant="contained" color="error" onClick={onClick} className={classes.button}>{processState}</Button>
        </div>
    );


}