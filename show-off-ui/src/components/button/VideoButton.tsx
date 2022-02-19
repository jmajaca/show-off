import React, {createRef, useEffect} from 'react'

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
    sendAnimationFlag: boolean,
    onClick: () => void,
    className?: string,
}

export default function VideoButton({processState, sendAnimationFlag = false, onClick, className}: VideoButtonProps) {

    const classes = useStyles();

    const buttonRef = createRef<HTMLButtonElement>();

    useEffect(() => {
        if (sendAnimationFlag) {
            const leftOffset = buttonRef.current?.getBoundingClientRect().left;
            const topOffset = buttonRef.current?.getBoundingClientRect().top;
            buttonRef.current?.style.setProperty('transition', 'width 1.5s');
            buttonRef.current?.style.setProperty('position', 'fixed');
            buttonRef.current?.style.setProperty('left', leftOffset + 'px');
            buttonRef.current?.style.setProperty('top', topOffset + 'px');
            buttonRef.current?.style.setProperty('width', '70vw');
        }
    }, [sendAnimationFlag])

    return (
        <div className={className}>
            <Button ref={buttonRef} variant="contained" color="error" onClick={onClick} className={classes.button}>{processState}</Button>
        </div>
    );


}