import React, {useEffect} from 'react';

import {makeStyles} from '@mui/styles';
import {IconButton,} from '@mui/material';
import UploadFileRoundedIcon from '@mui/icons-material/UploadFileRounded';
import {ProcessState} from '../../enums/ProcessState';

const useStyles = makeStyles({
    imageInput: {
        display: 'none',
    },
});

type RecordButtonProps = {
    onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void,
    onClick: (ref: React.RefObject<HTMLInputElement>) => void,
    sendAnimationFlag: boolean,
    className?: string
}

export default function FileButton({onFileChange, onClick, sendAnimationFlag = false, className}: RecordButtonProps) {

    const rootRef = React.createRef<SVGSVGElement>();
    const inputFileRef = React.createRef<HTMLInputElement>();
    const classes = useStyles();

    useEffect(() => {
        if (sendAnimationFlag) {
            rootRef.current?.style.setProperty('display', 'none')
        }
    }, [sendAnimationFlag])

    const onFileChangeCapture = ( e: React.ChangeEvent<HTMLInputElement> ) => {
        onFileChange(e);
    };

    return (
        <div className={className}>
            <IconButton onClick={() => onClick(inputFileRef)} sx={{ padding: 0 }}>
                <UploadFileRoundedIcon ref={rootRef} fontSize='large'/>
            </IconButton>
            <input type="file" ref={inputFileRef} onChangeCapture={onFileChangeCapture} accept="image/*" className={classes.imageInput} capture="environment"/>
        </div>
    );
}