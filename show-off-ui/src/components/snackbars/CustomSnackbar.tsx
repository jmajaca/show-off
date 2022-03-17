import React, {Dispatch, SetStateAction} from 'react'

import {Snackbar} from '@mui/material';
import MuiAlert, { AlertProps } from '@mui/material/Alert';


const Alert = React.forwardRef<HTMLDivElement, AlertProps>(function Alert(
    props,
    ref,
) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

type CustomSnackbarProps = {
    open: boolean,
    setOpen: Dispatch<SetStateAction<boolean>>,
    type: 'success' | 'error' | 'warning' | 'info'
    message: string,
    autoHideDuration?: number,
    vertical?: 'top' | 'bottom',
    horizontal?: 'left' | 'center' | 'right',
}

export default function CustomSnackbar({open, setOpen, type, message, autoHideDuration = 3000, vertical = 'top', horizontal = 'center'}: CustomSnackbarProps) {

    const handleClose = (event?: React.SyntheticEvent | Event, reason?: string) => {
        if (reason === 'clickaway') {
            return;
        }
        setOpen(false);
    };

    return (
        <Snackbar open={open} autoHideDuration={autoHideDuration} anchorOrigin={{ vertical, horizontal }} onClose={handleClose}>
            <Alert onClose={handleClose} severity={type}>
                {message}
            </Alert>
        </Snackbar>
    );

}