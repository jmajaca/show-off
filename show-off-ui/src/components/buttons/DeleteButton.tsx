import React from 'react';

import {IconButton} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';

type DeleteButtonProps = {
    onClick: () => void,
    className?: string,
}

export default function DeleteButton({onClick, className}: DeleteButtonProps) {

    return (
        <div className={className}>
            <IconButton onClick={onClick}>
                <DeleteIcon/>
            </IconButton>
        </div>
    );

}