import React from 'react';

import {makeStyles} from '@mui/styles';
import {IconButton,} from '@mui/material';
import UploadFileRoundedIcon from '@mui/icons-material/UploadFileRounded';

const useStyles = makeStyles({
    imageInput: {
        display: 'none',
    },
});

type RecordButtonProps = {
    onFileChange: (e: React.ChangeEvent<HTMLInputElement>) => void,
    onClick: (ref: React.RefObject<HTMLInputElement>) => void,
    className?: string
}

export default function FileButton({onFileChange, onClick, className}: RecordButtonProps) {

    const inputFileRef = React.createRef<HTMLInputElement>();
    const classes = useStyles();

    const onFileChangeCapture = ( e: React.ChangeEvent<HTMLInputElement> ) => {
        onFileChange(e);
    };

    return (
        <div className={className}>
            <IconButton onClick={() => onClick(inputFileRef)} sx={{ padding: 0 }}>
                <UploadFileRoundedIcon fontSize='large'/>
            </IconButton>
            <input type="file" ref={inputFileRef} onChangeCapture={onFileChangeCapture} accept="image/*" className={classes.imageInput} capture="environment"/>
        </div>
    );
}