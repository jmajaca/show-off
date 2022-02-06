import React, {Dispatch, SetStateAction} from 'react';

import {IconButton} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

import {ProcessState} from '../enums/ProcessState';
import background from '../assets/background.png'

type DeleteButtonProps = {
    className?: string,
    setProcessState: Dispatch<SetStateAction<ProcessState>>,
    setImage: Dispatch<SetStateAction<File | undefined>>,
}

export default function DeleteButton({className, setProcessState, setImage}: DeleteButtonProps) {

    const onDeleteClick = () => {
        setProcessState(ProcessState.UPLOAD);
        setImage(undefined);
    }

    return (
        <div className={className}>
            <IconButton onClick={onDeleteClick}>
                <DeleteIcon/>
            </IconButton>
        </div>
    );

}