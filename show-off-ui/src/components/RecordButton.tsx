import React, {Dispatch, SetStateAction} from 'react';

import {makeStyles} from '@mui/styles';
import {Button} from '@mui/material';
import {ProcessState} from '../enums/ProcessState';

const useStyles = makeStyles({
    imageInput: {
        display: 'none',
    },
    button: {
        width: '60vw',
    }
});

type RecordButtonProps = {
    processState: ProcessState,
    setProcessState: Dispatch<SetStateAction<ProcessState>>,
    setImage: Dispatch<SetStateAction<File | undefined>>,
    className?: string
}

export default function RecordButton({processState, setProcessState, setImage, className}: RecordButtonProps) {

    const inputFileRef = React.createRef<HTMLInputElement>();
    const classes = useStyles();

    const onFileChangeCapture = ( e: React.ChangeEvent<HTMLInputElement> ) => {
        if (e.target.files && e.target.files.length !== 0) {
            setImage(e.target.files[0]);
            setProcessState(ProcessState.SEND);
        }
    };

    const onClick = () => {
        if (processState === ProcessState.UPLOAD) {
            inputFileRef.current!.click();
        } else if (processState === ProcessState.SEND) {
            setProcessState(ProcessState.SENDING);
        }
    }

    return (
        <div className={className}>
            <Button variant="contained" color="error" onClick={onClick} className={classes.button}>{processState}</Button>
            <input type="file" ref={inputFileRef} onChangeCapture={onFileChangeCapture} accept="image/*" className={classes.imageInput} capture="environment"/>
        </div>
    );
}